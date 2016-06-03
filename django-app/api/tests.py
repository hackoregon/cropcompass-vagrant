from django.test import RequestFactory, TestCase
from django.http import QueryDict
from .models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    RegionLookup,
    MetadataTest,
    SubsidyDollarsTest,
    RegionLookupTest,
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


class TestViewHelperFunctions(TestCase):
    @classmethod
    def setUpClass(cls):
        # A test metadata database entry
        MetadataTest.objects.create(
            **dict(zip(METADATA_FIELDS, METADATA_FIELDS)))
        # A few region lookup table entries
        regions = ['Amazon', 'Mordor', 'Pluto', 'Gotham']
        fips = [90202, 11235, 60001, 291]
        region_lookup_list = [
            RegionLookupTest(region=r, fips=f) for r, f in zip(regions, fips)
        ]
        RegionLookupTest.objects.bulk_create(region_lookup_list)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_fetch_metadata_retrieves_all_rows_from_table(self):
        fetch_metadata(MetadataTest)
        self.assertEqual(MetadataTest.objects.count(), len(metadata_dict))

    def test_fetch_metadata_retrieves_correct_values(self):
        fetch_metadata(MetadataTest)
        metadata = MetadataTest.objects.first()
        table_name = metadata.table_name
        self.assertIn(table_name, metadata_dict)
        for field in METADATA_FIELDS:
            self.assertEqual(
                getattr(metadata, field),
                metadata_dict[table_name][field]
            )

    def test_get_most_recent_year(self):
        # A few SubsidyDollarsTest entries
        subsidy_dollars_list = [
            SubsidyDollarsTest(year=year) for year in (1997, 2000, 2013, 2015)
        ]
        SubsidyDollarsTest.objects.bulk_create(subsidy_dollars_list)
        self.assertEqual(2015, get_most_recent_year(SubsidyDollarsTest))

    def test_fetch_region_lookup_retrieves_all_rows(self):
        fetch_region_lookup(RegionLookupTest)
        self.assertEqual(RegionLookupTest.objects.count(), len(region_to_fips))

    def test_fetch_region_lookup_generates_correct_values(self):
        fetch_region_lookup(RegionLookupTest)
        for region_lookup in RegionLookupTest.objects.all():
            self.assertIn(region_lookup.region, region_to_fips)
            self.assertEqual(
                region_lookup.fips,
                region_to_fips[region_lookup.region]
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
