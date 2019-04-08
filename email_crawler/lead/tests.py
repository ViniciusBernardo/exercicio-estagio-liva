from django import test
from rest_framework import status
from rest_framework.test import APIClient
from .models import Lead


class EmailCrawlerEndpointsTest(test.TestCase):

    def setUp(self):
        self.api_client_test = APIClient()

    def test_get_specify_from_email(self):
        response = self.api_client_test.get(
            '/api/lead/lead-viewset/search_leads/?from=a@mail.com',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'found 0 leads'})

    def test_get_specify_subject(self):
        response = self.api_client_test.get(
            '/api/lead/lead-viewset/search_leads/?subject=ola%20mundo',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'found 0 leads'})

    def test_get_without_specify_from_or_subject(self):
        response = self.api_client_test.get(
            '/api/lead/lead-viewset/search_leads/',
        )

        leads = Lead.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(leads) > 0)
        self.assertEqual(
            response.data,
            {'detail': 'found {} leads'.format(len(leads))}
        )
