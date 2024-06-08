from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt

class ElectionPublicOpinion(Agent):
    '''
    Several steps:
    1. Get all the news articles.
    2. Filter out the articles related to the election and push them to a new stream.
    3. Filter out the articles based on some criteria (state, party, sentiment analysis, keyword matching, etc.) and push them to a new stream.
    4. Summarize each stream's opinion every day and push it to a new stream.
    5. Listens to the stream from different sources and compares the opinions between them.
    '''