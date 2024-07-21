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
from .email_task import EmailTask5
from .news_task  import NewsTask1
from .news_task  import NewsTask2
from .news_task  import NewsTask3
from .news_task  import NewsTask4
from .stock_task import StockTask1
from .arxiv_task import ArxivTask1
from .arxiv_task import ArxivTask2
from .arxiv_task import ArxivTask3
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
ALL_TASKS = {
    EmailTask1.__name__: EmailTask1,
    EmailTask2.__name__: EmailTask2,
    EmailTask3.__name__: EmailTask3,
    EmailTask4.__name__: EmailTask4,
    EmailTask5.__name__: EmailTask5,
    NewsTask1.__name__: NewsTask1,
    NewsTask2.__name__: NewsTask2,
    NewsTask3.__name__: NewsTask3,
    NewsTask4.__name__: NewsTask4,
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
    HealthTask5.__name__: HealthTask5
}


def get_task_batch():
    return ALL_TASKS
