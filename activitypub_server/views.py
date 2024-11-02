# activitypub_server/views.py
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from activitypub import Actor as APActor, Activity as APActivity

def webfinger(request):
    """WebFinger endpoint to provide actor discovery"""
    resource = request.GET.get('resource')
    if resource == 'acct:staythepath@ap.staythepath.lol':
        response_data = {
            "subject": "acct:staythepath@ap.staythepath.lol",
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://ap.staythepath.lol/activitypub/actor/"
                }
            ]
        }
        return JsonResponse(response_data)
    
    # If the requested resource is not found, respond with a 404 error
    return JsonResponse({"error": "Resource not found"}, status=404)



def actor(request):
    """Returns the Actor JSON data."""
    if request.method == "GET":
        try:
            actor_data = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "https://ap.staythepath.lol/activitypub/actor/",
                "type": "Service",
                "name": "Cheed Aggregator Service",
                "inbox": "https://ap.staythepath.lol/activitypub/inbox/",
                "outbox": "https://ap.staythepath.lol/activitypub/outbox/",
                "publicKey": {
                    "id": "https://ap.staythepath.lol/activitypub/actor#main-key",
                    "owner": "https://ap.staythepath.lol/activitypub/actor/",
                    "publicKeyPem": open('activitypub_server/public.pem').read()
                }
            }
            logger.info(f"Actor endpoint accessed: {request.get_full_path()}")
            response = JsonResponse(actor_data, status=200)
            response["Content-Type"] = "application/activity+json"
            return response

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    logger.warning(f"Invalid request method: {request.method}")
    return JsonResponse({"error": "Method not allowed"}, status=405)


# Inbox endpoint
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def inbox(request):
    """Receives incoming federated activities."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Received activity: {data}")  # Log the received activity
            activity_type = data.get("type")
            
            if activity_type == "Create":
                # Handle a new post creation
                activity = APActivity.from_dict(data)
                # Logic to store activity or process further if needed.
                return HttpResponse(status=202)
            elif activity_type == "Follow":
                # Handle follow requests
                activity = APActivity.from_dict(data)
                # Logic to store or approve follow if needed.
                return HttpResponse(status=202)
            else:
                return HttpResponse(status=400)
        except json.JSONDecodeError:
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
