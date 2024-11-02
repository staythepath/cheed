# activitypub_server/views.py
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from activitypub import Actor as APActor, Activity as APActivity
logger = logging.getLogger(__name__)

def webfinger(request):
    resource = request.GET.get('resource')
    if resource == 'acct:staythepath@ap.staythepath.lol':
        return JsonResponse({
            "subject": "acct:staythepath@ap.staythepath.lol",
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://ap.staythepath.lol/activitypub/actor/"
                }
            ]
        })
    return JsonResponse({"error": "Resource not found"}, status=404)




def actor(request):
    """Returns the Actor JSON data for federated ActivityPub requests."""
    if request.method == "GET":
        try:
            actor_data = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "https://ap.staythepath.lol/activitypub/actor/",
                "type": "Service",
                "name": "Cheed Aggregator Service",
                "inbox": "https://ap.staythepath.lol/activitypub/inbox/",
                "publicKey": {
                    "id": "https://ap.staythepath.lol/activitypub/actor#main-key",
                    "owner": "https://ap.staythepath.lol/activitypub/actor/",
                    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsAMRvlQ4v5Yex343kKzO\nsBzloZCS8XQVNruXo25adIFVjKH8ovSvp/t86P998ycx3Ea7AH75pc1tc6HoS4TH\n/OZ/masas0QJHfk663pHTQz6RceXPRIHgrx3HNDf1KFNlcZtfiFEhGKEdAjr/Q1y\nq6IgM+jRFyF8QXUHlYNUWoBRNeaYKAvNOPju3ODCTCNaxYJ45VK0Fblftday7Ha1\nBHe3b3X91cCfuFKmPoShiYqI9XueHLdUS7aIcc72PgZOeJputysrv2dDNdnxmiP1\nKAvdke4/4d4LSwMdf43oGspkAP9xk9d91+xNXWe1ywxqj/mkuYf+sn2v3WnvYOEf\nNQIDAQAB\n-----END PUBLIC KEY-----\n"
                }
            }
            return JsonResponse(actor_data, status=200, content_type="application/activity+json")

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


# Inbox endpoin
@csrf_exempt
def inbox(request):
    """Receives incoming federated activities from other servers and logs public posts."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Received ActivityPub post data: {data}")
            
            # Check activity type to process public "Create" posts
            activity_type = data.get("type")
            actor = data.get("actor")
            if activity_type == "Create":
                content = data.get("object", {}).get("content", "No content found")
                # Log or store the content as needed
                logger.info(f"New public post from {actor}: {content}")
                # Respond as per ActivityPub protocol for successful inbox receipt
                return HttpResponse(status=202)
            
            return HttpResponse(status=400)
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON received in inbox.")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error handling inbox activity: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return HttpResponse(status=405)





# Outbox endpoint
def outbox(request):
    """Returns the instance's own activities."""
    if request.method == "GET":
        # Assuming you have a list of activities stored, you can convert them to JSON
        activities = [
            APActivity(type="Create", actor="https://ap.staythepath.lol/activitypub/actor/", content="An example note.")
        ]
        activities_data = [activity.to_dict() for activity in activities]
        return JsonResponse(activities_data, safe=False)

    return HttpResponse(status=405)

# Followers endpoint
def followers(request):
    """Returns the list of followers for this actor."""
    if request.method == "GET":
        # Placeholder: Replace with logic to return followers list from database
        followers_list = []  # Implement your logic here
        return JsonResponse(followers_list, safe=False)

    return HttpResponse(status=405)

# Following endpoint
def following(request):
    """Returns the list of actors that this actor is following."""
    if request.method == "GET":
        try:
            # Logic to get the following list, for now, it's just an empty list
            following_list = []  
            return JsonResponse(following_list, safe=False)
        except Exception as e:
            # Handle any exception and provide a useful response
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)
