from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from tasks.views import custom_login

def root_redirect(request):
    return redirect('task_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('tasks/', include('tasks.urls')),
    path('', root_redirect),
]