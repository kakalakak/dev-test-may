from django.db import models
import spacy
from collections import Counter
from string import punctuation
nlp = spacy.load("en_core_web_lg")
import en_core_web_lg
nlp = en_core_web_lg.load()
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False) # topic.tweet_set.all()
       
    def __str__(self):
        return self.name
    
    
class Tweet(models.Model):
    body = models.TextField(null=False,blank=False)
    topics = models.ManyToManyField(Topic, null=True, blank=True) #tweet.topics.all()

    def get_hotwords(self,text):
        result = []
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
        doc = nlp(text.lower()) # 2
        for token in doc:
            # 3
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            # 4
            if(token.pos_ in pos_tag):
                result.append(token.text)
        return result # 5 

    @property
    def related_tweets(self):
        related_tweets_list_of_sets = [topic.tweet_set.all() for topic in self.topics.all()] #[<QuerySet [<Tweet: Tweet object (3)>]>, <QuerySet [<Tweet: Tweet object (3)>]>]
        related_tweets = set()
        for query_set in related_tweets_list_of_sets:
            for tweet in query_set:
                if self.pk == tweet.pk:
                    continue
                related_tweets.add(tweet)
                
        return list(related_tweets) #TODO: to make this go through teh serializer at some point
        

    def save(self,*args,**kwargs):
        # if not self.pk:
        super(Tweet,self).save(*args,**kwargs)
 
        hotwords = self.get_hotwords(self.body)
        for word in hotwords:
            if Topic.objects.filter(name=word).count()==0:
                new_topic = Topic(name = word)
                new_topic.save()
            else:
                new_topic = Topic.objects.get(name=word)

            self.topics.add(new_topic)
        # super(Tweet,self).save(*args,**kwargs)