from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission


class GlobalPermissionManager(models.Manager):
    def get_query_set(self):
        return super(GlobalPermissionManager, self).\
            get_query_set().filter(content_type__name='global_permission')


class GlobalPermission(Permission):
    """A global permission, not attached to a model"""

    objects = GlobalPermissionManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            name="global_permission", app_label=self._meta.app_label
        )
        self.content_type = ct
        super(GlobalPermission, self).save(*args, **kwargs)


try:
    permission = GlobalPermission.objects.get_or_create(
        codename='can_upload_files',
        name='Can Upload Files',
    )
except:
    # "Table 'fileswidgettest16.auth_permission' doesn't exist"
    # it should exist the next time that this file is loaded
    pass


class FileComment(models.Model):
    path = models.CharField(max_length=255, unique=True)
    comment = models.CharField(max_length=500)
