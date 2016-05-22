from django.contrib.auth.models import User, Group
from api.models import (
    Metadata,
    NassAnimalsSales,
    SubsidyDollars,
)
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class MetadataSerializer(serializers.HyperlinkedModelSerializer):
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
