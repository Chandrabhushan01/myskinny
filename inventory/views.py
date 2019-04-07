# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from inventory.serializers import BoxSerializer
from inventory.models import Box

class StaffUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, and is staff user
    or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class BoxViewSets(viewsets.ModelViewSet):
    serializer_class = BoxSerializer
    queryset = Box.objects.all()
    permission_classes = (StaffUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'length', 'breadth', 'height', 'area', 'volume',
        'created_at', 'create_by'
    )

    def get_queryset(self, *args, **kwargs):
        if self.action == 'list' and self.request.get("my_boxes") == "1":
            self.queryset = self.queryset.filter(create_by=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data.update({"create_by": request.user.id})
        return super(BoxViewSets, self).create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("create_by"):
            # remove create_by oberride
            request.data.pop("create_by")
        return super(BoxViewSets, self).partial_update(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):
        if request.get("my_boxes") == "1":
            if request.user.is_staff is False:
                return Response(
                    {"error": "Only staff user are allowed to see their boxes"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return super(BoxViewSets, self).list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.id == self.get_object().create_by.id:
            return super(BoxViewSets, self).delete(request, *args, **kwargs)
        return Response(
            {"error": "You can only delete boxes created by You"},
            status=status.HTTP_401_UNAUTHORIZED
        )
