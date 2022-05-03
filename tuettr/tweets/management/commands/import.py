import base64

from django.core.management.base import BaseCommand
from tweets.models import Tweet


class Command(BaseCommand):
    help = 'Commandline to import data'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename'], 'r') as f:
            count = 0
            for line in f:
                count += 1
                if Tweet.objects.filter(body=line.strip()).exists():
                    print('exists')
                    continue
                print("Line{}: {}".format(count, line.strip()))
                Tweet.objects.create(body=line.strip())
