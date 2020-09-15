from django.urls import path, include
from . import views

urlpatterns = [
    path('run/', views.home, name='home'),
    path('', views.usage, name='usage'),
    path('images/', views.saveImages, name='images'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('images/', views.saveImages, name='images'),
    path('upload/', views.Upload, name='upload'),
    path('analyze/', views.analyze_images, name='analyze'),
    path('download/', views.download_images, name='download'),
    path('home/', views.usage, name='usage'),
    path('labels/', views.showlabels, name='labels'),
    path('dataset/', views.dataset, name='dataset'),
    path('deldataset/<int:pmk>', views.delete_dataset, name='deldataset'),
    path('dataset/<int:pmk>', views.showdataset, name='showdataset'),
    path('downloaddataset/<int:pmk>', views.download_dataset, name='downloaddataset'),
    path('manalyze/<int:pmk>', views.analyze_images, name='manalyze'),
    path('multipleanalyze/', views.multiple_analyze, name='multipleanalyze'),
    path('multipleanalyze/<str:pmks>/', views.multiple_analyze, name='multipleanalyze'),
]