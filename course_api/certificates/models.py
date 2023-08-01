from django.db import models


class Certificate(models.Model):
    name = models.CharField(max_length=255, null=False)
    url = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey("courses.Course", on_delete=models.PROTECT, null=False)

    def __str__(self) -> str:
        return str(self.name)
