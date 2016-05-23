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

from django.core.exceptions import FieldError
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import OrderedDict
from .models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    RegionLookup,
    NassCommodityArea
)
from .serializers import (
    MetadataSerializer,
    NassAnimalsSalesSerializerWrapped,
    SubsidyDollarsSerializerWrapped,
    NassCommodityAreaSerializerWrapped
)

# Metadata dictionary of database tables keyed on the table_name. It will be
# populated by fetch_metadata() when the first view that needs it is called.
metadata_dict = {}
# Oregon region -> fips lookup dictionary.  It will be
# populated by fetch_metadata() when the first view that needs it is called.
region_to_fips = {}

METADATA_FIELDS = (
    'name',
    'description',
    'table_name',
    'unit',
    'field',
    'source_name',
    'source_link'
)


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
    Fetch region lookup table. Stores only region and fips fields in
    region_to_fips dictionary.
    """
    for region_entry in region_lookup_model.objects.all().values(
        'region',
        'fips'
    ):
        region_to_fips[region_entry['region']] = region_entry['fips']


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


class MetadataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows metadata to be viewed or edited.
    """
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer


class FilteredListView(FilteredAPIView):
    """
    Endpoint class allowing filtering by arbitrary params.

    Example 1: GET /data/nass_animals_sales/
    Returns all rows of the table in browsable API format, which is the default format, also specifiable by the query parameter "format=api".

    Example 2:
    GET /data/nass_animals_sales/?year=1997&
        commodity=Corn&year=2002&format=json
    Returns rows of Corn from 1997 and 2002 in JSON format.
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


class NassAnimalsSalesList(FilteredListView):
    """
    List animal sales.
    """
    model = NassAnimalsSales
    serializer = NassAnimalsSalesSerializerWrapped


class SubsidyDollarsList(FilteredListView):
    """
    List subsidy dollars, optionally filtered on commodity and/or year.
    """
    model = SubsidyDollars
    serializer = SubsidyDollarsSerializerWrapped


class NassCommodityAreaList(FilteredListView):
    """
    List commodities with area. Exclude rows where acres == null
    """
    model = NassCommodityArea
    serializer = NassCommodityAreaSerializerWrapped
    queryset = model.objects.filter(acres__isnull=False)


# class TableView(APIView):
#     @staticmethod
#     def prepare_data(query, fields=(), **kwargs):
#         """ Retrieve specific data from queryset """
#         from django.db.models import QuerySet
#         assert isinstance(query, QuerySet)
#
#         data = query.values(*fields)
#
#         if kwargs.get('unique', False):
#             pass
#
#         return data


class SubsidyDollarsTable(APIView):
    """
    Table of (commodity -> subsidy dollars) for Oregon or selected county.
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
        if not metadata_dict:
            fetch_metadata(Metadata)
        if not region_to_fips:
            fetch_region_lookup(RegionLookup)
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
                fips=region_to_fips[county])
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


class CommodityAreaTable(APIView):
    """
    Table of (commodity -> area) for Oregon or selected county.
    """
    @staticmethod
    def fill_in_data(query, data_array):
        """Populate data array from the query"""
        for row in query:
            data_array['data'].append({
                'commodity': row.commodity,
                'acres': row.acres
            })

        commodity_list = []
        for item in data_array['data']:
            commodity_list.append(item['commodity'])

        commodity_list = set(commodity_list)
        tempdata = []

        for commodity in commodity_list:
            acres = [item['acres'] for item in data_array['data'] if item['commodity'] == commodity]
            tempdata.append({
                'commodity': commodity,
                'acres': sum(acres)
            })

        data_array['data'] = tempdata

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
        if not metadata_dict:
            fetch_metadata(Metadata)
        if not region_to_fips:
            fetch_region_lookup(RegionLookup)
        # Get the most recent year for subsidy dollars
        latest_year = get_most_recent_year(NassCommodityArea)
        data = {
            'error': None,
            'unit': "acres",
            'year': latest_year,
            'description': 'Commodity area for each commodity in {}',
            'data': []
        }
        # If a county has been selected in the query parameters
        if 'county' in request.query_params:
            county = request.query_params['county']
            commodity_area = NassCommodityArea.objects.filter(
                year=latest_year,
                fips=region_to_fips[county],
                acres__isnull=False
                )
            data['description'] = data['description'].format(county) + ' County'
            data.update({
                'rows': commodity_area.distinct("commodity").count(),
                'region': county,
            })
            self.fill_in_data(commodity_area, data)
        # If no county is specified, return Oregon total acreas
        else:
            commodity_area = NassCommodityArea.objects.filter(
                year=latest_year,
                fips__startswith=41,
                acres__isnull=False)
            data['description'] = data['description'].format('Oregon')
            data.update({
                'rows': commodity_area.distinct("commodity").count(),
                'region': 'Oregon (Statewide)',
            })
            self.fill_in_data(commodity_area, data)
        return Response(data)
