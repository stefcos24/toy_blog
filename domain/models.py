# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Writer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_editor = models.BooleanField(default=False)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "writer"

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    written_by = models.ForeignKey(
        Writer, related_name="articles_written", on_delete=models.CASCADE
    )
    edited_by = models.ForeignKey(
        Writer,
        related_name="articles_edited",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.title
