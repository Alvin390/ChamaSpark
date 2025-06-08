from django.urls import path
from .views import SparkGalChatView

urlpatterns = [
    path('chat/', SparkGalChatView.as_view(), name='sparkgal_chat'),
]