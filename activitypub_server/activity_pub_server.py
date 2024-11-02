import os
import django
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from activitypub import Service, Activity
import logging
from email.utils import formatdate  # For formatting Date headers
import hashlib  # For creating the digest
import base64  # For encoding the digest and signature
from Crypto.PublicKey import RSA  # For RSA key import
from Crypto.Signature import PKCS1_v1_5  # For signing HTTP requests
from Crypto.Hash import SHA256  # For hashing the signature string


# Set up Django environment before any imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')
django.setup()

from post_manager.models import Post  # Import your existing Django model

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Flask logger to work alongside Python logging
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

# Define global list to keep track of actors we are aggregating from
tracked_actors = ["https://mstdn.social/users/staythepath"]  # Example tracked actor


# Actor endpoint definition (for the aggregator service)
@app.route('/actor', methods=['GET'])
def actor():
    app.logger.info("Received request for actor endpoint")

    # Create an instance of the Service actor for aggregation purposes
    aggregator_actor = Service()
    aggregator_actor.ap_id = "https://ap.staythepath.lol/aggregator"
    aggregator_actor.ap_name = "Cheed Aggregator Service"
    aggregator_actor.ap_inbox = "https://ap.staythepath.lol/shared-inbox"
    aggregator_actor.ap_publicKey = {
        "id": "https://ap.staythepath.lol/aggregator#main-key",
        "owner": "https://ap.staythepath.lol/aggregator",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsAMRvlQ4v5Yex343kKzO
        sBzloZCS8XQVNruXo25adIFVjKH8ovSvp/t86P998ycx3Ea7AH75pc1tc6HoS4TH
        /OZ/masas0QJHfk663pHTQz6RceXPRIHgrx3HNDf1KFNlcZtfiFEhGKEdAjr/Q1y
        q6IgM+jRFyF8QXUHlYNUWoBRNeaYKAvNOPju3ODCTCNaxYJ45VK0Fblftday7Ha1
        BHe3b3X91cCfuFKmPoShiYqI9XueHLdUS7aIcc72PgZOeJputysrv2dDNdnxmiP1
        KAvdke4/4d4LSwMdf43oGspkAP9xk9d91+xNXWe1ywxqj/mkuYf+sn2v3WnvYOEf
        NQIDAQAB
        -----END PUBLIC KEY-----"""
    }

    actor_dict = aggregator_actor.to_dict()

    # Add the public key to the actor dictionary explicitly
    actor_dict["publicKey"] = {
        "id": "https://ap.staythepath.lol/aggregator#main-key",
        "owner": "https://ap.staythepath.lol/aggregator",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsAMRvlQ4v5Yex343kKzO
        sBzloZCS8XQVNruXo25adIFVjKH8ovSvp/t86P998ycx3Ea7AH75pc1tc6HoS4TH
        /OZ/masas0QJHfk663pHTQz6RceXPRIHgrx3HNDf1KFNlcZtfiFEhGKEdAjr/Q1y
        q6IgM+jRFyF8QXUHlYNUWoBRNeaYKAvNOPju3ODCTCNaxYJ45VK0Fblftday7Ha1
        BHe3b3X91cCfuFKmPoShiYqI9XueHLdUS7aIcc72PgZOeJputysrv2dDNdnxmiP1
        KAvdke4/4d4LSwMdf43oGspkAP9xk9d91+xNXWe1ywxqj/mkuYf+sn2v3WnvYOEf
        NQIDAQAB
        -----END PUBLIC KEY-----"""
    }

    app.logger.debug(f"Actor JSON response: {json.dumps(actor_dict, indent=2)}")

    return jsonify(actor_dict)

# Aggregator Actor Endpoint Definition (for the aggregator service)
@app.route('/aggregator', methods=['GET'])
def aggregator():
    app.logger.info("Received request for aggregator endpoint")

    # Create an instance of the Service actor for aggregation purposes
    aggregator_actor = Service()
    aggregator_actor.ap_id = "https://ap.staythepath.lol/aggregator"
    aggregator_actor.ap_name = "Cheed Aggregator Service"
    aggregator_actor.ap_inbox = "https://ap.staythepath.lol/shared-inbox"
    aggregator_actor.ap_publicKey = {
        "id": "https://ap.staythepath.lol/aggregator#main-key",
        "owner": "https://ap.staythepath.lol/aggregator",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsAMRvlQ4v5Yex343kKzO
        sBzloZCS8XQVNruXo25adIFVjKH8ovSvp/t86P998ycx3Ea7AH75pc1tc6HoS4TH
        /OZ/masas0QJHfk663pHTQz6RceXPRIHgrx3HNDf1KFNlcZtfiFEhGKEdAjr/Q1y
        q6IgM+jRFyF8QXUHlYNUWoBRNeaYKAvNOPju3ODCTCNaxYJ45VK0Fblftday7Ha1
        BHe3b3X91cCfuFKmPoShiYqI9XueHLdUS7aIcc72PgZOeJputysrv2dDNdnxmiP1
        KAvdke4/4d4LSwMdf43oGspkAP9xk9d91+xNXWe1ywxqj/mkuYf+sn2v3WnvYOEf
        NQIDAQAB
        -----END PUBLIC KEY-----"""
    }

    # Convert actor to dictionary and return as JSON response
    actor_dict = aggregator_actor.to_dict()

    # Add the public key to the actor dictionary explicitly
    actor_dict["publicKey"] = {
        "id": "https://ap.staythepath.lol/aggregator#main-key",
        "owner": "https://ap.staythepath.lol/aggregator",
        "publicKeyPem": """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsAMRvlQ4v5Yex343kKzO
        sBzloZCS8XQVNruXo25adIFVjKH8ovSvp/t86P998ycx3Ea7AH75pc1tc6HoS4TH
        /OZ/masas0QJHfk663pHTQz6RceXPRIHgrx3HNDf1KFNlcZtfiFEhGKEdAjr/Q1y
        q6IgM+jRFyF8QXUHlYNUWoBRNeaYKAvNOPju3ODCTCNaxYJ45VK0Fblftday7Ha1
        BHe3b3X91cCfuFKmPoShiYqI9XueHLdUS7aIcc72PgZOeJputysrv2dDNdnxmiP1
        KAvdke4/4d4LSwMdf43oGspkAP9xk9d91+xNXWe1ywxqj/mkuYf+sn2v3WnvYOEf
        NQIDAQAB
        -----END PUBLIC KEY-----"""
    }

    # Log the full actor dictionary
    app.logger.debug(f"Aggregator JSON response: {json.dumps(actor_dict, indent=2)}")

    return jsonify(actor_dict)



# Shared inbox endpoint definition
@app.route('/shared-inbox', methods=['POST'])
def shared_inbox():
    """
    This endpoint serves as a shared inbox that acts similarly to a webhook.
    It receives activities from multiple sources (actors).
    """
    data = request.get_json()
    app.logger.info("Received POST request to shared inbox")
    app.logger.debug(f"Received activity data: {json.dumps(data, indent=2)}")

    try:
        # Parse as ActivityPub Activity
        activity = Activity.from_dict(data)

        if activity.ap_type == "Create":
            # Handle Create Activity (e.g., a new post)
            app.logger.info(f"Received post from actor {activity.ap_actor}")
            app.logger.debug(f"Post content: {activity.ap_object.get('content', 'No content provided')}")

        elif activity.ap_type == "Follow":
            # Handle Follow Requests if needed (maybe to track followers)
            actor = activity.ap_actor
            app.logger.info(f"Received follow request from: {actor}")

    except Exception as e:
        app.logger.error(f"Failed to parse activity: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "accepted"}), 202

@app.route('/notify-actors', methods=['POST'])
def notify_actors():
    """
    Notify the actors we want to track about our shared inbox.
    This will prompt them to use the aggregator's shared inbox for updates.
    """
    for actor_url in tracked_actors:
        try:
            # Fetch actor information
            response = requests.get(actor_url, headers={"Accept": "application/json"})
            if response.status_code == 200:
                actor_info = response.json()
                app.logger.info(f"Successfully fetched actor info for {actor_url}")

                # Prepare to inform the actor about the shared inbox
                announce_activity = {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Announce",
                    "actor": "https://ap.staythepath.lol/aggregator",
                    "object": {
                        "type": "Service",
                        "name": "Cheed Aggregator Service",
                        "inbox": "https://ap.staythepath.lol/shared-inbox"
                    },
                    "to": [actor_url],
                    "published": datetime.utcnow().isoformat() + "Z",
                }

                # Log the activity that will be sent
                app.logger.debug(f"Announce activity: {json.dumps(announce_activity, indent=2)}")

                # Prepare the headers
                date_header = formatdate(timeval=None, localtime=False, usegmt=True)
                digest_content = hashlib.sha256(json.dumps(announce_activity).encode('utf-8')).digest()
                digest_header = "SHA-256=" + base64.b64encode(digest_content).decode('utf-8')

                headers = {
                    "Content-Type": "application/activity+json",
                    "Accept": "application/activity+json",
                    "Date": date_header,
                    "Digest": digest_header,
                    "Host": "mstdn.social"
                }

                # Construct the signature string
                request_target = "(request-target): post /users/staythepath/inbox"
                host_header = f"host: mstdn.social"
                date_header_str = f"date: {date_header}"
                digest_header_str = f"digest: {digest_header}"

                signature_string = "\n".join([request_target, host_header, date_header_str, digest_header_str])

                # Sign the string with the private key
                with open("private.pem", "r") as key_file:
                    private_key = key_file.read()

                key = RSA.importKey(private_key)
                signer = PKCS1_v1_5.new(key)
                hashed_signature_string = SHA256.new(signature_string.encode('utf-8'))
                signature = signer.sign(hashed_signature_string)
                signature_base64 = base64.b64encode(signature).decode('utf-8')

                # Construct the Signature header
                signature_header = (
                    f'keyId="https://ap.staythepath.lol/aggregator#main-key",'
                    f'headers="(request-target) host date digest",'
                    f'signature="{signature_base64}"'
                )

                headers['Signature'] = signature_header

                # Log the signature header before making the request
                app.logger.debug(f"Signature header: {signature_header}")

                # Send the announce activity to the actor's inbox
                target_inbox = actor_info.get("inbox")
                if target_inbox:
                    announce_response = requests.post(target_inbox, json=announce_activity, headers=headers)
                    if announce_response.status_code in [200, 202]:
                        app.logger.info(f"Successfully announced shared inbox to {actor_url}")
                    else:
                        app.logger.error(f"Failed to announce shared inbox, status code: {announce_response.status_code}")
                        app.logger.error(f"Response: {announce_response.text}")
                else:
                    app.logger.error(f"No inbox found for actor: {actor_url}")

            else:
                app.logger.error(f"Failed to fetch actor info from {actor_url}, status code: {response.status_code}")

        except Exception as e:
            app.logger.error(f"Error fetching or notifying actor {actor_url}: {str(e)}")

    return jsonify({"status": "notified"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
