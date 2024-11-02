from django.core.management.base import BaseCommand
from activitypub_server.activitypub_utils import send_follow_request

class Command(BaseCommand):
    help = "Send a follow request from the service actor to the target actor."

    def add_arguments(self, parser):
        parser.add_argument('target_actor_url', type=str, help='The URL of the actor to follow')
        parser.add_argument('inbox_url', type=str, help='The inbox URL of the target actor')

    def handle(self, *args, **options):
        target_actor_url = options['target_actor_url']
        service_actor_url = "https://ap.staythepath.lol/activitypub/actor/"
        inbox_url = options['inbox_url']
        
        status_code = send_follow_request(target_actor_url, service_actor_url, inbox_url)
        if status_code == 200 or status_code == 202:
            self.stdout.write(self.style.SUCCESS(f"Successfully sent follow request to {target_actor_url}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to send follow request to {target_actor_url}"))