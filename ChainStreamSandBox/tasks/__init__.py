# from tasks.old_tasks.sms_task import *
# from tasks.old_tasks.arxiv_task import *
# from tasks.old_tasks.email_task import *
# from tasks.old_tasks.news_task import *
# from tasks.old_tasks.stock_task import *
# from tasks.old_tasks.daily_dialogue_task import *
# from tasks.old_tasks.gps_task import *
# from tasks.old_tasks.twitter_task import *
# from tasks.old_tasks.gps_task import *
# from .task_config_base import TaskConfigBase
#
# ALL_TASKS_OLD = {'ArxivAbstractTask': ArxivAbstractConfig,
#                  'ArxivAlgorithmTask': ArxivAlgorithmConfig,
#                  'ArxivApproachTask': ArxivApproachConfig,
#                  'ArxivAuthorsTask': ArxivAuthorsConfig,
#                  'ArxivCommentsTask': ArxivCommentsConfig,
#                  'ArxivDateTask': ArxivDateConfig,
#                  'ArxivImplementationTask': ArxivImplementationConfig,
#                  'ArxivReferenceTask': ArxivReferenceConfig,
#                  'ArxivProblemsTask': ArxivProblemsConfig,
#                  'ArxivStageTask': ArxivStageConfig,
#                  'ArxivTopicTask': ArxivTopicConfig,
#                  'ArxivWebsiteTask': ArxivWebsiteConfig,
#                  'MessageContentTask': MessageContentConfig,
#                  'MessageEmotionTask': MessageEmotionConfig,
#                  'MessageLanguageTask': MessageLanguageConfig,
#                  'MessageSummaryTask': MessageSummaryConfig,
#                  'MessageTimeTask': MessageTimeConfig,
#                  'EmailDateTask': EmailDateConfig,
#                  'EmailEmotionTask': EmailEmotionConfig,
#                  'EmailReceiverTask': EmailReceiverConfig,
#                  'EmailReplyTask': EmailReplyConfig,
#                  'EmailSenderTask': EmailSenderConfig,
#                  'EmailSubjectTask': EmailSubjectConfig,
#                  'EmailSummaryTask': EmailSummaryConfig,
#                  'NewsAuthorsTask': NewsAuthorsConfig,
#                  'NewsCategoryTask': NewsCategoryConfig,
#                  'NewsDateTask': NewsDateConfig,
#                  'NewsDescriptionTask': NewsDescriptionConfig,
#                  'NewsLinkTask': NewsLinkConfig,
#                  'NewsPeopleTask': NewsPeopleConfig,
#                  'NewsPlaceTask': NewsPlaceConfig,
#                  'NewsTitleTask': NewsTitleConfig,
#                  'StockInfoTask': StockInfoConfig,
#                  'StockPurchaseTask': StockPurchaseConfig,
#                  'StockRecommendTask': StockRecommendConfig,
#                  'StockSellTask': StockSellConfig,
#                  'DialogueDailyTask': DialogueDailyConfig,
#                  'DialogueEmotionTask': DialogueEmotionConfig,
#                  'DialogueIdentityTask': DialogueIdentityConfig,
#                  'DialoguePlaceTask': DialoguePlaceConfig,
#                  'DialogueTimeTask': DialogueTimeConfig,
#                  'DialogueTopicTask': DialogueTopicConfig,
#                  'GPSCapitalTask': GPSCapitalConfig,
#                  'GPSContinentTask': GPSContinentConfig,
#                  'GPSCountryTask': GPSCountryConfig,
#                  'GPSLatitudeTask': GPSLatitudeConfig,
#                  'GPSLongitudeTask': GPSLongitudeConfig,
#                  'RetweetCountTask': RetweetCountConfig,
#                  'TweetAirlineTask': TweetAirlineConfig,
#                  'TweetLocationTask': TweetLocationConfig,
#                  'TweetNegativeReasonTask': TweetNegativeReasonConfig,
#                  'TweetSentimentTask': TweetSentimentConfig,
#                  'TweetTextTask': TweetTextConfig,
#                  'TweetTimeTask': TweetTimeConfig,
#                  'TweetTimezoneTask': TweetTimezoneConfig,
#                  'TweetUserTask': TweetUserConfig,
#                  'LandmarkLocationTask': LandmarkLocationConfig,
#                  'LandmarkTypeTask': LandmarkTypeConfig,
#                  'LandmarkTimeTask': LandmarkTimeConfig,
#                  'LandmarkNeighborhoodTask': LandmarkNeighborhoodConfig,
#                  'LandmarkNameTask': LandmarkNameConfig,
#                  'LandmarkFloorsTask': LandmarkFloorsConfig,
#                  'BuildingElectricityTask': BuildingElectricityConfig,
#                  'BuildingGHGEmissionsTask': BuildingGHGEmissionsConfig,
#                  'BuildingNaturalGasTask': BuildingNaturalGasConfig
#                  }

from .email_task import EmailTask1
from .email_task import EmailTask2
from .email_task import EmailTask3
from .email_task import EmailTask4
from .email_task import OldEmailTask1
from .email_task import OldEmailTask2
from .email_task import OldEmailTask3
from .email_task import OldEmailTask4
from .email_task import OldEmailTask5
from .email_task import OldEmailTask6
from .email_task import OldEmailTask7
from .news_task import NewsTask1
from .news_task import NewsTask2
from .news_task import NewsTask3
from .news_task import NewsTask4
from .news_task import NewsTask5
from .news_task import OldNewsTask1
from .news_task import OldNewsTask2
from .news_task import OldNewsTask3
from .news_task import OldNewsTask4
from .news_task import OldNewsTask5
from .news_task import OldNewsTask6
from .news_task import OldNewsTask7
from .news_task import OldNewsTask8
from .stock_task import StockTask1
from .stock_task import OldStockTask2
from .stock_task import OldStockTask3
from .stock_task import OldStockTask4
from .arxiv_task import ArxivTask1
from .arxiv_task import ArxivTask2
from .arxiv_task import ArxivTask3
from .arxiv_task import OldArxivTask1
from .arxiv_task import OldArxivTask2
from .arxiv_task import OldArxivTask3
from .arxiv_task import OldArxivTask4
from .arxiv_task import OldArxivTask5
from .arxiv_task import OldArxivTask6
from .arxiv_task import OldArxivTask7
from .arxiv_task import OldArxivTask8
from .arxiv_task import OldArxivTask9
from .arxiv_task import OldArxivTask10
from .arxiv_task import OldArxivTask11
from .arxiv_task import OldArxivTask12
from .sensor_task import GPSTask1
from .sensor_task import GPSTask2
from .sensor_task import GPSTask3
from .sensor_task import WeatherTask1
from .sensor_task import WeatherTask2
from .sensor_task import WeatherTask3
from .sensor_task import WeatherTask4
from .sensor_task import HealthTask1
from .sensor_task import HealthTask2
from .sensor_task import HealthTask3
from .sensor_task import HealthTask4
from .sensor_task import HealthTask5
from .sensor_task import OldGPSTask1
from .sensor_task import OldGPSTask2
from .sensor_task import OldGPSTask3
from .sensor_task import OldGPSTask4
from .sensor_task import OldGPSTask5
from .sensor_task import OldGPSTask6
from .sensor_task import OldGPSTask7
from .sensor_task import OldGPSTask8
from .sensor_task import OldGPSTask9
from .sensor_task import OldGPSTask10
from .sensor_task import OldGPSTask11
from .sensor_task import OldGPSTask12
from .sensor_task import OldGPSTask13
from .sensor_task import OldGPSTask14
from .sensor_task import OldHealthTask1
from .sensor_task import OldHealthTask2
from .sensor_task import OldHealthTask3
from .sensor_task import OldHealthTask4
from .sensor_task import OldHealthTask5
from .sensor_task import OldHealthTask6
from .sensor_task import OldHealthTask7
from .sensor_task import OldHealthTask8
from .sensor_task import OldHealthTask9
from .sensor_task import OldHealthTask10
from .sensor_task import OldHealthTask11
from .sensor_task import OldHealthTask12
from .sensor_task import OldHealthTask13
from .sensor_task import OldHealthTask14
from .sensor_task import OldHealthTask15
from .sensor_task import OldWeatherTask1
from .sensor_task import OldWeatherTask2
from .sensor_task import OldWeatherTask3
from .sensor_task import OldWeatherTask4
from .sensor_task import OldWeatherTask5
from .sensor_task import OldWeatherTask6
from .sensor_task import OldWifiTask1
from .sensor_task import OldWifiTask2
from .sensor_task import OldWifiTask3
from .sensor_task import OldWifiTask4
from .sensor_task import OldWifiTask5
from .desktop_ui_task import ImageTask1
from .ego_4d_task import VideoTask1
from .ego_4d_task import VideoTask2
from .ego_4d_task import VideoTask3
from .three_person_task import VideoTask4
from .three_person_task import VideoTask5
from .three_person_task import VideoTask6
from .github_task import GithubTask1
from .github_task import GithubTask2
from .github_task import GithubTask3
from .github_task import GithubTask4
from .daily_dialogue_task import OldDialogueTask2
from .daily_dialogue_task import OldDialogueTask3
from .daily_dialogue_task import OldDialogueTask4
from .daily_dialogue_task import OldDialogueTask5
from .daily_dialogue_task import OldDialogueTask6
from .sms_task import OldMessageTask1
from .sms_task import OldMessageTask2
from .sms_task import OldMessageTask3
from .sms_task import OldMessageTask4
from .sms_task import OldMessageTask5
from .twitter_task import OldTweetTask1
from .twitter_task import OldTweetTask2
from .twitter_task import OldTweetTask3
from .twitter_task import OldTweetTask4
from .twitter_task import OldTweetTask5
from .twitter_task import OldTweetTask6
from .twitter_task import OldTweetTask7
from .twitter_task import OldTweetTask8
from .twitter_task import OldTweetTask9
from .activity_task import OldActivityTask1
from .activity_task import OldActivityTask2
from .activity_task import OldActivityTask3
from .activity_task import OldActivityTask4
from .multi_task import EmailTaskTest
from .multi_task import MessageStockTask
from .multi_task import WorkReminderTask
from .multi_task import CatFoodTask
from .multi_task import TravelTask
from .multi_task import WaterFlowerTask
from .multi_task import KitchenSafetyTask
from .multi_task import CloseWindowTask
from .multi_task import RemindDriverTask
from .multi_task import StudentInClassTask
from .multi_task import ReadingLightTask
from .multi_task import WaitingRoomTask
from .multi_task import ShopStockTask
from .multi_task import TripMusicTask

ALL_TASKS = {
    EmailTask1.__name__: EmailTask1,
    EmailTask2.__name__: EmailTask2,
    EmailTask3.__name__: EmailTask3,
    EmailTask4.__name__: EmailTask4,
    NewsTask1.__name__: NewsTask1,
    NewsTask2.__name__: NewsTask2,
    NewsTask3.__name__: NewsTask3,
    NewsTask4.__name__: NewsTask4,
    NewsTask5.__name__: NewsTask5,
    StockTask1.__name__: StockTask1,
    ArxivTask1.__name__: ArxivTask1,
    ArxivTask2.__name__: ArxivTask2,
    ArxivTask3.__name__: ArxivTask3,
    GPSTask1.__name__: GPSTask1,
    GPSTask2.__name__: GPSTask2,
    GPSTask3.__name__: GPSTask3,
    WeatherTask1.__name__: WeatherTask1,
    WeatherTask2.__name__: WeatherTask2,
    WeatherTask3.__name__: WeatherTask3,
    WeatherTask4.__name__: WeatherTask4,
    HealthTask1.__name__: HealthTask1,
    HealthTask2.__name__: HealthTask2,
    HealthTask3.__name__: HealthTask3,
    HealthTask4.__name__: HealthTask4,
    HealthTask5.__name__: HealthTask5,
    ImageTask1.__name__: ImageTask1,
    VideoTask1.__name__: VideoTask1,
    VideoTask2.__name__: VideoTask2,
    VideoTask3.__name__: VideoTask3,
    VideoTask4.__name__: VideoTask4,
    VideoTask5.__name__: VideoTask5,
    VideoTask6.__name__: VideoTask6,
    GithubTask1.__name__: GithubTask1,
    GithubTask2.__name__: GithubTask2,
    GithubTask3.__name__: GithubTask3,
    GithubTask4.__name__: GithubTask4,
    EmailTaskTest.__name__: EmailTaskTest,
    MessageStockTask.__name__: MessageStockTask,
    WorkReminderTask.__name__: WorkReminderTask,
    TravelTask.__name__: TravelTask,
    CatFoodTask.__name__: CatFoodTask,
    WaterFlowerTask.__name__: WaterFlowerTask,
    KitchenSafetyTask.__name__: KitchenSafetyTask,
    CloseWindowTask.__name__: CloseWindowTask,
    RemindDriverTask.__name__: RemindDriverTask,
    StudentInClassTask.__name__: StudentInClassTask,
    ReadingLightTask.__name__: ReadingLightTask,
    WaitingRoomTask.__name__: WaitingRoomTask,
    ShopStockTask.__name__: ShopStockTask,
    TripMusicTask.__name__: TripMusicTask,
    OldArxivTask1.__name__: OldArxivTask1,
    OldArxivTask2.__name__: OldArxivTask2,
    OldArxivTask3.__name__: OldArxivTask3,
    OldArxivTask4.__name__: OldArxivTask4,
    OldArxivTask5.__name__: OldArxivTask5,
    OldArxivTask6.__name__: OldArxivTask6,
    OldArxivTask7.__name__: OldArxivTask7,
    OldArxivTask8.__name__: OldArxivTask8,
    OldArxivTask9.__name__: OldArxivTask9,
    OldArxivTask10.__name__: OldArxivTask10,
    OldArxivTask11.__name__: OldArxivTask11,
    OldArxivTask12.__name__: OldArxivTask12,
    OldDialogueTask2.__name__: OldDialogueTask2,
    OldDialogueTask3.__name__: OldDialogueTask3,
    OldDialogueTask4.__name__: OldDialogueTask4,
    OldDialogueTask5.__name__: OldDialogueTask5,
    OldDialogueTask6.__name__: OldDialogueTask6,
    OldEmailTask1.__name__: OldEmailTask1,
    OldEmailTask2.__name__: OldEmailTask2,
    OldEmailTask3.__name__: OldEmailTask3,
    OldEmailTask4.__name__: OldEmailTask4,
    OldEmailTask5.__name__: OldEmailTask5,
    OldEmailTask6.__name__: OldEmailTask6,
    OldEmailTask7.__name__: OldEmailTask7,
    OldGPSTask1.__name__: OldGPSTask1,
    OldGPSTask2.__name__: OldGPSTask2,
    OldGPSTask3.__name__: OldGPSTask3,
    OldGPSTask4.__name__: OldGPSTask4,
    OldGPSTask5.__name__: OldGPSTask5,
    OldGPSTask6.__name__: OldGPSTask6,
    OldGPSTask7.__name__: OldGPSTask7,
    OldGPSTask8.__name__: OldGPSTask8,
    OldGPSTask9.__name__: OldGPSTask9,
    OldGPSTask10.__name__: OldGPSTask10,
    OldGPSTask11.__name__: OldGPSTask11,
    OldGPSTask12.__name__: OldGPSTask12,
    OldGPSTask13.__name__: OldGPSTask13,
    OldGPSTask14.__name__: OldGPSTask14,
    OldNewsTask1.__name__: OldNewsTask1,
    OldNewsTask2.__name__: OldNewsTask2,
    OldNewsTask3.__name__: OldNewsTask3,
    OldNewsTask4.__name__: OldNewsTask4,
    OldNewsTask5.__name__: OldNewsTask5,
    OldNewsTask6.__name__: OldNewsTask6,
    OldNewsTask7.__name__: OldNewsTask7,
    OldNewsTask8.__name__: OldNewsTask8,
    OldMessageTask1.__name__: OldMessageTask1,
    OldMessageTask2.__name__: OldMessageTask2,
    OldMessageTask3.__name__: OldMessageTask3,
    OldMessageTask4.__name__: OldMessageTask4,
    OldMessageTask5.__name__: OldMessageTask5,
    OldTweetTask1.__name__: OldTweetTask1,
    OldTweetTask2.__name__: OldTweetTask2,
    OldTweetTask3.__name__: OldTweetTask3,
    OldTweetTask4.__name__: OldTweetTask4,
    OldTweetTask5.__name__: OldTweetTask5,
    OldTweetTask6.__name__: OldTweetTask6,
    OldTweetTask7.__name__: OldTweetTask7,
    OldTweetTask8.__name__: OldTweetTask8,
    OldTweetTask9.__name__: OldTweetTask9,
    OldActivityTask1.__name__: OldActivityTask1,
    OldActivityTask2.__name__: OldActivityTask2,
    OldActivityTask3.__name__: OldActivityTask3,
    OldActivityTask4.__name__: OldActivityTask4,
    OldHealthTask1.__name__: OldHealthTask1,
    OldHealthTask2.__name__: OldHealthTask2,
    OldHealthTask3.__name__: OldHealthTask3,
    OldHealthTask4.__name__: OldHealthTask4,
    OldHealthTask5.__name__: OldHealthTask5,
    OldHealthTask6.__name__: OldHealthTask6,
    OldHealthTask7.__name__: OldHealthTask7,
    OldHealthTask8.__name__: OldHealthTask8,
    OldHealthTask9.__name__: OldHealthTask9,
    OldHealthTask10.__name__: OldHealthTask10,
    OldHealthTask11.__name__: OldHealthTask11,
    OldHealthTask12.__name__: OldHealthTask12,
    OldHealthTask13.__name__: OldHealthTask13,
    OldHealthTask14.__name__: OldHealthTask14,
    OldHealthTask15.__name__: OldHealthTask15,
    OldWeatherTask1.__name__: OldWeatherTask1,
    OldWeatherTask2.__name__: OldWeatherTask2,
    OldWeatherTask3.__name__: OldWeatherTask3,
    OldWeatherTask4.__name__: OldWeatherTask4,
    OldWeatherTask5.__name__: OldWeatherTask5,
    OldWeatherTask6.__name__: OldWeatherTask6,
    OldWifiTask1.__name__: OldWifiTask1,
    OldWifiTask2.__name__: OldWifiTask2,
    OldWifiTask3.__name__: OldWifiTask3,
    OldWifiTask4.__name__: OldWifiTask4,
    OldWifiTask5.__name__: OldWifiTask5,
    OldStockTask2.__name__: OldStockTask2,
    OldStockTask3.__name__: OldStockTask3,
    OldStockTask4.__name__: OldStockTask4

}


def get_task_batch():
    return ALL_TASKS
