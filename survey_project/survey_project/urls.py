from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/login/',auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('profile/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('main.urls')),
    path('__debug__/', include('debug_toolbar.urls')), 
]
