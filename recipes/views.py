from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'recipes/pages/home.html', context={'name': 'Jefferson Duarte'})


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={'name': 'Jefferson Duarte'})
