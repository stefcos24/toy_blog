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

    def create(self, validated_data):
        user = self.context["request"].user
        writer = Writer.objects.get(user=user)
        validated_data["written_by"] = writer
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


class ArticleApprovalSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=["approved", "rejected"])

    class Meta:
        model = Article
        fields = ["id", "status"]


class DashboardSerializer(serializers.Serializer):
    writer = serializers.CharField(source="name")
    total_articles_written = serializers.IntegerField()
    total_articles_last_30 = serializers.IntegerField()
