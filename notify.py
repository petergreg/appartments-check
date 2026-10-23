#!/usr/bin/env python3
import os, requests


def send(title, message, click_url=None):
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        return
    headers = {"Title": title.encode("utf-8")}
    if click_url:
        headers["Click"] = click_url
    try:
        requests.post(f"https://ntfy.sh/{topic}", data=message.encode("utf-8"), headers=headers, timeout=20)
    except requests.RequestException as e:
        print(f"[notify] ERREUR : {e}")
