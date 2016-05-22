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
from django.db.models import Max
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import OrderedDict
from .models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    RegionLookup
)
from .serializers import (
    MetadataSerializer,
    NassAnimalsSalesSerializerWrapped,
    SubsidyDollarsSerializerWrapped,
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
        return model.objects.all().aggregate(Max('year'))['year__max']
    except AttributeError:  # model does not exist
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


class NassAnimalsSalesList(FilteredAPIView):
    """
    List animal sales.
    """
    def get(self, request, format=None):
        """List animal sales with optional filtering from nass_animals_sales.

        Example 1: GET /data/nass_animals_sales/
        Returns all rows of the table in browsable API format, which is the default format, also specifiable by the query parameter "format=api".

        Example 2:
        GET /data/nass_animals_sales/?year=1997&
            commodity=Corn&year=2002&format=json
        Returns rows of Corn from 1997 and 2002 in JSON format.
        """
        # Accepted fields for filtering output
        FILTER_FIELDS = ['commodity', 'year']
        if request.query_params:
            # Generate query filter dictionary
            query = self.query_dict(request.query_params, FILTER_FIELDS)
            # Generate queryset
            animal_sales = NassAnimalsSales.objects.filter(**query)
        else:
            animal_sales = NassAnimalsSales.objects.all()
        serializer = NassAnimalsSalesSerializerWrapped({
            "error": None,
            "rows": animal_sales.count(),
            "data": animal_sales
        })
        return Response(serializer.data)


class SubsidyDollarsList(FilteredAPIView):
    """
    List subsidy dollars, optionally filtered on commodity and/or year.
    """
    def get(self, request, format=None):
        """List subsidy dollars with optional filtering from subsidy_dollars.

        Example 1: GET /data/subsidy_dollars/
        Returns all rows of the table in browsable API format, which is the default format, also specifiable by the query parameter "format=api".

        Example 2:
        GET /data/subsidy_dollars/?year=1997&
            commodity=Corn&format=json
        Returns rows of Corn from 1997 in JSON format.
        """
        # Accepted fields for filtering output
        FILTER_FIELDS = ['commodity', 'year']
        if request.query_params:
            # Generate query filter dictionary
            query = self.query_dict(request.query_params, FILTER_FIELDS)
            # Generate queryset
            subsidy_dollars = SubsidyDollars.objects.filter(**query)
        else:
            subsidy_dollars = SubsidyDollars.objects.all()
        serializer = SubsidyDollarsSerializerWrapped({
            "error": None,
            "rows": subsidy_dollars.count(),
            "data": subsidy_dollars
        })
        return Response(serializer.data)


class SubsidyDollarsTable(APIView):
    """
    Table of (commodity -> subsidy dollars) for Oregon or selected county.
    """
    @staticmethod
    def fill_in_data(query, data_array):
        """Populate data array from the query"""
        for row in query:
            data_array['data'].append({
                'commodity': row.commodity,
                'subsidy_dollars': row.subsidy_dollars
            })

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
            self.fill_in_data(subsidy_dollars, data)
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
            self.fill_in_data(subsidy_dollars, data)
        return Response(data)
