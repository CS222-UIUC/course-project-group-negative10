from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from google_play_scraper import app, reviews, Sort, reviews_all
from google_play_scraper.features.reviews import _ContinuationToken
from app_store_scraper import AppStore
from collections import defaultdict,OrderedDict
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from django.contrib import messages
nltk.download('vader_lexicon')

class SimpleAPIView(APIView):
    def get(self, request):
        text = request.query_params.get('text', '')
        result = app(
            text,
            lang='en',  # defaults to 'en'
            country='us'  # defaults to 'us'
        )
        return Response({"text": "test"}, status=status.HTTP_200_OK)
        # return Response({"text": str(result)}, status=status.HTTP_200_OK)


def PlayStoreRatings(app_name, startDate, endDate):
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
    review_data = defaultdict(list)
    for review in reversed(result):
        day = review['at'].strftime('%Y-%m-%d')
        review_data[day].append(review['score'])

    review_data_average = {
        key: sum(values)/len(values) for key, values in review_data.items()}

    review_data_average_list = []
    for key, value in review_data_average.items():
        review_data_average_list.append({'date': key, 'rating': round(value, 2)})

    final_reviews = {'reviews': review_data_average_list}
    return Response({"text": json.dumps(final_reviews)}, status=status.HTTP_200_OK)

def AppStoreRatings(appname, startDate, endDate):
    app = AppStore(country="us", app_name=appname)
    app.review(how_many=20,after=startDate)
    result = app.reviews
    review_data = defaultdict(list)
    for review in result:
        day = review['date'].strftime('%Y-%m-%d')
        review_data[day].append(review['rating'])
    
    data = defaultdict(list)
    for key in sorted(review_data.keys()):
        data[key] = (review_data[key])

    review_data = data
    review_data_average = {
        key: sum(values)/len(values) for key, values in review_data.items()}

    review_data_average_list = []
    for key, value in review_data_average.items():
        review_data_average_list.append({'date': key, 'rating': round(value, 2)})

    final_reviews = {'reviews': review_data_average_list}
    return Response({"text": json.dumps(final_reviews)}, status=status.HTTP_200_OK)
def AppStoreNLP(appname,startDate,endDate):
    app = AppStore(country="us", app_name=appname)
    app.review(how_many=20,after=startDate)
    result = app.reviews
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = defaultdict(list)
    for review in reversed(result):
        day = review['date'].strftime('%Y-%m-%d')
        score = sia.polarity_scores(review['review'])['compound']
        sentiment_scores[day].append(score)
    print(sentiment_scores)
    data = defaultdict(list)
    for key in sorted(sentiment_scores.keys()):
        data[key]=sentiment_scores[key]
    
    sentiment_scores = data
    print(sentiment_scores)
    sentiment_scores_average = {
        key: sum(values)/len(values) for key, values in sentiment_scores.items()}

    sentiment_data_average_list = []
    for key, value in sentiment_scores_average.items():
        sentiment_data_average_list.append(
            {'date': key, 'sentiment': round(value, 2)})

    final_sentiments = {'sentiments': sentiment_data_average_list}
    return Response({"text": json.dumps(final_sentiments)}, status=status.HTTP_200_OK)

    


class getReviews(APIView):
    def get(self, request):
        app_name = request.query_params.get('appName', '')
        store = request.query_params.get('store', '')
        startDate = request.query_params.get('startDate', (datetime.date.today(
        ) - datetime.timedelta(days=20)).strftime('%Y-%m-%d'))
        endDate = request.query_params.get(
            'endDate', datetime.date.today().strftime('%Y-%m-%d'))
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

        result = []
        if store == "Play Store":
            return PlayStoreRatings(app_name, startDate, endDate)
        elif store == "App Store":
            return AppStoreRatings(app_name, startDate, endDate)

        
def PlayStoreNLP(app_name, startDate, endDate):
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

    sia = SentimentIntensityAnalyzer()
    sentiment_scores = defaultdict(list)
    for review in reversed(result):
        day = review['at'].strftime('%Y-%m-%d')
        score = sia.polarity_scores(review['content'])['compound']
        sentiment_scores[day].append(score)

    sentiment_scores_average = {
        key: sum(values)/len(values) for key, values in sentiment_scores.items()}

    sentiment_data_average_list = []
    for key, value in sentiment_scores_average.items():
        sentiment_data_average_list.append(
            {'date': key, 'sentiment': round(value, 2)})

    final_sentiments = {'sentiments': sentiment_data_average_list}
    return Response({"text": json.dumps(final_sentiments)}, status=status.HTTP_200_OK)

class NLP(APIView):
    def get(self, request):
        
        app_name = request.query_params.get('appName', '')
        store = request.query_params.get('store', '')
        startDate = request.query_params.get('startDate', (datetime.date.today(
        ) - datetime.timedelta(days=20)).strftime('%Y-%m-%d'))
        endDate = request.query_params.get(
            'endDate', datetime.date.today().strftime('%Y-%m-%d'))
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

        result = []
        if store == "Play Store":
            return PlayStoreNLP(app_name, startDate, endDate)
        elif store == "App Store":
            return AppStoreNLP(app_name, startDate, endDate)

class appDetails(APIView):
    def get(self, request):       
        app_name = request.query_params.get('appName', '')
        result = app(app_name)
        histogram_list = []
        for i in reversed(range(len(result['histogram']))):
            histogram_list.append({'rating': i+1, 'count': result['histogram'][i]})
        result['histogram'] = histogram_list
        return Response({"text": json.dumps(result)}, status=status.HTTP_200_OK)

class getRawReviews(APIView):
    def get(self, request):       
        app_name = request.query_params.get('appName', '')
        continuation_token = request.query_params.get('continuationToken', '')
        if continuation_token == "undefined":
            continuation_token = None
        else:
            continuation_token = _ContinuationToken(continuation_token, 'en', 'us', Sort.NEWEST, count=30, filter_score_with=None)
        result, new_continuation_token = reviews(app_name, continuation_token=continuation_token, count=30)
        final = {'reviews': result, 'continuationToken': new_continuation_token.token}
        return Response({"text": json.dumps(final, cls=DjangoJSONEncoder)}, status=status.HTTP_200_OK)


        
