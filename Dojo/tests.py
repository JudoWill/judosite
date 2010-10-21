"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from Dojo.models import *
from django.contrib.auth.models import User

class TestViews(TestCase):
    fixtures = ['test_Club', 'test_Person', 'test_RankRecord',
                'test_MemberRecord', 'test_PracticeRecord', 'test_Practice']

    def setUp(self):
        user = User.objects.create_user('tu', 't@example.com', 'tpass')
        user.save()


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
            self.assertContains(resp, club.Name)
            for person in Person.objects.filter(practicerecord__Practice__Club = club):
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            else:
                self.assertTrue(club.Members.all().count() > 0)

    def test_practice_list(self):

        for club in Club.objects.all():
            resp = self.client.get(reverse('practice_list', kwargs = {'club':club}))
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, club.Name)

            for practice in Practice.objects.filter(Club = club):
                self.assertContains(resp, practice.get_absolute_url())
            else:
                self.assertTrue(Practice.objects.filter(Club = club).count() > 0)


    def test_practice_detail(self):
        self.client.login(username = 'tu', password = 'tpass')
        for practice in Practice.objects.all():
            print practice.get_absolute_url()
            resp = self.client.get(practice.get_absolute_url())
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, practice.Club.Name)

            for person in practice.person_set.all():
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            else:
                self.assertTrue(practice.person_set.all().count() > 0)


