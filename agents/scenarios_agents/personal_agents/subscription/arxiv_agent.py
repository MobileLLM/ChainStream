import chainstream as cs
import arxiv
import datetime

"""
每天帮我做一次Arxiv订阅

最low版：
1.用户设置topics，输入Arxiv订阅的关键词 
2.定时触发收集函数，抓取每天新文章
3.根据paper的abs判断是否推荐

中等版：
1.构建研究方向memory，用户能主动写入，同时也有其他科研agent可以写入
2.3.同上

高级版：
1.构建科研工作专属agent，代理一切科研相关数据和内容，该agent监听会议、笔记、实时录音、工作区文件，对所有内容进行统一汇总和分发。下游对接所有科研类任务流，包括arxiv订阅topic等
2.3.同上

"""


class ArxivAgent(cs.agent.Agent):
    def __init__(self, agent_id='arxiv_subscription_agent'):
        super().__init__(agent_id)
        self.clock_hours_stream = cs.stream.get_stream('clock_hours_stream')
        self.daily_new_papers_stream = cs.stream.create_stream('daily_new_papers_stream')
        self.daily_recommendations_stream = cs.stream.create_stream('daily_recommendations_stream')

        self.text_model = cs.llm.get_model('text_model')

        self.recent_research_memory = cs.memory.fetch('recent_research_memory')

        self.subscription_topics = ['machine learning', 'computer vision']

    def start(self):
        def collect_daily_new_papers(item):
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            client = arxiv.Client()
            # 抓取每天新文章
            for topic in self.subscription_topics:
                search = arxiv.Search(query="cat:cs.AI AND all:%s" % topic,
                                      sort_by=arxiv.SortCriterion.SubmittedDate,
                                      sort_order=arxiv.SortOrder.Descending)
                papers = client.results(search)
                for paper in papers:
                    if paper.published.strftime("%Y-%m-%d") != current_date:
                        break
                    self.daily_new_papers_stream.send(paper)

        def recommend_paper(paper):
            prompt = f"Recently I have been doing research on { self.recent_research_memory }, and this morning a paper with the title {paper.title} and the content {} was released on arxiv. Would you recommend me to read this paper? ?Simply answer Yes or No"
            response = self.text_model.query(prompt).lower().strip()
            print(response)
            if response.startswith('yes'):
                self.daily_recommendations_stream.send_item(paper)


        self.clock_hours_stream.register_listener(self, collect_daily_new_papers)
        self.daily_new_papers_stream.register_listener(self, recommend_paper)
