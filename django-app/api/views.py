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
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    SubsidyRecipients,
    RegionLookup,
    NassCommodityArea,
    NassCommodityFarms,
    OainHarvestAcres,
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
    for region_entry in region_lookup_model.objects.values(
        'region',
        'fips'
    ):
        region_to_fips[region_entry['region']] = region_entry['fips']
        fips_to_region[region_entry['fips']] = region_entry['region']


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
            ('List commodities by area - row view', 'nass_commodity_area_list'),
            ('List commodities by area - table view', 'nass_commodity_area_table'),
            ('List commodities by number of farms - row view', 'nass_commodity_farms_list'),
            ('List commodities by harvested acres - row view', 'oain_harvest_acres_list'),
            ('List animal sales - row view', 'nass_animals_sales'),
            ('Subsidy Dollars - row view', 'subsidy_dollars_data'),
            ('Subsidy Dollars - table view', 'subsidy_dollars_table'),
            ('Subsidy Dollars - top 5 counties', 'subsidy_dollars_top_counties'),
            ('Subsidy Dollars - top 5 commodities', 'subsidy_dollars_top_commodities'),
            ('Subsidy Recipients - row view', 'subsidy_recipients_data'),
        ]
        endpoint_dict = OrderedDict()
        for endpoint_name, path in endpoints:
            endpoint_dict[endpoint_name] = api_reverse(path, request=request)
        return Response(endpoint_dict)


class FilteredListView(FilteredAPIView):
    """
    Endpoint class allowing filtering by arbitrary params.
    """
    filter_fields = ['commodity', 'year']
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
            qs = qs.filter(fips=region_to_fips[county])
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
    List subsidy dollars, optionally filtered on commodity and/or year.

    By default all data in the table is returned, row-wise. Filtered results by year, and commodity may be specified by providing query parameters

    Example filtering: "?year=2012&year=2003&commodity=Tree" to get Tree data for both 2012 and 2003.
    """
    model = SubsidyDollars
    serializer = SubsidyDollarsSerializerWrapped


class SubsidyDollarsTable(APIView):
    """
    Table of county or Oregon state (commodity -> subsidy
    dollars) for the most recent year for which data is available in the DB.
    (Section E)

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
        """Return table of county or Oregon state (commodity -> subsidy
        dollars) for the most recent year for which data is available.

        Example 1: GET /table/subsidy_dollars/?format=json
        Returns the table (commodity -> subsidy dollars) for all of Oregon
        in JSON format.

        Example 2: GET /table/subsidy_dollars/?county=Linn&format=json
        Returns the table (commodity -> subsidy dollars) for Linn County
        in JSON format.

        Selecting a commodity or a year has no effect on the returned
        subsidy data.

        Use format=api or no query parameter to get browsable api results.
        """
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
                fips=region_to_fips[county.capitalize()])
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


class SubsidyDollarsTopFiveCounties(APIView):
    """
    Top five counties plus Oregon (statewide) subsidy summed over all
    commodities. (Section E)
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
            region = fips_to_region[subs.fips]
            subs_c[region] = subs_c.get(region, 0) + subs.subsidy_dollars
        top_six_comm = dict(subs_c.most_common(6))
        data['data'].append(top_six_comm)
        return Response(data)


class SubsidyDollarsTopFiveCommodities(APIView):
    """
    Top five commodities subsidy summed over all counties. (Section D)
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


class SubsidyRecipientsList(FilteredListView):
    """
    List subsidy recipients, optionally filtered on commodity and/or year.

    By default all data in the table is returned, row-wise. Filtered results by year, and commodity may be specified by providing query parameters

    Example filtering: "?year=2012&year=2003&commodity=Tree" to get Tree data for both 2012 and 2003.
    """
    model = SubsidyRecipients
    serializer = SubsidyRecipientsSerializerWrapped
