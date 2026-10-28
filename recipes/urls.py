from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('recipe/<int:pk>/rating/', views.add_rating, name='add_rating'),
    path('category/<int:pk>/', views.recipe_by_category, name='recipe_by_category'),
path('random/', views.random_recipe, name='random_recipe'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('recipe/<int:pk>/favorite/', views.add_to_favorites, name='add_to_favorites'),
path('signup/', views.SignUpView.as_view(), name='signup'),
]