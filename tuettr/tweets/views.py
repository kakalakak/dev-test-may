from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tweets.models import Tweet, Topic
from tweets.serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import random

    
class TweetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def random(self, request, **kwargs):
        random_tweet = random.choice(Tweet.objects.exclude(topics=None))
        # random_tweet = Tweet.objects.order_by('?').first()
        return Response(TweetSerializer(random_tweet).data)