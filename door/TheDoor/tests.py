from django.test import TestCase
from django.shortcuts import reverse

class UrlTests(TestCase):
    def test_homePage(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
    
   # def test_homeURL(self):
    #    response = self.client.get(reverse("dashboard"))
     #   self.assertEquals(response.status_code, 200)