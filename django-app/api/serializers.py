from api.models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    NassCommodityArea
)
from rest_framework import serializers


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = (
            'name',
            'description',
            'table_name',
            'unit',
            'field',
            'source_name',
            'source_link'
        )


class MetadataSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = MetadataSerializer(many=True)


class NassAnimalsSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NassAnimalsSales
        fields = (
            'commodity',
            'year',
            'fips',
            'animals'
        )


class NassAnimalsSalesSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = NassAnimalsSalesSerializer(many=True)


class SubsidyDollarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsidyDollars
        fields = (
            'commodity',
            'year',
            'fips',
            'subsidy_dollars'
        )


class SubsidyDollarsSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = SubsidyDollarsSerializer(many=True)


class NassCommodityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NassCommodityArea
        fields = (
            'commodity',
            'year',
            'fips',
            'acres'
        )


class NassCommodityAreaSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = NassCommodityAreaSerializer(many=True)
