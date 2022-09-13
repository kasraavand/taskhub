from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy  as _


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=255)
    done = models.BooleanField(_("Done"), default=False)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tasks")
        verbose_name_plural = _("Tasks")

    def __unicode__(self):
        return smart_unicode(self.name)
