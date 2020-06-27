from django.urls import path
from .views import *


app_name = 'MindMap'

urlpatterns = [
    path('<int:shareID>/', MindMapView.as_view())
]