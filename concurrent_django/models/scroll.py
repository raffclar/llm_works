from django.db import models
from django.db.models import Model


class Scroll(Model):
    name = models.CharField(max_length=256)
    update_text = models.CharField(max_length=256)
