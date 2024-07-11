from AgentGenerator.generator.utils import TextGPTModel
from AgentGenerator.chainstream_doc import chainstream_doc
from .generator_base import AgentGeneratorBase
from ..io_model import StreamListDescription


class FewShotGenerator(AgentGeneratorBase):
    def __init__(self, model_name="gpt-3.5-turbo-1106"):
        super().__init__()
        self.model = TextGPTModel(model_name)
        self.max_token_len = 4096

    # TODO: need new parameters for few-shot generation
    def generate_agent_impl(self, input_description: [StreamListDescription, None], agent_description: StreamListDescription) -> str:
        prompt = [
            {
                "role": "system",
                "content": self._get_system_prompt()
            },
            {
                "role": "user",
                "content": self._get_user_prompt(input_description+agent_description)
            }
        ]
        response = self.model.query(prompt)
        return response.replace("'''", " ").replace("```", " ").replace("python", "")

    def _get_system_prompt(self):
        return chainstream_doc.chinese_chainstream_doc

    # TODO: need to update user prompt to support new prompt format
    def _get_user_prompt(self, task):
        # user_prompt = (
        #     "Design an agent mainly for processing Arxiv paper abstracts. Get the configuration of ArxivTask "
        #     "from the ALL_TASKS dictionary, retrieve data from the input stream all_arxiv, define and register "
        #     "a listener, and process the value corresponding to the 'abstract' key in the paper dictionary: "
        #     "Extract the abstract content and generate a prompt asking whether the abstract is related to 'edge LLM agent'. "
        #     "Query the prompt using the text type llm to get a response. If the response is 'Yes', add the paper to the output stream cs_arxiv, "
        #     "and save the results in the output stream."
        # )
        # return user_prompt
        return task


if __name__ == "__main__":
    agent_generator = FewShotGenerator()
    task_description = "Process Arxiv paper abstracts to filter those related to 'edge LLM agent'."
    dsl_output = agent_generator.generate_dsl(task_description)
    print(dsl_output)
