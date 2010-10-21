"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from Dojo.models import *

class TestViews(TestCase):
    fixtures = ['test_Club', 'test_Person', 'test_RankRecord',
                'test_MemberRecord', 'test_PracticeRecord']

    def test_home(self):

        resp = self.client.get(reverse('home_site'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Home')

    def test_club_list(self):

        resp = self.client.get(reverse('club_list'))
        self.assertEqual(resp.status_code, 200)
        for club in Club.objects.all():
            self.assertContains(resp, club.Name)
            self.assertContains(resp, club.get_absolute_url())
        else:
            self.assertTrue(Club.objects.all().count() > 0)

    def test_club_detail(self):

        for club in Club.objects.all():
            resp = self.client.get(club.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

            for person in Person.objects.filter(practicerecord__Practice__Club = club):
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            else:
                self.assertTrue(club.Members.all().count() > 0)



