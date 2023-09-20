from django.shortcuts import render
from recipe.models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, "home/home.html", context={'recipes':recipes, 'page':'RacipeHOME'})