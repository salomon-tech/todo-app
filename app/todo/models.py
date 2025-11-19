from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=350, unique=True)
    completed = models.BooleanField(default=False)
    created = models.DataTimeField(auto_now_add=True)

    def __self__(self):
        return self.title