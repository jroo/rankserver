from django.db import models

# Create your models here.

class Campaign(models.Model):
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    multiplier = models.IntegerField()
    
class CampaignOption(models.Model):
    campaign = models.ForeignKey(Campaign)
    title = models.CharField(max_length=255)
    description = models.TextField()
    display_order = models.IntegerField()
    
class FormSubmission(models.Model):
    submission_id = models.CharField(max_length=64)
    campaign = models.ForeignKey(Campaign)
    item = models.ForeignKey(CampaignOption)
    rank = models.IntegerField()