from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google_play_scraper import app, reviews, Sort, reviews_all
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

def getReviewsBetweenDates(app_name, startDate, endDate):
    result, continuation_token = reviews(
        app_name,
        count=200,
    )

    oldest_date = result[-1]['at']
    while oldest_date > startDate:
        newResult, continuation_token = reviews(
            app_name,
            count=200,
            continuation_token=continuation_token
        )
        result.extend(newResult)
        oldest_date = result[-1]['at']

    # Filter out by newest date
    i = 0
    newest_date = result[i]['at']
    while newest_date > endDate:
        i += 1
        newest_date = result[i]['at']
    result = result[i:]

    # Filter out by oldest date
    i = 0
    oldest_date = result[-i-1]['at']
    while oldest_date < startDate:
        i += 1
        oldest_date = result[-i-1]['at']
    result = result[:-i]

    return result

class getReviews(APIView):
    def get(self, request):
        app_name = request.query_params.get('appName', '')
        
        startDate = request.query_params.get('startDate', (datetime.date.today() - datetime.timedelta(days=20)).strftime('%Y-%m-%d'))
        endDate = request.query_params.get('endDate', datetime.date.today().strftime('%Y-%m-%d'))
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

        result = getReviewsBetweenDates(app_name, startDate, endDate)

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

class NLP(APIView):
    def get(self, request):
            app_name = request.query_params.get('appName', '')
            
            startDate = request.query_params.get('startDate', (datetime.date.today() - datetime.timedelta(days=20)).strftime('%Y-%m-%d'))
            endDate = request.query_params.get('endDate', datetime.date.today().strftime('%Y-%m-%d'))
            startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
            endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

            result = getReviewsBetweenDates(app_name, startDate, endDate)

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
            return Response({"text": json.dumps(final_sentiments)}, status=status.HTTP_200_OK)
