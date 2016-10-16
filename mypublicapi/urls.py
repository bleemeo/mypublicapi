"""mypublicapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import django_filters 


from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import (
    decorators, filters, response, routers, serializers, status, viewsets
)
from rest_framework_jwt import views as jwt_views 

from mypublicapi.models import Metric, Server, ServerProperty


# http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
# http://stackoverflow.com/a/23674297
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if 'request' in self.context:
            fields = self.context['request'].query_params.get('fields')
            if fields:
                fields = fields.split(',')
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class ServerPropertySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = ServerProperty
        fields = ('name', 'value')


class MetricFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
         model = Metric


class ServerSerializer(DynamicFieldsModelSerializer):

    properties = ServerPropertySerializer(
        source='serverproperty_set', many=True
    )

    class Meta:
        model = Server
        fields = ('id', 'name', 'properties')

    def create(self, validated_data):
        properties = validated_data.pop('serverproperty_set')
        server = super(ServerSerializer, self).create(validated_data)

        for prop in properties:
            ServerProperty.objects.create(
                server=server,
                **prop
            )

        return server

    def update(self, instance, validated_data):
        if 'serverproperty_set' in validated_data:
            properties = validated_data.pop('serverproperty_set')

            instance.serverproperty_set.all().delete()
            for prop in properties:
                ServerProperty.objects.create(
                    server=instance,
                    **prop
                )

        return super(ServerSerializer, self).update(instance, validated_data)


class ServerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
         model = Server


class ServerViewSet(viewsets.ModelViewSet):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter
    search_fields = ('name', 'serverproperty__value')


class MetricSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Metric
        fields = ('id', 'name')


class MetricFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
         model = Metric


class MetricViewSet(viewsets.ModelViewSet):

    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    filter_class = MetricFilter
    search_fields = ('name', 'server__name')


router = routers.DefaultRouter()
router.register(r'server', ServerViewSet)
router.register(r'metric', MetricViewSet)



urlpatterns = [

    # API
    url(r'^v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #    url(r'^api-token-auth/', 'rest_framework.views.obtain_auth_token'),
    url(r'^v1/jwt-auth/', jwt_views.obtain_jwt_token),
    url(r'^v1/jwt-refresh/', jwt_views.refresh_jwt_token),

    url(r'^admin/', admin.site.urls),
]
