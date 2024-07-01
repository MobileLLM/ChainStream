from tasks.sms_task import *
from tasks.arxiv_task import *
from tasks.email_task import *
from tasks.news_task import *
from tasks.stock_task import *
from tasks.daily_dialogue_task import *
from tasks.gps_task import *
from tasks.twitter_task import *
from tasks.gps_task import *

ALL_TASKS = {'ArxivAbstractTask': ArxivAbstractConfig,
             'ArxivAlgorithmTask': ArxivAlgorithmConfig,
             'ArxivApproachTask': ArxivApproachConfig,
             'ArxivAuthorsTask': ArxivAuthorsConfig,
             'ArxivCommentsTask': ArxivCommentsConfig,
             'ArxivDateTask': ArxivDateConfig,
             'ArxivImplementationTask': ArxivImplementationConfig,
             'ArxivReferenceTask': ArxivReferenceConfig,
             'ArxivProblemsTask': ArxivProblemsConfig,
             'ArxivStageTask': ArxivStageConfig,
             'ArxivTopicTask': ArxivTopicConfig,
             'ArxivWebsiteTask': ArxivWebsiteConfig,
             'MessageContentTask': MessageContentConfig,
             'MessageEmotionTask': MessageEmotionConfig,
             'MessageLanguageTask': MessageLanguageConfig,
             'MessageSummaryTask': MessageSummaryConfig,
             'MessageTimeTask': MessageTimeConfig,
             'EmailDateTask': EmailDateConfig,
             'EmailEmotionTask': EmailEmotionConfig,
             'EmailReceiverTask': EmailReceiverConfig,
             'EmailReplyTask': EmailReplyConfig,
             'EmailSenderTask': EmailSenderConfig,
             'EmailSubjectTask': EmailSubjectConfig,
             'EmailSummaryTask': EmailSummaryConfig,
             'NewsAuthorsTask': NewsAuthorsConfig,
             'NewsCategoryTask': NewsCategoryConfig,
             'NewsDateTask': NewsDateConfig,
             'NewsDescriptionTask': NewsDescriptionConfig,
             'NewsLinkTask': NewsLinkConfig,
             'NewsPeopleTask': NewsPeopleConfig,
             'NewsPlaceTask': NewsPlaceConfig,
             'NewsTitleTask': NewsTitleConfig,
             'StockInfoTask': StockInfoConfig,
             'StockPurchaseTask': StockPurchaseConfig,
             'StockRecommendTask': StockRecommendConfig,
             'StockSellTask': StockSellConfig,
             'DialogueDailyTask': DialogueDailyConfig,
             'DialogueEmotionTask': DialogueEmotionConfig,
             'DialogueIdentityTask': DialogueIdentityConfig,
             'DialoguePlaceTask': DialoguePlaceConfig,
             'DialogueTimeTask': DialogueTimeConfig,
             'DialogueTopicTask': DialogueTopicConfig,
             'GPSCapitalTask': GPSCapitalConfig,
             'GPSContinentTask': GPSContinentConfig,
             'GPSCountryTask': GPSCountryConfig,
             'GPSLatitudeTask': GPSLatitudeConfig,
             'GPSLongitudeTask': GPSLongitudeConfig,
             'RetweetCountTask': RetweetCountConfig,
             'TweetAirlineTask': TweetAirlineConfig,
             'TweetLocationTask': TweetLocationConfig,
             'TweetNegativeReasonTask': TweetNegativeReasonConfig,
             'TweetSentimentTask': TweetSentimentConfig,
             'TweetTextTask': TweetTextConfig,
             'TweetTimeTask': TweetTimeConfig,
             'TweetTimezoneTask': TweetTimezoneConfig,
             'TweetUserTask': TweetUserConfig
             }

