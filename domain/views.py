from datetime import timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.models import Article, Writer
from domain.permissions import IsEditor
from domain.serializers import ArticleSerializer, ArticleApprovalSerializer, \
    DashboardSerializer


# Create your views here.
class DashboardAPIView(APIView):

    def get(self, request):
        now = timezone.now()
        writers_summary = Writer.objects.annotate(
            total_articles_written=Count("articles_written"),
            total_articles_last_30=Count(
                "articles_written",
                filter=Q(
                    articles_written__created_at__gte=now - timedelta(days=30)
                ),
            ),
        )
        serializer = DashboardSerializer(writers_summary, many=True)
        return Response(serializer.data)


class ArticleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ArticleSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "PUT":
            return [IsAuthenticated()]
        return []

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(
            article, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleApprovalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEditor]

    def get(self, request):
        articles = Article.objects.filter(status="draft")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def put(self, request):
        article = get_object_or_404(Article, id=request.data["id"])

        if not request.user.writer.is_editor:
            return Response(
                {"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )

        status_action = request.data.get("status")
        serializer = ArticleApprovalSerializer(data=request.data)
        if serializer.is_valid():
            article.status = serializer.validated_data.get("status")
            article.edited_by = request.user.writer
            article.save()
            return Response(
                {"detail": f"Article {article.title} is {status_action}"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesEditedAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEditor]

    def get(self, request):
        articles = Article.objects.filter(
            edited_by=request.user.writer, status__in=["approved", "rejected"]
        )
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
