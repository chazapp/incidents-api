from datetime import datetime, timezone
import json
from django import http
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics, views, filters
from rest_framework.pagination import LimitOffsetPagination
from incidents.app.serializers import UserSerializer, GroupSerializer
from incidents.app.models import Incident
from incidents.app.serializers import IncidentSerializer



@method_decorator(ensure_csrf_cookie, 'dispatch')
class AuthView(View):
    def get(self, request):
        if not request.user.is_authenticated:
          resp = render(request, 'login.html', status=403)
          resp['WWW-Authenticate'] = ''
          return resp
        return render(request, 'login.html', status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "id": user.pk,
                    "username": user.get_username(),
                })
            return http.JsonResponse({"message": "invalid credentials"}, status=400)
        except Exception as e:
            return http.JsonResponse({"message": "invalid supplied data"}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows incidents to be viewed or edited.
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title', 'description']
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination

    @property
    def default_response_headers(self):
        headers = viewsets.ModelViewSet.default_response_headers.fget(self)
        headers['WWW-Authenticate'] = ''
        return headers

class MetricsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
        This method returns PromQL metrics of the Incident database.
    """
    def get(self, request):
        # TODO Uptime metric ? 
        total_incidents = Incident.objects.count()
        if total_incidents > 0:
            latest_incident = Incident.objects.latest('created_at')
            days_without_incidents = (datetime.now(timezone.utc) - latest_incident.created_at).days
        else:
            days_without_incidents = "NaN"
        metrics = f"""\
total_incidents{{job="incidents"}} {total_incidents}
days_without_incidents{{job="incidents"}} {days_without_incidents}
"""
        return HttpResponse(metrics, content_type='text/plain')


class HealthAPIView(views.APIView):
    """
        This method returns health check metrics
    """
    def get(self, request):
        return HttpResponse('OK', content_type='text/plain')
