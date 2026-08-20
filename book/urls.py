from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('list/', views.book_list, name='list'),
]
