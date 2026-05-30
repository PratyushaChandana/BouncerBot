import os
import json
import requests
from datetime import datetime
from core.logger import get_logger

logger = get_logger("box_rest")

BOX_UPLOAD_URL = "https://upload.box.com/api/2.0/files/content"
BOX_VERSION_UPLOAD_URL = "https://upload.box.com/api/2.0/files/{file_id}/content"
BOX_SEARCH_URL = "https://api.box.com/2.0/search"


# ---------------------------------------------------------
# DEBUG HELPER — prints EVERYTHING about the request
# ---------------------------------------------------------
def debug_request_info(url, headers, files):
    logger.debug("----- BOX DEBUG REQUEST -----")
    logger.debug(f"URL: {url}")
    logger.debug(f"Headers: {headers}")

    for key, value in files.items():
        if isinstance(value, tuple):
            name, content, mime = value
            size = len(content) if content else 0
            logger.debug(f"Field: {key} | Filename: {name} | MIME: {mime} | Size: {size}")
        else:
            logger.debug(f"Field: {key} | Value: {value}")

    logger.debug("----- END BOX DEBUG REQUEST -----")


def upload_structured_log(session_id, user_message, ai_message, verdict):
    """
    Stores structured JSON logs in Box:
    - One file per session
    - Append user + AI messages
    - Only user messages include metadata
    """

    logger.info(f"Appending structured log for session {session_id}")

    developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
    folder_id = os.getenv("BOX_FOLDER_ID", "0")

    if not developer_token:
        logger.error("Missing BOX_DEVELOPER_TOKEN")
        return

    filename = f"session_{session_id}.json"
    headers = {"Authorization": f"Bearer {developer_token}"}

    # ---------------------------------------------------------
    # STEP 1 — Check if file already exists in Box
    # ---------------------------------------------------------
    search_params = {
        "query": filename,
        "type": "file",
        "content_types": "name",
        "ancestor_folder_ids": folder_id
    }

    search_resp = requests.get(BOX_SEARCH_URL, headers=headers, params=search_params)

    file_id = None
    if search_resp.status_code == 200:
        items = search_resp.json().get("entries", [])
        if items:
            file_id = items[0]["id"]

    # ---------------------------------------------------------
    # STEP 2 — Build new log entry
    # ---------------------------------------------------------
    timestamp = datetime.utcnow().isoformat() + "Z"

    user_entry = {
        "timestamp": timestamp,
        "role": "user",
        "text": user_message,
        "verdict": verdict
    }

    ai_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "role": "assistant",
        "text": ai_message
    }

    # ---------------------------------------------------------
    # STEP 3 — If file exists → download, append, upload new version
    # ---------------------------------------------------------
    if file_id:
        logger.info(f"Found existing session log: {filename} (file_id={file_id})")

        # Download existing file
        download_url = f"https://api.box.com/2.0/files/{file_id}/content"
        existing_resp = requests.get(download_url, headers=headers)

        if existing_resp.status_code == 200:
            log_data = json.loads(existing_resp.text)
        else:
            logger.error(f"Failed to download existing log: {existing_resp.text}")
            return

        # Append new entries
        log_data["messages"].append(user_entry)
        log_data["messages"].append(ai_entry)

        # Upload new version
        files = {
            "attributes": (None, json.dumps({
                "name": filename,
                "parent": {"id": folder_id}
            }), "application/json"),

            "parent_id": (None, str(folder_id), "text/plain"),

            "file": (filename, json.dumps(log_data).encode("utf-8"), "application/json")
        }

        version_url = BOX_VERSION_UPLOAD_URL.format(file_id=file_id)

        debug_request_info(version_url, headers, files)

        version_resp = requests.post(version_url, headers=headers, files=files)

        logger.info(f"BOX UPDATE STATUS: {version_resp.status_code}")
        logger.debug(f"BOX UPDATE RESPONSE: {version_resp.text}")

        if version_resp.status_code in (200, 201):
            logger.info(f"Updated session log: {filename}")
        else:
            logger.error(f"Failed to upload new version: {version_resp.text}")

        return

    # ---------------------------------------------------------
    # STEP 4 — If file does NOT exist → create new JSON log
    # ---------------------------------------------------------
    logger.info(f"Creating new session log: {filename}")

    new_log = {
        "session_id": session_id,
        "created_at": timestamp,
        "messages": [user_entry, ai_entry]
    }

    files = {
        "attributes": (None, json.dumps({
            "name": filename,
            "parent": {"id": folder_id}
        }), "application/json"),

        "parent_id": (None, str(folder_id), "text/plain"),

        "file": (filename, json.dumps(new_log).encode("utf-8"), "application/json")
    }

    debug_request_info(BOX_UPLOAD_URL, headers, files)

    create_resp = requests.post(BOX_UPLOAD_URL, headers=headers, files=files)

    logger.info(f"BOX CREATE STATUS: {create_resp.status_code}")
    logger.debug(f"BOX CREATE RESPONSE: {create_resp.text}")

    if create_resp.status_code in (200, 201):
        logger.info(f"Created new session log in Box: {filename}")
    else:
        logger.error(f"Failed to create session log: {create_resp.text}")
