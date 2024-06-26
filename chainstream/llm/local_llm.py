
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from transformers.generation import GenerationConfig
import ollama

class BaseModel:
    def __init__(self,):
        '''
           To be able to accommodate a large number of applications based on local models,
           I will not provide excessive definitions here.
        '''

    def query(self,*args, **kwargs):
        raise RuntimeError("must implement query method")

class LocalChatLLM(BaseModel):
    def __init__(self,name_or_path,system_define:dict=None,pre_history:list=None,max_token=128):
        self.tokenizer=AutoTokenizer.from_pretrained(name_or_path)
        self.model=AutoModelForCausalLM.from_pretrained(name_or_path)
        self.max_new__token=max_token
        self.history=[]
        self.ues_system_define=False
        self.use_pre_history=False


        if system_define:
            self.history.append(system_define)
            self.use_system_define=True
        if pre_history:
            self.history+=pre_history
            self.use_pre_history=True
            self.pre_history_len=len(pre_history)
    def query(self,query:str):
        message={"role":"user","content":query}
        self.history.append(message)
        tokenized_chat=self.tokenizer.apply_chat_template(self.history, tokenize=True, add_generation_prompt=True, return_tensors="pt")
        output=self.model.generate(tokenized_chat,max_new_tokens=self.max_new_token)

        content=self.tokenizer.decode(tokenized_chat[0]).repace(self.tokenizer.decode(output[0]),'')

        reply={"role":"assistant","content":content}

        self.history.append(reply)

        return content
    def clear_history(self):
        '''
        Resetting the conversation history to its initial state
        '''
        clear_idx=0
        if self.use_system_define:
            clear_idx+=1
        if self.use_pre_history:
            clear_idx+=self.pre_history_len
        self.history=self.history[:clear_idx]

class QWenChatLLM(BaseModel):
    def __init__(self,use_local=False,model_dir=None,system_prompt=None):
        if not use_local:
            self.tokenizer=AutoTokenizer.from_pretrained("Qwen/Qwen-1_8B-Chat",trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-1_8B-Chat", device_map="auto", trust_remote_code=True,
                                                     bf16=True).eval()
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                device_map="auto",
                trust_remote_code=True
            ).eval()

        self.history=None
        self.system_prompt=system_prompt

    def query(self, query: str):
        response, history = self.model.chat(self.tokenizer, query, history=self.history,system=self.system_prompt)

        self.history=history

        return response

    def clear_history(self):

        self.history=None

class QWenVLChatLLM(BaseModel):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
        self.model=AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()
        self.model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

        self.history=None
    def query(self,image:str=None,text:str=None):
        query = self.tokenizer.from_list_format([
            {'image': image},
            {'text': text},
        ])

        response,history=self.model.chat(self.tokenizer, query=self.query, history=self.history)

        self.history=history

        return response

    def clear_history(self):
        self.history=None

class GemmaLLM(BaseModel):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("/kaggle/input/gemma/transformers/2b-it/2")
        self.model = AutoModelForCausalLM.from_pretrained("/kaggle/input/gemma/transformers/2b-it/2")

    def query(self,query:str):
        query_ids=self.tokenizer(query, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**query_ids)
        return outputs

