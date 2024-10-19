from django.urls import path

from .views import (
    DashboardAPIView,
    ArticleCreateAPIView,
    ArticleDetailAPIView,
)

urlpatterns = [
    path("", DashboardAPIView.as_view(), name="dashboard"),
    path(
        "article/create/",
        ArticleCreateAPIView.as_view(),
        name="article-create",
    ),
    path(
        "article/<int:article_id>/",
        ArticleDetailAPIView.as_view(),
        name="article-detail",
    ),
]
