# from task_example/*/config.py import all tasks and put them in a list
# import task_config_base

ALL_TASKS = {}
# import all tasks
from tasks.sms_task.sms_task import MessageContentConfig,MessageEmotionConfig,MessageLanguageConfig,MessageSummaryConfig,MessageTimeConfig
from tasks.arxiv_task.arxiv_task import ArxivAlgorithmConfig,ArxivAbstractConfig,ArxivApproachConfig,ArxivAuthorsConfig,ArxivCommentsConfig,ArxivDateConfig,ArxivImplementationConfig,ArxivReferenceConfig,ArxivProblemsConfig,ArxivStageConfig,ArxivTopicConfig,ArxivWebsiteConfig
from tasks.email_task.email_task import EmailDateConfig,EmailEmotionConfig,EmailReceiverConfig,EmailReplyConfig,EmailSenderConfig,EmailSubjectConfig,EmailSummaryConfig
from tasks.news_task.news_task import NewsAuthorsConfig,NewsCategoryConfig,NewsDateConfig,NewsDescriptionConfig,NewsLinkConfig,NewsPeopleConfig,NewsPlaceConfig,NewsTitleConfig
from tasks.stock_task.stock_task import StockInfoConfig,StockPurchaseConfig,StockRecommendConfig,StockSellConfig
from tasks.daily_dialogue_task.daily_dialogue_task import DialogueDailyConfig,DialogueEmotionConfig,DialogueIdentityConfig,DialoguePlaceConfig,DialogueTimeConfig,DialogueTopicConfig
ALL_TASKS['ArxivAbstractTask'] = ArxivAbstractConfig
ALL_TASKS['ArxivAlgorithmTask'] = ArxivAlgorithmConfig
ALL_TASKS['ArxivApproachTask'] = ArxivApproachConfig
ALL_TASKS['ArxivAuthorsTask'] = ArxivAuthorsConfig
ALL_TASKS['ArxivCommentsTask'] = ArxivCommentsConfig
ALL_TASKS['ArxivDateTask'] = ArxivDateConfig
ALL_TASKS['ArxivImplementationTask'] = ArxivImplementationConfig
ALL_TASKS['ArxivReferenceTask'] = ArxivReferenceConfig
ALL_TASKS['ArxivProblemsTask'] = ArxivProblemsConfig
ALL_TASKS['ArxivStageTask'] = ArxivStageConfig
ALL_TASKS['ArxivTopicTask'] = ArxivTopicConfig
ALL_TASKS['ArxivWebsiteTask'] = ArxivWebsiteConfig
ALL_TASKS['MessageContentTask'] = MessageContentConfig
ALL_TASKS['MessageEmotionTask'] = MessageEmotionConfig
ALL_TASKS['MessageLanguageTask'] = MessageLanguageConfig
ALL_TASKS['MessageSummaryTask'] = MessageSummaryConfig
ALL_TASKS['MessageTimeTask'] = MessageTimeConfig
ALL_TASKS['EmailDateTask'] = EmailDateConfig
ALL_TASKS['EmailEmotionTask'] = EmailEmotionConfig
ALL_TASKS['EmailReceiverTask'] = EmailReceiverConfig
ALL_TASKS['EmailReplyTask'] = EmailReplyConfig
ALL_TASKS['EmailSenderTask'] = EmailSenderConfig
ALL_TASKS['EmailSubjectTask'] = EmailSubjectConfig
ALL_TASKS['EmailSummaryTask'] = EmailSummaryConfig
ALL_TASKS['NewsAuthorsTask'] = NewsAuthorsConfig
ALL_TASKS['NewsCategoryTask'] = NewsCategoryConfig
ALL_TASKS['NewsDateTask'] = NewsDateConfig
ALL_TASKS['NewsDescriptionTask'] = NewsDescriptionConfig
ALL_TASKS['NewsLinkTask'] = NewsLinkConfig
ALL_TASKS['NewsPeopleTask'] = NewsPeopleConfig
ALL_TASKS['NewsPlaceTask'] = NewsPlaceConfig
ALL_TASKS['NewsTitleTask'] = NewsTitleConfig
ALL_TASKS['StockInfoTask'] = StockInfoConfig
ALL_TASKS['StockPurchaseTask'] = StockPurchaseConfig
ALL_TASKS['StockRecommendTask'] = StockRecommendConfig
ALL_TASKS['StockSellTask'] = StockSellConfig
ALL_TASKS['DialogueDailyTask'] = DialogueDailyConfig
ALL_TASKS['DialogueEmotionTask'] = DialogueEmotionConfig
ALL_TASKS['DialogueIdentityTask'] = DialogueIdentityConfig
ALL_TASKS['DialoguePlaceTask'] = DialoguePlaceConfig
ALL_TASKS['DialogueTimeTask'] = DialogueTimeConfig
ALL_TASKS['DialogueTopicTask'] = DialogueTopicConfig