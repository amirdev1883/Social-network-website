from django.shortcuts import render
from django.views import View
from .models import post


class HomeView(View):
    def get(self, request):
        posts = post.objects.all()
        return render(request, 'home/index.html', {"posts":posts})

