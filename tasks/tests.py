from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_string_representation_is_title(self):
        task = Task(title="Pythonを復習する")
        self.assertEqual(str(task), "Pythonを復習する")


class TaskViewTests(TestCase):
    def test_list_page_is_displayed(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "学習ToDo")

    def test_create_task(self):
        response = self.client.post(
            reverse("tasks:list"), {"title": "Djangoを学ぶ"}
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertTrue(Task.objects.filter(title="Djangoを学ぶ").exists())

    def test_toggle_task(self):
        task = Task.objects.create(title="テストを書く")
        self.client.post(reverse("tasks:toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.is_done)

    def test_delete_task(self):
        task = Task.objects.create(title="削除する")
        self.client.post(reverse("tasks:delete", args=[task.pk]))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
