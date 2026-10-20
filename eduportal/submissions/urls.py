from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('run-pipeline/', views.execute_sorting_pipeline, name='run_pipeline'),
]
