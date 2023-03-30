from django.db import models
from django.contrib.auth.models import User, Group


class Post(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "post"
