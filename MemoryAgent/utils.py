from datetime import datetime
import json
import urllib
import os
import requests
from response import ChatCompletionResponse
def get_local_time():

    # Get the current time, which will be in the local timezone of the computer
    local_time = datetime.now().astimezone()

    # You may format it as you desire, including AM/PM
    time_str = local_time.strftime("%Y-%m-%d %I:%M:%S %p %Z%z")

    return time_str.strip()

def get_login_event(last_login="Never (first login)", include_location=False, location_name="San Francisco, CA, USA"):
    # Package the message with time and location
    formatted_time = get_local_time()
    packaged_message = {
        "type": "login",
        "last_login": last_login,
        "time": formatted_time,
    }

    if include_location:
        packaged_message["location"] = location_name

    return json.dumps(packaged_message, ensure_ascii=False)

def smart_urljoin(base_url, relative_url):
    """urljoin is stupid and wants a trailing / at the end of the endpoint address, or it will chop the suffix off"""
    if not base_url.endswith("/"):
        base_url += "/"
    return urllib.parse.urljoin(base_url, relative_url)

def verify_first_message_correctness(
    response: ChatCompletionResponse,
) -> bool:
    """Can be used to enforce that the first message always follow one style"""
    return True

def openai_chat_completions_request(url, api_key, data):
    url = smart_urljoin(url, "chat/completions")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    if "functions" in data and data["functions"] is None:
        data.pop("functions")
        data.pop("function_call", None)

    if "tools" in data and data["tools"] is None:
        data.pop("tools")
        data.pop("tool_choice", None)

    print(f"Sending request to {url}")
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"response = {response}")
        response.raise_for_status()  # Raises HTTPError for 4XX/5XX status
        response = response.json()  # convert to dict from string
        print(f"response.json = {response}")
        response = ChatCompletionResponse(**response)
        return response
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., response 4XX, 5XX)
        print(f"Got HTTPError, exception={http_err}, payload={data}")
        raise http_err
    except requests.exceptions.RequestException as req_err:
        # Handle other requests-related errors (e.g., connection error)
        print(f"Got RequestException, exception={req_err}")
        raise req_err
    except Exception as e:
        # Handle other potential errors
        print(f"Got unknown Exception, exception={e}")
        raise e
def package_function_response(was_success, response_string, timestamp=None):
    formatted_time = get_local_time() if timestamp is None else timestamp
    packaged_message = {
        "status": "OK" if was_success else "Failed",
        "message": response_string,
        "time": formatted_time,
    }

    return json.dumps(packaged_message, ensure_ascii=False)
def get_system_text(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"No file found for path={path}")


