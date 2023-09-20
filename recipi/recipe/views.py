from django.shortcuts import render, redirect
from recipe.models import *
from django.contrib.auth.models import*
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def CreateRecipe(request):
    if request.method == 'POST':
        data = request.POST
        # get data fro data
        recipe = {
            'recipeName': data.get('recipeName'), 
            'recipeCode':data.get("recipeCode"), 
            'recipeDetils': data.get("recipeDetils"),
            'recipeImage': request.FILES.get('recipeImage')
        }
        Recipe.objects.create(**recipe)
        return redirect('/recipe/')
    recipes = Recipe.objects.all()
    if request.GET.get('search'):
        print(request.GET.get('search'))
        recipes = recipes.filter(recipeName__icontains = request.GET.get('search'))
    return render(request, "recipetempltes/createrecipe.html", context={'recipes': recipes , 'page': 'Racipe'})

def user_login(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.error(request, f"{username} is invalid usser")
            return redirect('/login/')
        
        user = authenticate(username = username, password= password)

        if user is None:
            messages.error(request , "Invalid password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipe/')

    return render(request, 'recipetempltes/login.html')

@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    return redirect('/login/')



def user_register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        userexist = User.objects.filter(username = username)
        if userexist.exists():
            messages.info(request, f'{username} is alrady taken')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.success(request, f'{user} created successfully')
        return redirect('/register/')
    users = User.objects.all()
    return render(request, 'recipetempltes/register.html', context = {'users':users})    

@login_required(login_url='/login/')
def delete_recipe(request, id):
   recipe = Recipe.objects.get(id=id)
   recipe.delete()
   return redirect('/recipe/')

@login_required(login_url='/login/')
def get_recipe(request, id):
    queryset = Recipe.objects.get(id = id)

    if request.method == 'POST':
        data = request.POST
        recip_img = request.FILES.get('recipeImage')
        recipe_name = data.get('recipeName') 
        recipe_code = data.get("recipeCode")
        recipe_detils = data.get("recipeDetils")
        # updating
        queryset.recipeName = recipe_name
        queryset .recipeCode = recipe_code
        queryset .recipeDetils = recipe_detils
        if recip_img:
             queryset.recipeImage = recip_img
        queryset .save()
        return redirect('/recipe/')
    return render(request, 'recipetempltes/updaterecipe.html', context={'recipe': queryset})
    


