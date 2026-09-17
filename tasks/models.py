from django.db import models


class Task(models.Model):
    """やることを1件表すデータ。"""

    title = models.CharField("タイトル", max_length=100)
    is_done = models.BooleanField("完了", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["is_done", "-created_at"]

    def __str__(self):
        return self.title
