from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Difficulty_Task_tag(Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"


class Domain_Task_tag(Enum):
    Health = "Health"
    Location = "Location"
    Weather = "Weather"
    Interpersonal_relationship = "Interpersonal_relationship"
    Daily_information = "Daily_information"
    Living = "Living"
    # Travel = "Travel"
    Office = "Office"
    # Hospital = "Hospital"
    # School = "School"
    # Home = "Home"
    # Traffic = "Traffic"
    # Shop = "Shop"
    Activity = "Activity"
    # Other = "Other"


class Modality_Task_tag(Enum):
    Audio = "Audio"
    Video = "Video"
    Text = "Text"
    Image = "Image"
    GPS_Sensor = "GPS_Sensor"
    Gas_Sensor = "Gas_Sensor"
    Health_Sensor = "Health_Sensor"
    Wifi_Sensor = "Wifi_Sensor"
    Weather_Sensor = "Weather_Sensor"
    Activity_Sensor = "Activity_Sensor"


class TaskTag(BaseModel):
    difficulty: Optional[str] = None
    domain: Optional[str] = None
    modality: Optional[str] = None
    scene: Optional[str] = None
