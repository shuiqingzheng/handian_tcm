from rest_framework import serializers

from tcm.models import TCM, Literature, HandianProduct


class TcmSerializer(serializers.ModelSerializer):

    class Meta:
        model = TCM
        exclude = ('id', )


class LiteratureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Literature
        exclude = ('id', )


class LiteratureByProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Literature
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'literature-detail', 'lookup_field': 'neo_id'},
        }


class HandianProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='neo_id')

    class Meta:
        model = HandianProduct
        exclude = ('id', )
        # fields = '__all__'
