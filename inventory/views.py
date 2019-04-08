# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from inventory.serializers import BoxSerializer, BoxGetSerializer
from inventory.serializers import BoxStaffGetSerializer
from inventory.models import Box

class StaffUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, and is staff user
    or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.method in permissions.SAFE_METHODS) or
            (request.user and
            request.user.is_staff)
        )

class BoxFilter(filters.FilterSet):
    min_length = filters.NumberFilter(field_name="length", lookup_expr='gt')
    max_length = filters.NumberFilter(field_name="length", lookup_expr='lt')
    min_breadth = filters.NumberFilter(field_name="breadth", lookup_expr='gt')
    max_breadth = filters.NumberFilter(field_name="breadth", lookup_expr='lt')
    min_height = filters.NumberFilter(field_name="height", lookup_expr='gt')
    max_height = filters.NumberFilter(field_name="height", lookup_expr='lt')
    min_area = filters.NumberFilter(field_name="area", lookup_expr='gt')
    max_area = filters.NumberFilter(field_name="area", lookup_expr='lt')
    min_volume = filters.NumberFilter(field_name="volume", lookup_expr='gt')
    max_volume = filters.NumberFilter(field_name="volume", lookup_expr='lt')
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr='lt')
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr='gt')
    username = filters.CharFilter(field_name="created_by", lookup_expr="username")

    class Meta:
        model = Box
        fields = ['length', 'min_length', 'max_length',
        'breadth', 'min_breadth', 'max_breadth',
        'height', 'min_height', 'max_height',
        'area', 'min_area', 'max_area',
        'volume', 'min_volume', 'max_volume',
        'created_at', 'created_before', 'created_after',
        'created_by', 'username']

class BoxViewSets(viewsets.ModelViewSet):
    serializer_class = BoxGetSerializer
    queryset = Box.objects.all()
    permission_classes = (StaffUserOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BoxFilter

    def get_serializer_class(self, *args, **kwargs):
        serializer = BoxGetSerializer
        if self.request.method in ['POST', 'PATCH']:
            serializer = BoxSerializer
        if self.request.user.is_staff:
            serializer = BoxStaffGetSerializer
        return serializer

    def get_queryset(self, *args, **kwargs):
        if self.action == 'list' and self.request.GET.get("my_boxes") == "1":
            self.queryset = self.queryset.filter(created_by=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by": request.user.id})
        print(request.data)
        return super(BoxViewSets, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("created_by"):
            # remove created_by oberride
            request.data.pop("created_by")
        return super(BoxViewSets, self).partial_update(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):
        if request.GET.get("my_boxes") == "1":
            if request.user.is_staff is False:
                return Response(
                    {"error": "Only staff user are allowed to see their boxes"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return super(BoxViewSets, self).list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.id == self.get_object().created_by.id:
            return super(BoxViewSets, self).delete(request, *args, **kwargs)
        return Response(
            {"error": "You can only delete boxes created by You"},
            status=status.HTTP_401_UNAUTHORIZED
        )
