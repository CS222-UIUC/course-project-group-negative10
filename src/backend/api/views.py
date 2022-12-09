from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google_play_scraper import app, reviews, Sort, reviews_all
from app_store_scraper import AppStore
from collections import defaultdict
import datetime
import json
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

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
        store = request.query_params.get('store', '') 
        appname = request.query_params.get('text', '')
        if store == "Play Store":
            result, continuation_token = reviews(
                appname,
                # lang='en', # defaults to 'en'
                # country='us', # defaults to 'us'
                # sort=Sort.NEWEST, # defaults to Sort.NEWEST
                count=300, # defaults to 100
                # filter_score_with=5 # defaults to None(means all score)
            )
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
        elif store == "App Store":
            app = AppStore(country="us",app_name=appname)
            app.review(how_many=300)
            review_data = defaultdict(list)
            for review in reversed(app.reviews):
                day = review['at'].strftime('%Y-%m-%d')
                review_data[day].append(review['score'])
            
            review_data_average = {key:sum(values)/len(values) for key, values in review_data.items()}

            review_data_average_list = []
            for key, value in review_data_average.items():
                review_data_average_list.append({'date': key, 'rating': round(value, 2)})
            
            final_reviews = {'reviews': review_data_average_list}
            return Response({"text": json.dumps(final_reviews)}, status=status.HTTP_200_OK)
        
        
        
class NLP(APIView):
    def get(self, request):
            app_name = request.query_params.get('text', '')
            # result = reviews_all(
                # app_name,
                # sleep_milliseconds=0, # defaults to 0
                # lang='en', # defaults to 'en'
                # country='us', # defaults to 'us'
                # sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
                #filter_score_with=5 defaults to None(means all score)
            # )
            result, continuation_token = reviews(
                app_name,
                # lang='en', # defaults to 'en'
                # country='us', # defaults to 'us'
                # sort=Sort.NEWEST, # defaults to Sort.NEWEST
                count=300, # defaults to 100
                # filter_score_with=5 # defaults to None(means all score)
            )

            sia = SentimentIntensityAnalyzer()
            sentiment_scores = defaultdict(list)
            for review in reversed(result):
                day = review['at'].strftime('%Y-%m-%d')
                score = sia.polarity_scores(review['content'])['compound']
                sentiment_scores[day].append(score)

            sentiment_scores_average = {key:sum(values)/len(values) for key, values in sentiment_scores.items()}

            sentiment_data_average_list = []
            for key, value in sentiment_scores_average.items():
                sentiment_data_average_list.append({'date': key, 'sentiment': round(value, 2)})
            
            final_sentiments = {'sentiments': sentiment_data_average_list}
            print(final_sentiments)
            return Response({"text": json.dumps(final_sentiments)}, status=status.HTTP_200_OK)



