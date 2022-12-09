from django.urls import path

from .views import SimpleAPIView
from .views import getReviews
from .views import NLP
from .views import appDetails
from .views import getRawReviews

urlpatterns = [
    path('test', SimpleAPIView.as_view(), name='test_api_view'),
    path('getReviews', getReviews.as_view(), name='getReviews_view'),
    path('NLP', NLP.as_view(), name='NLP'),
    path('appDetails', appDetails.as_view(), name='appDetails'),
    path('getRawReviews', getRawReviews.as_view(), name='getRawReviews')
]
