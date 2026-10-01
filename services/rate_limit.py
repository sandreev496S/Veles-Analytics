import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


def _redis_enabled():
    return bool(UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN)


def _redis_request(command):
    response = requests.post(
        UPSTASH_REDIS_REST_URL,
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"},
        json=command,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def _session_rate_limit(action_name, limit, window_seconds):
    now = time.time()
    key = f"rate_limit_{action_name}"

    events = st.session_state.get(key, [])
    events = [timestamp for timestamp in events if now - timestamp < window_seconds]

    if len(events) >= limit:
        wait_seconds = int(window_seconds - (now - events[0]))
        return False, wait_seconds

    events.append(now)
    st.session_state[key] = events
    return True, 0


def check_rate_limit(action_name, limit, window_seconds, user_id=None):
    if not user_id:
        user_id = "anonymous"

    if not _redis_enabled():
        return _session_rate_limit(action_name, limit, window_seconds)

    bucket = int(time.time() // window_seconds)
    key = f"rate:{user_id}:{action_name}:{bucket}"

    count_result = _redis_request(["INCR", key])
    count = int(count_result.get("result", 0))

    if count == 1:
        _redis_request(["EXPIRE", key, window_seconds])

    if count > limit:
        ttl_result = _redis_request(["TTL", key])
        wait_seconds = int(ttl_result.get("result", window_seconds))
        return False, wait_seconds

    return True, 0


def enforce_rate_limit(action_name, limit, window_seconds, user_id=None):
    allowed, wait_seconds = check_rate_limit(
        action_name=action_name,
        limit=limit,
        window_seconds=window_seconds,
        user_id=user_id,
    )

    if not allowed:
        st.error(f"Rate limit reached. Try again in {wait_seconds} seconds.")
        st.stop()
