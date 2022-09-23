from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google_play_scraper import app

class SimpleAPIView(APIView):
    def get(self, request):
        text = request.query_params.get('text', '')
        result = app(
            text,
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        return Response({"text": str(result)}, status=status.HTTP_200_OK)
