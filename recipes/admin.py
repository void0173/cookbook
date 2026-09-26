from django.contrib import admin
from .models import Category, Recipe, Comment, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'cooking_time', 'difficulty', 'status')
    list_filter = ('category', 'difficulty', 'status')
    search_fields = ('title', 'ingredients')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'author', 'created_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user', 'value')