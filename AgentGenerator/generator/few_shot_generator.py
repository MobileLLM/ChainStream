from AgentGenerator.utils.llm_utils import TextGPTModel
from AgentGenerator.prompt.chainstream_doc import chainstream_doc
from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.io_model import StreamListDescription


class FewShotGenerator(AgentGeneratorBase):
    def __init__(self, model_name="gpt-4o"):
        super().__init__()
        self.model = TextGPTModel(model_name)
        self.max_token_len = 4096

    # TODO: need new parameters for few-shot generation
    def generate_agent_impl(self, base_prompt) -> str:
        # prompt = [
        #     {
        #         "role": "system",
        #         "content": self._get_system_prompt()
        #     },
        #     {
        #         "role": "user",
        #         "content": self._get_user_prompt(input_description+agent_description)
        #     }
        # ]

        base_prompt = base_prompt + "\n\nPlease write code directly in the code block below, do not need any explanation.\nCode: "

        print(base_prompt)

        prompt = [
            {
                "role": "system",
                "content": base_prompt
            }
        ]
        response = self.model.query(prompt)
        return response.replace("'''", " ").replace("```", " ").replace("python", "")

    def _get_system_prompt(self):
        return chainstream_doc.chainstream_chinese_doc

    # TODO: need to update user prompt to support new prompt format
    def _get_user_prompt(self, task):
        # user_prompt = (
        #     "Design an agent mainly for processing Arxiv paper abstracts. Get the configuration of ArxivTask "
        #     "from the ALL_TASKS_OLD dictionary, retrieve data from the input stream all_arxiv, define and register "
        #     "a listener, and process the value corresponding to the 'abstract' key in the paper dictionary: "
        #     "Extract the abstract content and generate a prompt asking whether the abstract is related to 'edge LLM agent'. "
        #     "Query the prompt using the text type llm to get a response. If the response is 'Yes', add the paper to the output stream cs_arxiv, "
        #     "and save the results in the output stream."
        # )
        # return user_prompt
        return task


if __name__ == "__main__":
    agent_generator = FewShotGenerator()
    agent_code = agent_generator.generate_agent(
        StreamListDescription(streams=[{
            "stream_id": "summary_by_sender",
            "description": "A list of email summaries grouped by each email sender for pre 10 emails, excluding advertisement emails",
            "fields": {
                "sender": "name xxx, string",
                "summary": "sum xxx, string"
            }
        }]),
        input_description=StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
    )
    print(agent_code)
