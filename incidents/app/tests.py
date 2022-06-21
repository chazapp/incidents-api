import re
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import IncidentViewSet, AuthView
from django.contrib.auth.models import User

class IncidentAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@incidents.com', password='top_secret')

    def create_incident(self, incident={}):
        incident =  {
            'title': 'Test Incident',
            'description':
            'Test Incident Description',
            'status': 'Test Status',
            'severity': 'Test Severity'
        } | incident
        factory = APIRequestFactory()
        request = factory.post('/incidents', incident)
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        return response

    def test_create_incident(self):
        resp = self.create_incident()

    def test_authentication_required(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get('/auth/')
        self.assertEqual(response.status_code, 403)
        csrf = re.search(r'value="([^"]+)"', response.content.decode('utf-8')).group(1)
        print(csrf)
        response = client.post('/auth/', {'username': 'jacob@incidents.com', 'password': 'top_secret'}, content_type="application/json", headers={'X-CSRFToken': csrf})
        print(response.content)
        self.assertEqual(response.status_code, 200)
        

    def test_list_incident(self):
        factory = APIRequestFactory()
        request = factory.get('/incidents')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_incident(self):
        # Create incident...
        resp = self.create_incident()
        incident_id = resp.data['id']
        # Retrieve incident by id
        factory = APIRequestFactory()
        request = factory.get(f'/incidents/{incident_id}')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'get': 'retrieve'})(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_update_incident(self):
        # Create an incident...
        resp = self.create_incident()
        incident_id = resp.data['id']
        # Update incident by id
        factory = APIRequestFactory()
        request = factory.put(f'/incidents/{incident_id}', {
            'title': 'Test Incident',
            'description':
            'Test Incident Description',
            'status': 'Test Status',
            'severity': 'Test Severity Updated'
        })
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'put': 'update'})(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['severity'], 'Test Severity Updated')

    def test_delete_incident(self):
        # Create an incident...
        resp = self.create_incident()
        incident_id = resp.data['id']
        # Delete incident by id
        factory = APIRequestFactory()
        request = factory.delete(f'/incidents/{incident_id}')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'delete': 'destroy'})(request, pk=1)
        self.assertEqual(response.status_code, 204)

    def test_list_incident_by_status(self):
        # Create an incident...
        resp = self.create_incident()
        incident_id = resp.data['id']
        # List incident by status
        factory = APIRequestFactory()
        request = factory.get('/incidents/', query={"status": 'Test Status'})
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_list_incident_by_severity(self):
        # Create an incident...
        factory = APIRequestFactory()
        resp = self.create_incident()
        incident_id = resp.data['id']
        # List incident by severity
        request = factory.get('/incidents/', query={'severity': 'Test Severity'})
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = IncidentViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

