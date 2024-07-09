from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Platform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=200)
    website_url = models.URLField(max_length=200)

    def __str__(self) -> str:
        return self.name


class TitleList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating=models.FloatField(default=0)
    total_rating=models.IntegerField(default=0)
    platform= models.ForeignKey(Platform,on_delete=models.CASCADE, related_name="TitleList")

    def __str__(self) -> str:
        return self.title
    
class Review(models.Model):
    reviewer_name=models.ForeignKey(User, on_delete=models.CASCADE)
    rating= models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    TitleList=models.ForeignKey(TitleList,on_delete=models.CASCADE, related_name="reviews")
    description=models.CharField(max_length=200, null=True)
    active =models.BooleanField(default=True)
    created= models.DateTimeField(auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.reviewer_name) +" | " + str(self.rating) + " | " + self.TitleList.title


