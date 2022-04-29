from pickle import FALSE
from sre_constants import FAILURE, SUCCESS
from unittest.result import failfast
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import login, authenticate, logout
from .views import *

# Used for signup tests later
def valid_signup(username, pass1, pass2, fname, lname):
    if not username.isalnum():
        return False
    if (not is_special_character(pass1)) or len(pass1) <= 8:
        return False
    if (not fname.isalpha()) or (not lname.isalpha()):
        return False
    if pass1 != pass2:
        return False
    return True


# Tests various Urls from our page
class UrlTests(TestCase):
    # Should pass because this is default page
    def test_homePage(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    # Should Fail because you need to have an account before going to dashboard
    def test_homeURL(self):
        response = self.client.get("dashboard")
        self.assertEquals(response.status_code, 200)


# Tests different cases of login
class loginTests(TestCase):

    # Should Pass because admin1 is in system
    def test_loginAdmin1(self):
        if authenticate(username="admin1", password="Jason123!") is not None:
            return SUCCESS
        return FAILURE

    # Should Fail, username has incorrect characters, password does not meet requirements
    def test_loginUser(self):
        assert authenticate(username="{user@,", password="j") is not None


# Tests different inputs for sign up
class signupTests(TestCase):
    def test_signup1(self):
        # Should Pass, all info is correct
        self.assertEquals(
            valid_signup("jk1834", "Wtge0897", "Wtge0897", "Bob", "Smith"), False
        )

    def test_signup2(self):
        # Should fail because password does not meet requirements
        self.assertEquals(valid_signup("jk1834", "k", "j", "Bob", "Smith"), True)


class PostTest(TestCase):
    def test_Post(self):
        assert authenticate(related_name="posts") is not None

