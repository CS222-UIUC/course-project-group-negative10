from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google_play_scraper import app, reviews, Sort, reviews_all
from collections import defaultdict
import datetime
import json
import en_core_web_sm
from spacytextblob.spacytextblob import SpacyTextBlob
from bs4 import BeautifulSoup
import requests
class SimpleAPIView(APIView):
    def get(self, request):
        text = request.query_params.get('text', '')
        result = app(
            text,
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        return Response({"text": "test"}, status=status.HTTP_200_OK)
        # return Response({"text": str(result)}, status=status.HTTP_200_OK)

class getReviews(APIView):
    def get(self, request):
        app_name = request.query_params.get('text', '')
        result, continuation_token = reviews(
            app_name,
            # lang='en', # defaults to 'en'
            # country='us', # defaults to 'us'
            # sort=Sort.NEWEST, # defaults to Sort.NEWEST
            # count=100, # defaults to 100
            # filter_score_with=5 # defaults to None(means all score)
        )
        #nlp = spacy.load("en_core_web_trf")
        review_data = defaultdict(list)
        for review in reversed(result):
            day = review['at'].strftime('%Y-%m-%d')
            review_data[day].append(review['score'])

        review_data_average = {key:sum(values)/len(values) for key, values in review_data.items()}

        review_data_average_list = []
        for key, value in review_data_average.items():
            review_data_average_list.append({'date': key, 'rating': round(value, 2)})
        
        final_reviews = {'reviews': review_data_average_list}
        return Response({"text": json.dumps(final_reviews)}, status=status.HTTP_200_OK)
def NLP(self, request):
        app_name = request.query_params.get('text', '')
        result = reviews_all(
            app_name,
            sleep_milliseconds=0, # defaults to 0
            lang='en', # defaults to 'en'
            country='us', # defaults to 'us'
            sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
            #filter_score_with=5 defaults to None(means all score)
        )  
        nlp = en_core_web_sm.load()
        nlp.add_pipe('spacytextblob')
        sentiment = []
        for review in result:
            doc = nlp(review['content'])
            sentiment.append(doc._.blob.polarity)
        
        overall = 0
        for score in sentiment:
            overall += score

        overall = overall * 100 / len(sentiment) # sentiment %