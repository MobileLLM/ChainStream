from enum import Enum
from pydantic import BaseModel


class Difficulty_Task_tag(Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"


class Domain_Task_tag(Enum):
    Health = "Health"
    Work = "Work"
    Location = "Location"
    Weather = "Weather"
    Interpersonal_relationship = "Interpersonal_relationship"
    Activity = "Activity"
    Daily_information = "Daily_information"
    Living = "Living"


class Scene_Task_tag(Enum):
    Travel = "Travel"
    Office = "Office"
    Hospital = "Hospital"
    School = "School"
    Home = "Home"
    Traffic = "Traffic"
    Shop = "Shop"
    Exercise = "Exercise"
    Other = "Other"


class Modality_Task_tag(Enum):
    Audio = "Audio"
    Video = "Video"
    Text = "Text"
    Image = "Image"


class TaskTag(BaseModel):
    difficulty = None
    domain = None
    modality = None
    scene = None
