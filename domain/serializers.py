from rest_framework import serializers

from domain.models import Writer, Article


class WriterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Writer
        fields = ["id", "name", "is_editor", "user"]
        read_only_fields = ["user"]


class ArticleSerializer(serializers.ModelSerializer):
    written_by = WriterSerializer(read_only=True)
    edited_by = WriterSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "status",
            "created_at",
            "written_by",
            "edited_by",
        ]
        read_only_fields = ["written_by", "edited_by", "created_at"]
