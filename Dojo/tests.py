"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from Dojo.models import *
from Dojo.forms import *
from django.contrib.auth.models import User
from datetime import date

class TestForms(TestCase):
    fixtures = ['test_Club', 'test_Person', 'test_RankRecord',
                'test_MemberRecord', 'test_PracticeRecord', 'test_Practice']
    
    def setUp(self):
        user = User.objects.create_user('tu', 't@example.com', 'tpass')
        user.is_superuser = True
        user.save()
    
    def test_add_practice_from_practice_list(self):
        
        self.client.login(username = 'tu', password = 'tpass')
        
        for club in Club.objects.all():
            url = reverse('practice_list', args = (), kwargs = {'club':club.Slug})
            resp = self.client.get(url)
            #make sure the form is the proper type
            self.assertTrue(isinstance(resp.context['form'], PracticeModelForm))
            
            resp = self.client.post(url, data = {'Date':date.today()}, 
                                    follow = True)
            
            self.assertTrue(club.practice_set.filter(Date = date.today()))
            practice = club.practice_set.get(Date = date.today())
            
            self.assertRedirects(resp, practice.get_absolute_url())    
    
    def test_practice_form_renders(self):
        landing_site = reverse('practice_form_landing')
        resp = self.client.get(reverse('home_site'))
        
        self.assertContains(resp, r'<form id="practice_form" method="post" action="%s">' % landing_site)
        
    
    def test_add_practice_from_anywhere(self):
        
        self.client.login(username = 'tu', password = 'tpass')
        landing_site = reverse('practice_form_landing')
        
        for club in Club.objects.all():
            resp = self.client.post(landing_site, data = {'Date':date.today(), 'Club':club.id}, 
                                    follow = True)
            self.assertTrue(club.practice_set.filter(Date = date.today()).exists())
            practice = club.practice_set.get(Date = date.today())
            
            self.assertRedirects(resp, practice.get_absolute_url())

    def test_add_existing_person_to_practice(self):
        
        self.client.login(username = 'tu', password = 'tpass')
        for club in Club.objects.all():
            practice = Practice(Date = date.today(),
                                Club = club)
            practice.save()
            url = practice.get_absolute_url()
            for person in Person.objects.filter(practicerecord__Practice__Club = club):
                resp = self.client.post(url, data = {'Person':person.id}, follow = True)
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            
    
        


class TestViews(TestCase):
    fixtures = ['test_Club', 'test_Person', 'test_RankRecord',
                'test_MemberRecord', 'test_PracticeRecord', 'test_Practice']

    def setUp(self):
        user = User.objects.create_user('tu', 't@example.com', 'tpass')
        user.is_superuser = True
        user.save()

    def check_login_required(self, url):

        resp = self.client.logout()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        self.client.login(username = 'tu', password = 'tpass')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        return resp


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

        for practice in Practice.objects.all():
            resp = self.check_login_required(practice.get_absolute_url())
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, practice.Club.Name)

            for person in practice.person_set.all():
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            else:
                self.assertTrue(practice.person_set.all().count() > 0)


    def test_person_list_by_club(self):

        for club in Club.objects.all():
            resp = self.client.get(reverse('person_list_by_club', args = (),
                                                kwargs = {'club':club.Slug}))

            self.assertContains(resp, club.Name)

            for person in Person.objects.filter(practicerecord__Practice__Club = club):
                self.assertContains(resp, person.Name)
                self.assertContains(resp, person.get_absolute_url())
            else:
                self.assertTrue(club.Members.all().count() > 0)
        else:
            self.assertTrue(Club.objects.all().count() > 0)

    def test_person_list(self):

        resp = self.client.get(reverse('person_list'))
        self.assertEqual(resp.status_code, 200)
        for person in Person.objects.all():
            self.assertContains(resp, person.Name)
            self.assertContains(resp, person.get_absolute_url())
        else:
            self.assertTrue(Person.objects.all().count() > 0 )


    def test_person_detail(self):

        for person in Person.objects.all():
            resp = self.check_login_required(person.get_absolute_url())
            self.assertContains(resp, person.Name)
            for club in person.club_set.all():
                self.assertContains(resp, club.Name)
                self.assertContains(resp, club.get_absolute_url())

        else:
            self.assertTrue(Person.objects.all().count() > 0 )



