from rest_framework import serializers
from tweets.models import Tweet, Topic


class RelatedTweet(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'body']


class TweetSerializer(serializers.ModelSerializer):
    related_tweets = RelatedTweet(many=True, required=False)

    class Meta:
        model = Tweet
        fields = ['id', 'body', 'related_tweets']
