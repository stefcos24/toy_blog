from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.models import Article
from domain.serializers import ArticleSerializer, ArticleApprovalSerializer


# Create your views here.
class DashboardAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleCreateAPIView(APIView):

    def post(self, request):
        serializer = ArticleSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):

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

    def get(self, request):
        articles = Article.objects.filter(
            edited_by=request.user.writer, status__in=["approved", "rejected"]
        )
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
