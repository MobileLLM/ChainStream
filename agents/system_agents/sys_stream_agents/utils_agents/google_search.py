import os
import requests
import json
import chainstream as cs
class SearchAgent(cs.agent.Agent):
    def __init__(self, agent_id='search_agent'):
        super().__init__(agent_id)
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.serper_google_url = os.getenv("SERPER_GOOGLE_URL")
    def start(self):
        def handle_input(query):
            search_result = self.search(query)
            self.result_buffer.save(search_result)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in Search Agent: ", e)
            return False

    def search(self, query):
        payload = json.dumps({
            "q": query
        })
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self.serper_google_url, headers=headers, data=payload)
        print(f'Google 搜索结果: \n {response.text}')
        return response.text
