from datetime import datetime
import json
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