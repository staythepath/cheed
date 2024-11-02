import hashlib
import base64
import logging
from httpsig.requests_auth import HTTPSignatureAuth
from email.utils import formatdate
import json
import requests

logger = logging.getLogger(__name__)

def send_follow_request(target_actor_url, service_actor_url, inbox_url):
    """Send a follow request from the service actor to the target actor, with HTTP signature."""

    # Construct the follow activity
    follow_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"{service_actor_url}#follow",
        "type": "Follow",
        "actor": service_actor_url,
        "object": target_actor_url
    }

    # Generate Digest header using SHA-256
    body = json.dumps(follow_activity)
    digest = "SHA-256=" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode("utf-8")

    # Headers including Date, Host, and Digest
    headers = {
        "Content-Type": "application/activity+json",
        "Date": formatdate(timeval=None, localtime=False, usegmt=True),
        "Host": "mstdn.social",
        "Digest": digest
    }

    # Load the private key for signing and log a hash for verification
    try:
        with open("activitypub_server/private.pem", "rb") as key_file:
            private_key = key_file.read()
            logger.info(f"Private key hash: {hashlib.sha256(private_key).hexdigest()}")
    except Exception as e:
        logger.error(f"Error reading private key: {e}")
        return

    # Create HTTP Signature Authentication, specifying headers to sign
    auth = HTTPSignatureAuth(
        key_id=f"{service_actor_url}#main-key",
        secret=private_key,
        algorithm="rsa-sha256",
        headers=["(request-target)", "host", "date", "digest"]  # Ensure exact order
    )

    # Prepare the request to inspect headers and signing
    with requests.Session() as session:
        request = requests.Request("POST", inbox_url, data=body, headers=headers, auth=auth)
        prepared = session.prepare_request(request)

        # Log the full details of the outgoing request for verification
        logger.info("Sending follow request with the following details:")
        logger.info(f"URL: {prepared.url}")
        logger.info("Headers:")
        for header, value in prepared.headers.items():
            logger.info(f"  {header}: {value}")
        logger.info(f"Body: {body}")

        # Send the request and log response
        response = session.send(prepared)
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        logger.info(f"Response content: {response.text}")
        return response.status_code
