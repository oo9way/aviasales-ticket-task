from django.urls import path
from app import views

urlpatterns = [path("", views.AviaSalesHome.as_view())]
