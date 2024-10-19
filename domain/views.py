from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.models import Article
from domain.serializers import ArticleSerializer


# Create your views here.
class DashboardAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
