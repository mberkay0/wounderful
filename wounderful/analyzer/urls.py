from django.urls import path, include
from . import views
from analyzer.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('run/', views.home, name='home'),
    path('', views.saveImages, name='images'),
    path('images/', views.saveImages, name='images'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('images/', views.saveImages, name='images'),
    path('upload/', views.Upload, name='upload'),
    path('analyze/', views.analyze_images, name='analyze'),
    path('download/', views.download_images, name='download'),
]