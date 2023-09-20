from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipeName = models.CharField(max_length=100)
    recipeCode = models.ImageField()
    recipeDetils = models.TextField()
    recipeImage = models.ImageField(upload_to='RacipeImg')

    def __str__(self) -> str:
        return self.recipeName