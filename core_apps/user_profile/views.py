from typing import Any, List
from rest_framework.views import APIView

from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, generics
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.request import Request

from core_apps.common.models import ContentView
from core_apps.common.permissions import IsBranchManager
from core_apps.common.renderers import GenericJSONRenderer
from .models import NextOfKin, Profile
from .serializers import NextOfKinSerializer, ProfileListSerializer, ProfileSerializer



class ProfileDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    renderer_classes = [GenericJSONRenderer]
    object_label = "profile"

    def get_object(self) -> Profile:
        try:
            profile = Profile.objects.get(user=self.request.user)
            self.record_profile_view(profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")

    def record_profile_view(self, profile: Profile) -> None:
        content_type = ContentType.objects.get_for_model(profile)
        viewer_ip = self.get_client_ip()
        user = self.request.user

        ContentView.objects.update_or_create(
            content_type=content_type,
            object_id=profile.id,
            user=user,
            viewer_ip=viewer_ip,
            defaults={
                "last_viewed": timezone.now(),
            },
        )

    def get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)
    
    def _update(self, request: Request, partial: bool) -> Response:
        instance = self.get_object()
        serializer = ProfileSerializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self._update(request, partial=False)

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self._update(request, partial=True)
    
