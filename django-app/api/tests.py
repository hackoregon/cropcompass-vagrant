from django.test import RequestFactory, TestCase
from django.http import QueryDict
from .models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    RegionLookup,
)
from .views import (
    METADATA_FIELDS,
    metadata_dict,
    region_to_fips,
    fetch_metadata,
    get_most_recent_year,
    fetch_region_lookup,
    FilteredAPIView,
    SubsidyDollarsList,
    SubsidyDollarsTable
)


class TestFilteredAPIView(TestCase):

    def setUp(self):
        self.qry_string1 = "bob=sled&format=json&bob=goat"
        self.qry_string2 = "bob=sled&cat=goat"
        self.filters = ['cat', 'bob', 'bobcat']

    def test_query_dict_excludes_format(self):
        qry_params = QueryDict(self.qry_string1)
        query = FilteredAPIView.query_dict(qry_params, self.filters)
        self.assertNotIn('filter__in', query)

    def test_query_dict_contains_filter_multiple_values(self):
        qry_params = QueryDict(self.qry_string1)
        query = FilteredAPIView.query_dict(qry_params, self.filters)
        self.assertIn('bob__in', query)
        self.assertListEqual(['sled', 'goat'], query['bob__in'])

    def test_query_dict_contains_filter_single_values(self):
        qry_params = QueryDict(self.qry_string2)
        query = FilteredAPIView.query_dict(qry_params, self.filters)
        self.assertIn('bob__in', query)
        self.assertListEqual(['sled'], query['bob__in'])
        self.assertIn('cat__in', query)
        self.assertListEqual(['goat'], query['cat__in'])

    def test_query_dict_excludes_unmatched_filters(self):
        qry_params = QueryDict(self.qry_string1)
        query = FilteredAPIView.query_dict(qry_params, self.filters)
        self.assertNotIn('cat__in', query)
        self.assertNotIn('bobcat__in', query)


class BaseViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()


class TestSubsidyDollarsList(BaseViewTestCase):

    def setUp(self):
        # Call BaseViewTestCase.setUp()
        super(TestFilteredAPIView, self).setUp()
