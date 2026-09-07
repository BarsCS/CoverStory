from django.core.management import BaseCommand
from django.conf import settings

import redis

from book.models import Book

class Command(BaseCommand):

    help = 'Sync database with cache Redis'

    def handle(self, *args, **options):

        updated_count = 0
        
        r = redis.Redis(host = settings.REDIS_HOST, 
                        port = settings.REDIS_PORT, 
                        db = settings.REDIS_DB, 
                        decode_responses=True)

        ranking_list = r.zrange('book:ranking', 0, -1, withscores=True)

        # [(book_id, score), (book_id, score)]

        if not ranking_list:
            self.stdout.write('Redis doesn\'t have data about total views')

        for book_id, score in ranking_list:

            book_id = int(book_id)
            views = int(score)

            updated = Book.objects.filter(id = book_id).update(views=views)

            if updated:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully update {updated_count} books"))