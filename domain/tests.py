# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class AuthAPITestCase(APITestCase):
    fixtures = ["writers.json", "articles.json"]

    def setUp(self):
        self.client = APIClient()
        self.editor_user = User.objects.filter(username="editor_user").first()
        self.writer_user = User.objects.filter(username="writer_user").first()

    def force_login_editor(self):
        self.client.force_login(user=self.editor_user)

    def force_login_writer(self):
        self.client.force_login(user=self.writer_user)


class DashboardAPITestCase(AuthAPITestCase):

    def test_dashboard_api(self):
        url = reverse("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)


class ArticleCreateAPITestCase(AuthAPITestCase):

    def test_article_create_api_not_authenticated(self):
        url = reverse("article-create")
        data = {
            "title": "New Test Article",
            "content": "New Test content",
            "status": "draft",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_create_api(self):
        self.force_login_editor()
        url = reverse("article-create")
        data = {
            "title": "New Test Article",
            "content": "New Test content",
            "status": "draft",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("id"), 7)
        self.assertEqual(response.data.get("title"), data.get("title"))
        self.assertEqual(response.data.get("content"), data.get("content"))
        self.assertEqual(response.data.get("status"), data.get("status"))

    def test_article_create_api_bad(self):
        self.force_login_editor()
        url = reverse("article-create")
        data = {"title": "New Test Article"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPITestCase(AuthAPITestCase):

    def test_get_article_detail_api(self):
        url = reverse("article-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Article 1")

    def test_get_article_detail_api_not_found(self):
        url = reverse("article-detail", args=[99])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article_detail_api_not_authenticated(self):
        url = reverse("article-detail", args=[1])
        data = {"title": "Updated Title"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_article_detail_api(self):
        self.force_login_editor()
        url = reverse("article-detail", args=[1])
        data = {"title": "Updated Title 1"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), data.get("title"))

    def test_update_article_detail_api_not_found(self):
        self.force_login_editor()
        url = reverse("article-detail", args=[99])
        data = {"title": "Updated Title 1"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article_detail_api_bad(self):
        self.force_login_editor()
        url = reverse("article-detail", args=[1])
        data = {"title": ""}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArticleApprovalAPITestCase(AuthAPITestCase):

    def test_get_article_approval_api_not_authenticated(self):
        url = reverse("article-approval")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_article_approval_api_not_editor(self):
        self.force_login_writer()
        url = reverse("article-approval")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_article_approval_api(self):
        self.force_login_editor()
        url = reverse("article-approval")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_article_approval_api_not_authenticated(self):
        url = reverse("article-approval")
        data = {"id": 1, "status": "approved"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_article_approval_api_not_editor(self):
        self.force_login_writer()
        url = reverse("article-approval")
        data = {"id": 1, "status": "approved"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_article_approval_api_not_found(self):
        self.force_login_editor()
        url = reverse("article-approval")
        data = {"id": 99, "status": "approved"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article_approval_api(self):
        self.force_login_editor()
        url = reverse("article-approval")
        data = {"id": 1, "status": "approved"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_article_approval_api_bad(self):
        self.force_login_editor()
        url = reverse("article-approval")
        data = {"id": 1, "status": ""}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArticlesEditedAPITestCase(AuthAPITestCase):

    def test_articles_edited_api_not_authenticated(self):
        url = reverse("articles-edited")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_articles_edited_api_not_editor(self):
        self.force_login_writer()
        url = reverse("articles-edited")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_articles_edited_api(self):
        self.force_login_editor()
        url = reverse("articles-edited")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
