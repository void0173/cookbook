from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Recipe, Category, Comment, Rating, Favorite
import random

def recipe_list(request):
    recipes = Recipe.objects.filter(status='published')
    categories = Category.objects.all()
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(title__icontains=query)
    sort = request.GET.get('sort')
    if sort == 'fast':
        recipes = recipes.order_by('cooking_time')
    elif sort == 'slow':
        recipes = recipes.order_by('-cooking_time')
    else:
        recipes = recipes.order_by('-created_at')
    return render(request, 'recipes/list.html', {'recipes': recipes, 'categories': categories})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/detail.html', {'recipe': recipe})

def recipe_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    recipes = Recipe.objects.filter(category=category, status='published')
    categories = Category.objects.all()
    return render(request, 'recipes/list.html', {'recipes': recipes, 'categories': categories, 'current_category': category})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        recipe = Recipe.objects.create(
            author=request.user,
            title=request.POST['title'],
            category_id=request.POST['category_id'],
            description=request.POST.get('description', ''),
            ingredients=request.POST['ingredients'],
            steps=request.POST['steps'],
            cooking_time=request.POST['cooking_time'],
            difficulty=request.POST['difficulty'],
            image=request.FILES.get('image'),
        )
        return redirect('recipe_detail', pk=recipe.pk)
    return render(request, 'recipes/create.html', {'categories': Category.objects.all()})

@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        Comment.objects.create(recipe=recipe, author=request.user, body=request.POST['body'])
    return redirect('recipe_detail', pk=pk)

@login_required
def add_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        Rating.objects.update_or_create(recipe=recipe, user=request.user, defaults={'value': request.POST['value']})
    return redirect('recipe_detail', pk=pk)

def random_recipe(request):
    recipes = Recipe.objects.filter(status='published')
    if recipes.exists():
        recipe = random.choice(recipes)
        return redirect('recipe_detail', pk=recipe.pk)
    return redirect('recipe_list')

@login_required
def add_to_favorites(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipe_detail', pk=pk)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorites.html', {'favorites': favorites})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'