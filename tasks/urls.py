from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/complete/', views.task_complete, name='task_complete'),
]