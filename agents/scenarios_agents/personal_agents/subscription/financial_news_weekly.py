import requests
import chainstream as cs
from chainstream.runtime.stream_manager import StreamManager

class BloombergNewsAgent(cs.agent.Agent):
    """
    An agent that retrieves Bloomberg news stories based on query parameters.
    """
    def __init__(self, agent_id="bloomberg_news_agent", stream_id="bloomberg_news_stream"):
        super().__init__(agent_id)
        self._source = StreamManager()  # instance of Stream
        self.stream_id = stream_id
        self.url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/stories/list"
        self.headers = {
            "X-RapidAPI-Key": "24a452e0dfmsh005053d29a98d82p11020bjsn78090bc7deaf",
            "X-RapidAPI-Host": "bloomberg-market-and-financial-news.p.rapidapi.com"
        }
        self._source.register_stream(self.stream_id, self)  # Pass self as the stream argument

    def start(self):
        try:
            self._source.register_listener(self, self.handle_input)
            return True
        except Exception as e:
            print("Error in Bloomberg News Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)

    def handle_input(self, query_params):
        response = requests.get(self.url, headers=self.headers, params=query_params)
        if response.status_code == 200:
            json_data = response.json()
            stories = json_data.get('stories', [])
            for story in stories:
                title = story.get('title', '')  # 获取文章标题
                shortURL = story.get('shortURL', '')  # 获取文章短链接
                published = shortURL.split('/')[-1]  # 从短链接中提取发布号
                published_date = shortURL.split('/')[-2]  # 从短链接中提取发布时间
                thumbnailImage = story.get('thumbnailImage', '')  # 获取文章缩略图链接
                # 打印文章信息而不是发布到流中
                print(f"标题：{title}\n发布号：{published}\n发布时间：{published_date}\n缩略图链接：{thumbnailImage}\n短链接：{shortURL}\n")
        else:
            print("请求失败:", response.status_code)

def main():
    bloomberg_news_agent = BloombergNewsAgent(agent_id="bloomberg_news_agent", stream_id="bloomberg_news_stream")
    query_params = {"template": "CURRENCY", "id": "usdjpy"}
    bloomberg_news_agent.handle_input(query_params)

if __name__ == "__main__":
    main()
