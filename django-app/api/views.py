"""
API views.

The API serves the response in either browsable format, by default, or when
including a "format=api" query parameter, or in JSON format, when including
a "format=json" query parameter.

The list views that support optional filtering indicate that in their
docstrings. For those views filtering can be applied as follows.

A URL may optionally include query parameters to filter the
JSON response. Query parameter keys that cause filtering should be
one of the field names in the FILTER_FIELDS list. Any other key is
ignored. The corresponding value is exact matched against the field
value in every table row. Multiple "key=value" pairs may be provided,
in any order, including multiple values for the same key.
"""

from django.db.models import Sum
from django.core.exceptions import FieldError
from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from collections import OrderedDict, Counter
from .models import (
    CropDiversity,
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    SubsidyRecipients,
    RegionLookup,
    NassCommodityArea,
    NassCommodityFarms,
    OainHarvestAcres,
    ExportsHistoricalCleaned,
)
from .serializers import (
    MetadataSerializerWrapped,
    NassAnimalsSalesSerializerWrapped,
    SubsidyDollarsSerializerWrapped,
    SubsidyRecipientsSerializerWrapped,
    NassCommodityAreaSerializerWrapped,
    NassCommodityFarmsSerializerWrapped,
    OainHarvestAcresSerializerWrapped,
)

# Metadata dictionary of database tables keyed on the table_name. It will be
# populated by fetch_metadata() when the first view that needs it is called.
metadata_dict = {}
# Oregon region -> fips lookup dictionary.  It will be
# populated by fetch_metadata() when the first view that needs it is called.
region_to_fips = {}
fips_to_region = {}

METADATA_FIELDS = (
    'name',
    'description',
    'table_name',
    'unit',
    'field',
    'source_name',
    'source_link'
)


def mean_stddev(items):
    from math import sqrt
    """
    Calculate the mean and population standard deviation of items list.
    Return the (<mean>, <stddev>) tuple
    """
    mean = sum(items) / len(items)
    sum_squared_diffs = sum([(item - mean) ** 2 for item in items])
    return (mean, sqrt(sum_squared_diffs / len(items)))


def grade(mean, stddev, item):
    """
    Return a grade (relative position) for an item among a list of items.
    """
    if item < mean - 2 * stddev:
        return "very low"
    if item < mean - stddev:
        return "low"
    if item < mean + stddev:
        return "moderate"
    if item < mean + 2 * stddev:
        return "high"
    return "very high"


def cache_lookups():
        if not metadata_dict:
            fetch_metadata(Metadata)
        if not region_to_fips:
            fetch_region_lookup(RegionLookup)


def fetch_metadata(metadata_model):
    """
    Fetch the metadata table, and store it in metadata_dict.
    """
    metadata = OrderedDict()
    metadata_query = metadata_model.objects.all()
    for table in metadata_query:
        for field in METADATA_FIELDS:
            metadata[field] = table.__dict__[field]
            # Add the metadata to metadata_dict
        metadata_dict[table.table_name] = metadata.copy()


def get_most_recent_year(model):
    """
    Return the most recent year for a model from the database.

    If the model does not exist or it has no year field, None is returned.
    """
    try:
        return model.objects.latest('year').year
    except (model.DoesNotExist, AttributeError):  # model does not exist
        return None
    except FieldError:  # model does not have a year field
        return None


def fetch_region_lookup(region_lookup_model):
    """
    Fetch region lookup tables. Stores only region and fips fields in
    lookup dictionaries.
    """
    crop_div_qs = CropDiversity.objects.all()
    for region_entry in region_lookup_model.objects.values(
        'region',
        'fips'
    ):
        county_name = region_entry['region']
        fips = region_entry['fips']
        if fips == 41000:
            region_to_fips[county_name] = {
                'fips': fips,
                'crop diversity score': None
            }
            fips_to_region[fips] = {
                'region': county_name,
                'crop diversity score': None
            }
        else:
            cd = crop_div_qs.get(county_name=county_name.upper())
            region_to_fips[county_name] = {
                'fips': fips,
                'crop diversity score': float(cd.diversity_score)
            }
            fips_to_region[fips] = {
                'region': county_name,
                'crop diversity score': float(cd.diversity_score)
            }


class FilteredAPIView(APIView):
    """
    APIView extended with filtered query dictionary generator method
    """
    @staticmethod
    def query_dict(query_params, filter_fields):
        # Build dictionary of filter parameters (exclude 'format', etc.)
        filter_params = {}
        for param in query_params.keys():
            if param in filter_fields:
                vals = query_params.getlist(param)
                # Convert 'county' to 'fips'
                if param == 'county':
                    vals = [region_to_fips[v]['fips'] for v in vals]
                    param = 'fips'
                filter_params[param] = vals
        # Augment dictionary keys with __in for looking up list inclusion
        query = {key + '__in': vals for key, vals in filter_params.items()}
        return query


class EndpointIndexView(APIView):
    """
Cropcompass API endpoints can be accessed at the URLs below. Add "format=json"
query parameter to get JSON response.
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer)

    # def get_renderers(self):
    #     return [renderer() for renderer in self.renderer_classes]

    def get(self, request, format=None):
        """
        Return a list of API endpoints with their documentation.
        """
        endpoints = [
            ('List metadata for DB tables', 'metadata'),
            ('County statistics - table view', 'county_stats'),
            ('List commodities by area - row view', 'nass_commodity_area_list'),
            ('List commodities by area - table view', 'nass_commodity_area_table'),
            ('List commodities by number of farms - row view', 'nass_commodity_farms_list'),
            ('List commodities by harvested acres - row view', 'oain_harvest_acres_list'),
            ('List animal sales - row view', 'nass_animals_sales'),
            ('Subsidy Dollars - row view', 'subsidy_dollars_data'),
            ('Subsidy Dollars - table view', 'subsidy_dollars_table'),
            ('Subsidy Dollars - timeline view', 'subsidy_dollars_timeline'),
            ('Subsidy Dollars - top 5 counties', 'subsidy_dollars_top_counties'),
            ('Subsidy Dollars - top 5 commodities', 'subsidy_dollars_top_commodities'),
            ('Subsidy Recipients - row view', 'subsidy_recipients_data'),
            ('Crop Diversity - row view', 'crop_diversity_data'),
            ('Oregon Exports - timeline view', 'oregon_exports_timeline'),
            ('Oregon Export Commodities - list view', 'oregon_export_commodities'),
            ('Oregon Top 5 Export Commodities - list view', 'oregon_exports_top_commodities'),
        ]
        endpoint_dict = OrderedDict()
        for endpoint_name, path in endpoints:
            endpoint_dict[endpoint_name] = api_reverse(path, request=request)
        return Response(endpoint_dict)


class FilteredListView(FilteredAPIView):
    """
    Endpoint class allowing filtering by arbitrary params.
    """
    filter_fields = ['commodity', 'year', 'fips', 'county']
    model = None
    serializer = None

    def __init__(self, **kwargs):
        self.queryset = self.queryset if hasattr(self, 'queryset') else self.model.objects.all()
        super(FilteredAPIView, self).__init__(**kwargs)

    def get(self, request, format=None):
        if request.query_params:
            # Generate query filter dict
            filters = self.query_dict(request.query_params, self.filter_fields)
            # Generate queryset
            qs = self.queryset.filter(**filters)
        else:
            qs = self.queryset.all()

        serializer = self.serializer({
            'error': None,
            'rows': qs.count(),
            'data': qs
        })
        return Response(serializer.data)


class MetadataView(FilteredListView):
    """
    List metadata for available DB tables.
    """
    model = Metadata
    serializer = MetadataSerializerWrapped


class NassAnimalsSalesList(FilteredListView):
    """
    List animal sales. Exclude rows where animals == null

    By default all data in the table is returned, row-wise. Filtered results by year, fips, and commodity may be specified by providing query parameters

    Example filtering: "?commodity=Tomatoes&fips=41005&year=2012&year=2007" to get Tomatoes data from county (fips=41005) for both 2012 and 2007.
    """
    filter_fields = ['fips', 'commodity', 'year']
    model = NassAnimalsSales
    serializer = NassAnimalsSalesSerializerWrapped
    queryset = model.objects.filter(animals__isnull=False)


class NassCommodityAreaList(FilteredListView):
    """
    List commodities by area. Exclude rows where acres == null

    By default all data in the table is returned, row-wise. Filtered results by year, fips, and commodity may be specified by providing query parameters

    Example filtering: "?commodity=Tomatoes&fips=41005&year=2012&year=2007" to get Tomatoes data from county (fips=41005) for both 2012 and 2007.
    """
    filter_fields = ['fips', 'commodity', 'year']
    model = NassCommodityArea
    serializer = NassCommodityAreaSerializerWrapped
    queryset = model.objects.filter(acres__isnull=False)


class CommodityAreaTable(FilteredAPIView):
    """
    Table of (commodity -> area) for Oregon or selected county and only from the most recent year in the DB (Section B).
    """
    @staticmethod
    def fill_in_data(query):
        """Populate data array from the query"""

        data_array = query.values('commodity', 'acres')
        commodity_list = query.distinct('commodity').values_list('commodity', flat=True)

        tempdata = []

        for commodity in commodity_list:
            acres = data_array.filter(commodity=commodity).aggregate(Sum('acres'))['acres__sum']
            tempdata.append({
                'commodity': commodity,
                'acres': acres
            })

        return tempdata

    def get(self, request, format=None):
        """Return table of county or Oregon state (commodity -> farm area) for the most recent year for which data is available.
        """
        # Fetch metadata and region lookup tables from database if necessary
        cache_lookups()
        # Get the most recent year for commodity area
        latest_year = get_most_recent_year(NassCommodityArea)
        data = {
            'error': None,
            'unit': "acres",
            'year': latest_year,
            'description': 'Commodity area for each commodity in {}',
            'data': [],
            'total_acres': 0
        }
        qs = NassCommodityArea.objects.filter(
            acres__isnull=False,
            year=latest_year
        ).exclude(commodity='Total Acres')

        query_params = request.query_params.copy()  # create mutable copy
        if 'county' in query_params:
            # remove county from query_params because of region_to_fips mapping
            county = query_params.pop('county')[0]
            qs = qs.filter(fips=region_to_fips[county]['fips'])
            data.update({
                'description': data['description'].format(county) + ' County',
                'region': county,
            })
        else:
            data.update({
                'description': data['description'].format('Oregon'),
                'region': 'Oregon (Statewide)'
            })

        # enable filtering on all fields
        all_fields = [f.name for f in NassCommodityArea._meta.fields]
        filters = self.query_dict(query_params, all_fields)
        # data['filters'] = filters
        qs = qs.filter(**filters)

        data['data'] = self.fill_in_data(qs)
        data['total_acres'] = qs.aggregate(Sum('acres'))['acres__sum']
        return Response(data)


class NassCommodityFarmsList(FilteredListView):
    """
    List commodities by number of farms. Exclude rows where farms == null

    By default all data in the table is returned, row-wise. Filtered results by year, fips, and commodity may be specified by providing query parameters

    Example filtering: "?commodity=Tomatoes&fips=41005&year=2012&year=2007" to get Tomatoes data from county (fips=41005) for both 2012 and 2007.
    """
    filter_fields = ['fips', 'commodity', 'year']
    model = NassCommodityFarms
    serializer = NassCommodityFarmsSerializerWrapped
    queryset = model.objects.filter(farms__isnull=False)


class OainHarvestAcresList(FilteredListView):
    """
    List commodities by number of harvested acres. Exclude rows where harvested_acres == null

    By default all data in the table is returned, row-wise. Filtered results by year, fips, and commodity may be specified by providing query parameters

    Example filtering: "?commodity=Tomatoes&fips=41005&year=2012&year=2007" to get Tomatoes data from county (fips=41005) for both 2012 and 2007.
    """
    filter_fields = ['fips', 'commodity', 'year']
    model = OainHarvestAcres
    serializer = OainHarvestAcresSerializerWrapped
    queryset = model.objects.filter(harvested_acres__isnull=False)


class SubsidyDollarsList(FilteredListView):
    """
    List subsidy dollars, optionally filtered on commodity, year, county or fips. Use either fips or county, but not both in the same query.

    By default all data in the table is returned, row-wise. Filtered results by year, commodity, county or fips may be specified by providing query parameters.

    Example filtering: "?year=2012&year=2003&commodity=Tree&county=Baker" to get Tree data from Baker county for both 2012 and 2003.
    """
    cache_lookups()
    model = SubsidyDollars
    serializer = SubsidyDollarsSerializerWrapped


class SubsidyDollarsTable(APIView):
    """
    Table of county or Oregon state (commodity -> subsidy
    dollars) for the most recent year for which data is available in the DB.

    By default returns Oregon statewide data. Add query parameter "county" to
    get data for a specific county.

    Example:
    /table/subsidy_dollars/?county=Linn
    """
    @staticmethod
    def fill_in_data(query, fields=(), **kwargs):
        """Populate data array from the query"""
        data = query.values(*fields)

        if kwargs.get('unique', False):
            pass

        return data

    def get(self, request, format=None):
        # Fetch metadata and region lookup tables from database if necessary
        cache_lookups()
        # Get the most recent year for subsidy dollars
        latest_year = get_most_recent_year(SubsidyDollars)
        data = {
            'error': None,
            'unit': metadata_dict['subsidy_dollars']['unit'],
            'year': latest_year,
            'description': 'Subsidy dollars for each commodity in {}',
            'data': []
        }
        # If a county has been selected in the query parameters
        if 'county' in request.query_params:
            county = request.query_params['county']
            subsidy_dollars = SubsidyDollars.objects.filter(
                year=latest_year,
                fips=region_to_fips[county.capitalize()]['fips'])
            data['description'] = data['description'].format(county) + ' County'
            data.update({
                'rows': subsidy_dollars.count(),
                'region': county,
            })
            data['data'] = self.fill_in_data(subsidy_dollars,
                                             fields=('commodity', 'subsidy_dollars'))
        # If no county is specified, return Oregon total subsidies
        else:
            subsidy_dollars = SubsidyDollars.objects.filter(
                year=latest_year,
                fips=41000)
            data['description'] = data['description'].format('Oregon')
            data.update({
                'rows': subsidy_dollars.count(),
                'region': 'Oregon (Statewide)',
            })
            data['data'] = self.fill_in_data(subsidy_dollars,
                                             fields=('commodity', 'subsidy_dollars'))
        return Response(data)


class SubsidyDollarsTimeline(APIView):
    """
    Table of county or Oregon state (year -> subsidy dollars) totaled over all commodities.

    By default returns Oregon statewide data. Add query parameter "county" to
    get data for a specific county.

    Example:
    /table/subsidy_dollars_timeline/?county=Linn
    """
    @staticmethod
    def fill_in_data(query, fields=(), **kwargs):
        """Populate data array from the query"""
        data = query.values(*fields)

        if kwargs.get('unique', False):
            pass

        return data

    def get(self, request, format=None):
        # Fetch metadata and region lookup tables from database if necessary
        cache_lookups()
        data = {
            'error': None,
            'unit': metadata_dict['subsidy_dollars']['unit'],
            'description': 'Subsidy dollar totals in each year in {}',
            'data': []
        }
        qs = SubsidyDollars.objects.all()
        county = request.query_params.get('county', None)
        if county:
            top_qs = qs.filter(fips=region_to_fips[county.capitalize()]['fips'])
            # Build a list of unique sorted years
            years_set = set(top_qs.values_list('year', flat=True))
            years = sorted(list(years_set))
            for year in years:
                qs = top_qs.filter(year=year)
                total_subsidy = qs.aggregate(Sum('subsidy_dollars'))['subsidy_dollars__sum']
                data['data'].append(
                    {"year": year, "subsidy_dollars": total_subsidy}
                )
            data['description'] = data['description'].format(county) + ' County'
            data.update({
                'rows': len(years),
                'region': county,
            })
        # If no county is specified, return Oregon total subsidies
        else:
            years_set = set(qs.values_list('year', flat=True))
            years = sorted(list(years_set))
            for year in years:
                new_qs = qs.filter(year=year)
                total_subsidy = new_qs.aggregate(Sum('subsidy_dollars'))['subsidy_dollars__sum']
                data['data'].append(
                    {"year": year, "subsidy_dollars": total_subsidy}
                )
            data['description'] = data['description'].format('Oregon')
            data.update({
                'rows': len(years),
                'region': 'Oregon (Statewide)',
            })
        return Response(data)


class SubsidyDollarsTopFiveCounties(APIView):
    """
    Top five counties plus Oregon (statewide) subsidy summed over all
    commodities.
    """
    def get(self, request, format=None):
        cache_lookups()
        # Get the most recent year for subsidy dollars
        latest_year = get_most_recent_year(SubsidyDollars)
        data = {
            'error': None,
            'unit': metadata_dict['subsidy_dollars']['unit'],
            'year': latest_year,
            'description': 'Subsidy dollars for top five counties',
            'data': []
        }
        qs = SubsidyDollars.objects. \
            filter(year=latest_year)
        subs_c = Counter()
        for subs in qs:
            region = fips_to_region[subs.fips]['region']
            subs_c[region] = subs_c.get(region, 0) + subs.subsidy_dollars
        top_six_comm = dict(subs_c.most_common(6))
        data['data'].append(top_six_comm)
        return Response(data)


class SubsidyDollarsTopFiveCommodities(APIView):
    """
    Top five commodities subsidy summed over all counties.
    """
    def get(self, request, format=None):
        cache_lookups()
        # Get the most recent year for subsidy dollars
        latest_year = get_most_recent_year(SubsidyDollars)
        data = {
            'error': None,
            'unit': metadata_dict['subsidy_dollars']['unit'],
            'year': latest_year,
            'description': 'Subsidy dollars for top five commodities',
            'data': []
        }
        qs = SubsidyDollars.objects.filter(
            year=latest_year
        )
        subs_c = Counter()
        for subs in qs:
            subs_c[subs.commodity] = subs_c.get(subs.commodity, 0) + subs.subsidy_dollars
        top_five_comm = dict(subs_c.most_common(5))
        data['data'].append(top_five_comm)
        return Response(data)


class CropDiversityList(APIView):
    """
    List crop diversity scores for Oregon counties, and average score over all counties.
    """
    def get(self, request, format=None):
        cache_lookups()
        # Get the most recent year for subsidy dollars
        data = {
            'error': None,
            'unit': metadata_dict['crop_diversity']['unit'],
            'description': 'Crop diversity scores for Oregon counties',
            'average_diversity_score': None,
            'data': []
        }
        total_div_score = 0
        total_counties = 0
        diversity_dict = {}
        for fips, value in fips_to_region.items():
            if fips != 41000:
                total_div_score += value['crop diversity score']
                total_counties += 1
                diversity_dict[value['region']] = value['crop diversity score']
        data['average_diversity_score'] = total_div_score / total_counties
        data['data'].append(diversity_dict)
        return Response(data)


class SubsidyRecipientsList(FilteredListView):
    """
    List subsidy recipients, optionally filtered on commodity and/or year.

    By default all data in the table is returned, row-wise. Filtered results by year, and commodity may be specified by providing query parameters

    Example filtering: "?year=2012&year=2003&commodity=Tree" to get Tree data for both 2012 and 2003.
    """
    model = SubsidyRecipients
    serializer = SubsidyRecipientsSerializerWrapped


class CountyStatisticsList(APIView):
    """
    List bucketed statistics, county name, fips for all Oregon counties. Table
    values are summed over all commodities in the selected year, which is the
    most recent year available, unless year is specified as a query parameter.
    """

    @staticmethod
    def find_stats(fips_no_or, year, model, value_field):
        """
        Return a {fips: grade} dictionary, mean, stddev for a dataset (model)
        in a given year.
        """
        qs = model.objects.filter(year=year)
        items = []
        value_field_sum_key = value_field + "__sum"
        for f in fips_no_or:
            item = qs.filter(fips=f).aggregate(Sum(value_field))[value_field_sum_key]
            # If the Sum() returned None, change it to zero.
            if item is None:
                item = 0
            else:
                # This type conversion is needed for DecimalField type data
                item = float(item)
            items.append(item)
        mean, stddev = mean_stddev(items)
        grades = {}
        for idx, f in enumerate(fips_no_or):
            grades[f] = grade(mean, stddev, items[idx])
        return (grades, mean, stddev)

    def get(self, request, format=None):
        cache_lookups()
        # Check for requested year
        year_qp = request.query_params.get('year', None)
        data = {
            'error': None,
            'description': 'Bucketed statistics, county name, fips for Oregon counties',
            'stats': {},
            'data': []
        }
        if year_qp is None:
            # The most recent year for SubsidyDollars will be used for all stats
            year = get_most_recent_year(SubsidyDollars)
        else:
            year = year_qp
        data['year'] = year

        results = {}
        # List of fips (integer) for all counties; excludes Oregon (statewide)
        fips_no_or = [f for f in fips_to_region.keys() if f > 41000]
        # Crop Diversity stats
        items = [fips_to_region[f]['crop diversity score'] for f in fips_no_or]
        mean, stddev = mean_stddev(items)
        data['stats']['cropDiversity'] = {'mean': mean, 'stddev': stddev}
        grades = {}
        for idx, f in enumerate(fips_no_or):
            grades[f] = grade(mean, stddev, items[idx])
        results['cropDiversity'] = grades
        # Subsidy Dollars stats
        stats, mean, stddev = self.find_stats(fips_no_or, year, SubsidyDollars, 'subsidy_dollars')
        results['subsidyLevel'] = stats
        data['stats']['subsidyLevel'] = {'mean': mean, 'stddev': stddev}
        # Subsidy Recipients stats
        stats, mean, stddev = self.find_stats(fips_no_or, year, SubsidyRecipients, 'subsidy_recipients')
        results['subsidyRecipients'] = stats
        data['stats']['subsidyRecipients'] = {'mean': mean, 'stddev': stddev}
        # NASS Commodity Farms stats
        stats, mean, stddev = self.find_stats(fips_no_or, year, NassCommodityFarms, 'farms')
        results['numberOfFarms'] = stats
        data['stats']['numberOfFarms'] = {'mean': mean, 'stddev': stddev}
        # NASS Commodity Area (Production) stats
        stats, mean, stddev = self.find_stats(fips_no_or, year, NassCommodityArea, 'acres')
        results['cropProduction'] = stats
        data['stats']['cropProduction'] = {'mean': mean, 'stddev': stddev}
        for fips in fips_no_or:
            stats_dict = {}
            stats_dict['subsidyLevel'] = results['subsidyLevel'][fips]
            stats_dict['subsidyRecipients'] = results['subsidyRecipients'][fips]
            stats_dict['numberOfFarms'] = results['numberOfFarms'][fips]
            stats_dict['cropProduction'] = results['cropProduction'][fips]
            stats_dict['cropDiversity'] = results['cropDiversity'][fips]
            stats_dict['fips'] = fips
            stats_dict['county'] = fips_to_region[fips]['region']
            data['data'].append(stats_dict)
        data['rows'] = len(data['data'])
        return Response(data)


class OregonExportsTimeline(APIView):
    """
    Table of Oregon state (year -> export) for a selected commodity.

    By default returns total export for all commodities. Add query parameter
    "commodity" to get data for a specific commodity.

    Example:
    /table/oregon_exports_timeline/?commodity=Quinoa
    """

    def get(self, request, format=None):
        # Fetch metadata and region lookup tables from database if necessary
        cache_lookups()
        data = {
            'error': None,
            'data': []
        }
        qs = ExportsHistoricalCleaned.objects.all()
        commodity = request.query_params.get('commodity', None)
        if commodity:
            top_qs = qs.filter(commodity=commodity)
            # Build a list of unique sorted years
            years_set = set(top_qs.values_list('time_year', flat=True))
            years = sorted(list(years_set))
            for year in years:
                qs = top_qs.filter(time_year=year)
                export = qs.aggregate(Sum('value_num'))['value_num__sum']
                data['data'].append(
                    {"year": year, "export": export}
                )
            data.update({
                'rows': len(years),
                'commodity': commodity,
                'description': 'Oregon exports of {} in each year'.format(commodity),
            })
        # If no commodity is specified, return Oregon total export
        else:
            years_set = set(qs.values_list('time_year', flat=True))
            years = sorted(list(years_set))
            for year in years:
                new_qs = qs.filter(time_year=year)
                export = new_qs.aggregate(Sum('value_num'))['value_num__sum']
                data['data'].append(
                    {"year": year, "export": export}
                )
            data.update({
                'rows': len(years),
                'commodity': 'All',
                'description': 'Oregon total exports in each year',
            })
        return Response(data)


class OregonExportCommodities(APIView):
    """
    List of Oregon export commodities. Choose from this list to filter the
    exports timeline.

    Example:
    /table/oregon_export_commodities/
    """

    def get(self, request, format=None):
        # Fetch metadata and region lookup tables from database if necessary
        cache_lookups()
        data = {
            'error': None,
            'description': 'List of Oregon export commodities',
            'data': []
        }
        qs = ExportsHistoricalCleaned.objects.values_list('commodity', flat=True)
        commodities = sorted(list(set(qs)))
        data['data'].extend(commodities)
        data['rows'] = len(commodities)
        return Response(data)


class ExportsTopFiveCommodities(APIView):
    """
    Top five exported commodities from Oregon in a year (default 2016, unless specified).
    """
    def get(self, request, format=None):
        cache_lookups()
        # Pick the year for the export data set
        year = request.query_params.get('year', '2016')
        data = {
            'error': None,
            'year': year,
            'description': 'Top five exported commodities from Oregon in {}'.format(year),
            'data': []
        }
        comms_qs = ExportsHistoricalCleaned.objects.values_list('commodity', flat=True)
        commodities = sorted(list(set(comms_qs)))
        qs = ExportsHistoricalCleaned.objects.filter(time_year=year)
        exports = []
        for c in commodities:
            qs_count = qs.filter(commodity=c).count()
            if qs_count == 0:
                continue
            export = float(qs.filter(commodity=c).aggregate(Sum('value_num'))['value_num__sum'])
            exports.append((export, c))
        data['data'].extend(sorted(exports, reverse=True)[:5])
        return Response(data)
