
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home),
    path("about", views.about),
    path("getprice", views.getPrice),
    path("fluctuations", views.fluctuations),
    path("product", views.product),
    path("users", views.users),
    path("usersproduct", views.usersProduct),
]
