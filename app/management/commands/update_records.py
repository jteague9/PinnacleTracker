from django.core.management.base import BaseCommand
from app.src.update_records import fetch_moneylines, purge_duplicate_ml_records,\
    count_db_entries, purge_records_until_limit
from app.src.update_winner import update_all_winners


class Command(BaseCommand):
    help = "Loads latest moneyline bets"

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--fetch",
            action="store_true",
            help="Fetch moneyline records",
        )
        parser.add_argument(
            "-p",
            "--purge-dup",
            action="store_true",
            help="Purge duplicate moneyline records",
        )
        parser.add_argument(
            "-c",
            "--count",
            action="store_true",
            help="Count db entries",
        )
        parser.add_argument(
            "-r",
            "--reduce-to",
            help="Reduce total db records to specified limit",
        )
        parser.add_argument(
            "-w",
            "--winners",
            action="store_true",
            help="Update all the winners for closed matchups",
        )

    def handle(self, *args, **options):
        if options.get('fetch'):
            fetch_moneylines()
        if options.get('purge_dup'):
            purge_duplicate_ml_records()
        if options.get('count'):
            print(count_db_entries())
        if options.get('reduce_to'):
            purge_records_until_limit(int(options['reduce_to']))
        if options.get('winners'):
            update_all_winners()
