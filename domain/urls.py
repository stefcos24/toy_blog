from django.urls import path

from .views import (
    DashboardAPIView,
    ArticleCreateAPIView,
)

urlpatterns = [
    path("", DashboardAPIView.as_view(), name="dashboard"),
    path(
        "article/create/",
        ArticleCreateAPIView.as_view(),
        name="article-create",
    ),
]
