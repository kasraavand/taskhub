import json
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from tasks.models import Task
from tasks.serializers import taskserializer
from project.models import Project
from project.serializers import ProjectSerializer
from django.contrib.auth import get_user_model



User = get_user_model()



class TaskListCreateAPIViewTestCase(APITestCase):
    url = reverse("tasks:list")
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password, role="dev")
        self.manager = User.objects.create_user("manager_user", "test@manager.com", "sample_pass", role="manager")
        self.project = Project.objects.create(manager=self.manager, name="Project No 0003")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()


    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_create_todo(self):
        response = self.client.post(self.url, {"project":self.project.name, "name": "Some random task!"})
        self.assertEqual(201, response.status_code)

    def test_developer_task(self):
        """
        Test to verify if developers can get the list of the tasks they have along with
        other devs with whom they share a project.
        """
        Task.objects.create(user=self.user, project=self.project, name="Clean up your room!")
        self.user = User.objects.create_user("dev_user02", "dev_user02@test.com", "sample_pass", role="dev")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.project.developers.add(self.user)
        Task.objects.create(user=self.user, project=self.project, name="Clean up your room 02!")
        
        response = self.client.get(self.url)
        self.assertTrue(
            len(response.json()) == Task.objects.count()
            )



class TaskDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        _manager = User.objects.create_user("manger_001", "manger_001@test.com", "test_password", role="manager")
        _project = Project.objects.create(manager=_manager, name="Project No 0001")
        self.todo = Task.objects.create(user=self.user, project=_project, name="Call Me!")
        self.url = reverse("tasks:detail", kwargs={"pk": self.todo.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_todo_object_bundle(self):
        """
        Test to verify todo object bundle
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        todo_serializer_data = taskserializer(instance=self.todo).data
        response_data = json.loads(response.content)
        self.assertEqual(todo_serializer_data, response_data)

    def test_todo_object_update_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        response = self.client.put(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

        # HTTP PATCH
        response = self.client.patch(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

    def test_todo_object_update(self):
        _manager = User.objects.create_user("manger_002", "manger_002@test.com", "test_password", role="manager")
        _project = Project.objects.create(manager=_manager, name="Project No 0002")
        response = self.client.put(self.url, {"project":_project.name, "name": "Call you!"})
        response_data = response.json()
        todo = Task.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get("name"), todo.name)

    def test_todo_object_partial_update(self):

        response = self.client.patch(self.url, {"done": True})
        response_data = response.json()
        todo = Task.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get("done"), todo.done)

    def test_todo_object_delete_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_todo_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
