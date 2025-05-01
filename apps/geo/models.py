from django.db import models


class Region(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name_uz = models.CharField(max_length=100, verbose_name="uz name")
    name_ru = models.CharField(max_length=100, verbose_name="ru name")
    ordering = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name_uz

    def __str__(self):
        return self.name_uz
    
    class Meta:
        ordering = ['name_uz']


class District(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name_uz = models.CharField(max_length=100, verbose_name="uz name")
    name_ru = models.CharField(max_length=100, verbose_name="ru name")
    region = models.ForeignKey(Region, related_name="district_region", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(default=0)

    @property
    def parent(self):
        return self.region

    def __unicode__(self):
        return self.name_uz

    def __str__(self):
        return self.name_uz
    
    class Meta:
        ordering = ['name_uz']
