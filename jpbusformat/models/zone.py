from django.contrib.gis.db import models


class Zone(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="運賃エリアID")
