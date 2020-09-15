from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('myaccounts/', views.user_menu, name="user_menu"),
    path('change_password/', views.user_change_password, name="change_password"),
    path('user_update/', views.user_update, name="user_update"),
]