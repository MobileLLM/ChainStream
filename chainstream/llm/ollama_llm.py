import ollama

class Ollama_LLM():
    def __init__(self,model_name,model_file=None):
        model_list=ollama.list()
        for model in model_list:
            if model['name'].split(':')[0] ==model_name or model['name']==model_name:
                self.model=model_name
            else:
                if model_file!=None:
                    ollama.create(model=model_name,model_file=model_file)
                    self.model=model_name
                else:
                    try:
                        ollama.pull(model_name)
                        self.model_name=model
                    except Exception as e:
                        print(f'error occur:{e}')
        self.message_list=[]
    def chat(self,query):
        message={'role':'user','content':query}
        self.message_list.append(message)
        try:
            response=ollama.chat(model=self.model,messages=self.message_list)
            self.message_list.append(response['message'])
            return response['message']['content']
        except Exception as e:
            print(f'error occur:{e}')
    def clear_meesage_list(self):
        self.message_list=[]







