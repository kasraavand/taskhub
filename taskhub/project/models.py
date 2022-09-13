from django.db import models
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager')
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    developers = models.ManyToManyField(User, related_name='developer', blank=True, null=True)


    def save(self, *args, **kwargs):
        
        if self.manager.role != 'manager':
            raise ValueError(f"Manager is fake! It doesn't have a manager role! User's role is {self.manager.role}")
        super().save(*args, **kwargs)