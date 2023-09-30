from django.db import models
import uuid
# Create your models here.


class NFT(models.Model):
    xid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=256, null=False, blank=False)
    image_url = models.CharField(max_length=256, null=False, blank=False)
    animation_url = models.CharField(max_length=256, null=True, blank=True)
    gltf_url = models.CharField(max_length=256, null=True, blank=True)