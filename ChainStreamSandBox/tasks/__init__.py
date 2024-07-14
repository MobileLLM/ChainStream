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
from .news_task  import NewsTask1
ALL_TASKS = {
    # EmailTask1.__name__: EmailTask1,
    # EmailTask2.__name__: EmailTask2,
    EmailTask4.__name__: EmailTask4
    # NewsTask1.__name__: NewsTask1
}


def get_task_batch():
    return ALL_TASKS
