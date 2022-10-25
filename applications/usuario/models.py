from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    verificado = models.BooleanField(default=True)

import inspect
class ModeloBase(models.Model):
    """
    Clase base para todos los modelos de la aplicación.
    """
    created_by = models.ForeignKey(User, related_name='%(class)s_created', editable=False, on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey(User, related_name='%(class)s_modified', editable=False, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
            else:
                request = None

        user = request.user if request else 1

        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(ModeloBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.id