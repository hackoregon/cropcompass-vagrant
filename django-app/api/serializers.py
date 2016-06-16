from api.models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
    SubsidyRecipients,
    NassCommodityArea,
    NassCommodityFarms,
    OainHarvestAcres,
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


class SubsidyRecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsidyRecipients
        fields = (
            'commodity',
            'year',
            'fips',
            'subsidy_recipients'
        )


class SubsidyRecipientsSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = SubsidyRecipientsSerializer(many=True)


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


class NassCommodityFarmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NassCommodityFarms
        fields = (
            'commodity',
            'year',
            'fips',
            'farms'
        )


class NassCommodityFarmsSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = NassCommodityFarmsSerializer(many=True)


class OainHarvestAcresSerializer(serializers.ModelSerializer):
    class Meta:
        model = OainHarvestAcres
        fields = (
            'commodity',
            'year',
            'fips',
            'harvested_acres'
        )


class OainHarvestAcresSerializerWrapped(serializers.Serializer):
    error = serializers.CharField(max_length=200, allow_blank=True)
    rows = serializers.IntegerField()
    data = OainHarvestAcresSerializer(many=True)
