import uuid

from django.core.validators import RegexValidator
from django.db import models

CODE_VALIDATOR = RegexValidator(
    regex=r'^[A-Z0-9]{2,5}$',
    message='Code must be 2-5 uppercase letters only')

class Province(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, validators=[CODE_VALIDATOR])  # shortform like BAG, GAN
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='districts')
    code = models.CharField(max_length=10, unique=True, validators=[CODE_VALIDATOR]) # shortform like KTM, PKR
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = [['name', 'province']]
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def __str__(self):
        return self.name
