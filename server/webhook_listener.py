from flask import Flask, request, abort
import json
import sys
import hmac
import hashlib
import subprocess
sys.path.append("../dc_public_transport")
from settings import GITHUB_WEBHOOK_SECRET
# this is ANOTHER test change, to see if the webhook from github is successfully delivered after merging to main

app = Flask(__name__)

def verify_signature(payload, signature_header):
    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature or not verify_signature(request.data, signature):
        abort(403)

    payload_data = json.loads(request.data)
    ref = payload_data.get("ref", "")
    if ref != "refs/heads/main":
        return "Ignored (not main)", 200

    repo_dir = "/home/ubuntu/projects/dc_public_transport"
    subprocess.run(["git", "-C", repo_dir, "pull"], check=True)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
