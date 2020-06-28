from django.urls import path
from .views import *

app_name = 'MindMap'

urlpatterns = [
    path('new/', MindMapView.as_view()),
    path('list/', MindMapListView.as_view()),
    path('<int:shareID>/', MindMapView.as_view()),

    path('<int:mapID>/<int:parent_id>/', MindMapNodeInfoView.as_view()),
    path('<int:mapID>/<int:nodeID>/', MindMapNodeInfoView.as_view()),
    path('join/<int:shareID>/', MindMapCoInfoView.as_view())
]
