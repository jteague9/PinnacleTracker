from django.core.management.base import BaseCommand
from app.src.update_records import fetch_moneylines, purge_duplicate_ml_records


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

    def handle(self, *args, **options):
        if options.get('fetch'):
            fetch_moneylines()
        if options.get('purge_dup'):
            purge_duplicate_ml_records()
