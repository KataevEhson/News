from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='home'),
    path('register/', views.registraion, name='registration'),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.show_profile, name='profile'),
    path('news/search/', views.search_news, name='search_news'),
    path('panel/', views.admin_panel, name='admin_panel'),
    path('news/create/', views.create_news, name='create_news'),
    path('news/<int:pk>/edit/', views.update_news, name='update_news'),
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),
]
