from django.db.models import Q
from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .models import Item

class ProductListView(ListView):
    queryset = Item.objects.all()
    

# class ProductDetailView(DetailView):
#     queryset = Item.objects.all()
