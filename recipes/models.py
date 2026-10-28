from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    DIFFICULTY = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Сложно'),
    ]
    STATUS = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Краткое описание', blank=True)
    ingredients = models.TextField('Ингредиенты')
    steps = models.TextField('Приготовление')
    cooking_time = models.IntegerField('Время готовки (мин)', default=30)
    difficulty = models.CharField('Сложность', max_length=10, choices=DIFFICULTY, default='easy')
    image = models.ImageField('Фото', upload_to='recipes/', blank=True, null=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS, default='published')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def avg_rating(self):
        result = self.ratings.aggregate(models.Avg('value'))['value__avg']
        return round(result, 1) if result else 0

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Рецепт')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    body = models.TextField('Текст')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings', verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    value = models.IntegerField('Оценка')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f'{self.user.username} — {self.value}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'