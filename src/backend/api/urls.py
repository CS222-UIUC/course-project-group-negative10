from django.urls import path

from .views import SimpleAPIView
from .views import getReviews

urlpatterns = [
    path('test', SimpleAPIView.as_view(), name='test_api_view'),
    path('getReviews', getReviews.as_view(), name='getReviews_view')
]
