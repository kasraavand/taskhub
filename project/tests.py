from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from project.models import Project
from project.serializers import ProjectSerializer
import json



User = get_user_model()



class ProjectListCreateAPIViewTestCase(APITestCase):
    url = reverse("project:projects")
    
    def setUp(self):
        self.username = "manager_01"
        self.email = "manager_01@cool.com"
        self.password = "some_random_pass"
        self.user = User.objects.create_user(self.username, self.email, self.password, role="manager")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_create_project(self):
        response = self.client.post(self.url, {"name": "Some random project!"})
        self.assertEqual(201, response.status_code)

    def test_create_project_fake(self):
        "test to create project with none manager user"
        
        self.user = User.objects.create_user("fakemanager_02", "fakemanager_02@test.com", "samlep_pass")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        try:
            self.client.post(self.url, {"name": "new random project!"})
        except ValueError:
            pass
        else:
            raise Exception("project creation worked with fake manager")

    def test_get_projects_for_manager(self):
        """
        Test to verify manager projects list
        """
        Project.objects.create(manager=self.user, name="Project No 0001")
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == Project.objects.count())

    def test_get_projects_for_developer(self):
        """
        Test to verify developer projects list
        """
        project = Project.objects.create(manager=self.user, name="Project No 0003")
        self.user = User.objects.create_user("dev_user", "test@dev.com", "sample_pass")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        project.developers.add(self.user)
        response = self.client.get(self.url)
        _projects = response.json()
        self.assertTrue(any(devs['username']=="dev_user" for p in _projects for devs in p['developers']))


class TaskDetailAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.username = "manager_01"
        self.email = "manager_01@cool.com"
        self.password = "some_random_pass"
        self.user = User.objects.create_user(self.username, self.email, self.password, role="manager")
        self.project = Project.objects.create(manager=self.user, name="Project No 0001")
        self.token = Token.objects.create(user=self.user)
        self.url = reverse("project:project_detail", kwargs={"pk": self.project.name})
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_assigning_developers(self):
        # self.assertTrue()
        response = self.client.put(
            self.url,
            {"name": self.project.name,
             "developers":[
                {"username": "random_user0", "email":"randomMail@sample.com", "password":"randompass"},
                {"username": "random_user1", "email":"randomMail1@sample.com", "password":"randompass"}
            ]},
            format='json'
        )

        dev_data = {d["username"] for d in response.json().get("developers")}
        self.assertTrue(all(i in dev_data for i in ["random_user0", "random_user1"]))