from django.urls import path
from .views import HomePageView, TopPageView

app_name = "WebAR"
urlpatterns = [
    path('ar/',HomePageView.as_view(), name='ar'),
    path('',TopPageView.as_view(), name='top'),
]