from django.urls import path

from .views import homePageView, addView, deleteView, downloadView, RegisterView, addMessage

urlpatterns = [
    path('', homePageView, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add/', addView, name='add'),
    path('addMessage/', addMessage, name='addMessage'),
    path('download/<int:fileid>', downloadView, name='add'),
    path('delete/', deleteView, name='delete'),
]
