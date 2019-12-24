from django.conf import settings
from rest_framework import serializers

from tcm.models import (
    TCM, Literature, HandianProduct, Prescription, XingWei, Term
)


class TcmSerializer(serializers.ModelSerializer):

    class Meta:
        model = TCM
        exclude = ('id', )


class TcmUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = TCM
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'tcm-detail', 'lookup_field': 'neo_id'},
        }


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
    pic_url = serializers.SerializerMethodField()

    class Meta:
        model = HandianProduct
        fields = ('neo_id', 'url', 'is_show', 'name', 'pic_url')

    def get_pic_url(self, obj):
        if not obj.pic_url:
            return None

        nginx_url = ':'.join([settings.NGINX_SERVER, str(settings.NGINX_PORT)])
        pic_url = '/'.join([nginx_url, settings.MEDIA_ROOT, str(obj.pic_url)])
        return pic_url


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        exclude = ('id',)


class PrescriptionUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'prescription-detail', 'lookup_field': 'neo_id'},
        }


class XingWeiSerializer(serializers.ModelSerializer):

    class Meta:
        model = XingWei
        exclude = ('id', )


class TermUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Term
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'term-detail', 'lookup_field': 'neo_id'},
        }


class TermSerializer(serializers.ModelSerializer):

    class Meta:
        model = Term
        exclude = ('id', )
