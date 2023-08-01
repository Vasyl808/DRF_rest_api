from django.db import models


class Lesson(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    is_open = models.BooleanField(default=False, null=False)
    video_url = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return str(self.name)
