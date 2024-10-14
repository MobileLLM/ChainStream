from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Difficulty_Task_tag(Enum):
    Easy = "Single-step"
    Medium = "Multi-step"
    Hard = "Multi-step"


class Domain_Task_tag(Enum):
    Health = "Health"
    Location = "Location"
    Weather = "Weather"
    Interpersonal_relationship = "Social"
    Daily_information = "Daily Info"
    # Travel = "Travel"
    Office = "Office"
    # Hospital = "Hospital"
    # School = "School"
    Home = "Home"
    # Traffic = "Traffic"
    # Shop = "Shop"
    Activity = "Activity"
    # Other = "Other"


class Modality_Task_tag(Enum):
    Audio = "Audio"
    Video = "Video"
    Text = "Text"
    Image = "Image"
    GPS_Sensor = "GPS"
    Gas_Sensor = "Gas"
    Health_Sensor = "Health Monitor"
    Wifi_Sensor = "Wifi"
    Weather_Sensor = "Weather"
    Activity_Sensor = "Activity Monitor"
    Light_Sensor = "Light"


class TaskTag(BaseModel):
    difficulty: Optional[str] = None
    domain: Optional[str] = None
    modality: Optional[str] = None
    scene: Optional[str] = None
