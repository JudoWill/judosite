"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from Dojo.models import *

class TestViews(TestCase):
    fixtures = ['test_Club', 'test_Person', 'test_RankRecord']

    def test_home(self):

        resp = self.client.get(reverse('home_site'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Home')

    def test_club_list(self):

        resp = self.client.get(reverse('club_list'))
        self.assertEqual(resp.status_code, 200)
        for club in Club.objects.all():
            self.assertContains(resp, club.Name)
        else:
            self.assertTrue(Club.objects.all().count() > 0)

