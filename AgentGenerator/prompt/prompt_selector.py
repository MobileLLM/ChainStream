from AgentGenerator.utils import TextGPTModel
from .API_prompt import API_USAGE_PROMPT
from .template_prompt import TEMPLATE_PROMPT, AGENT_EXAMPLE


class PromptSelector:
    def __init__(self):
        self.api_prompt_list = API_USAGE_PROMPT
        self.template_prompt_list = TEMPLATE_PROMPT
        self.agent_example_list = AGENT_EXAMPLE

        self.llm = TextGPTModel()

    def select_base_error(self, error_msg, select_policy="all"):
        assert select_policy in ["all", "random", "llm", "none"]

        if select_policy == "all":
            selected_prompt = self.api_prompt_list + self.template_prompt_list + self.agent_example_list
        elif select_policy == "random":
            selected_prompt = self._random_select_prompt()
        elif select_policy == "llm":
            selected_prompt = self._llm_select_prompt(error_msg)
        elif select_policy == "none":
            selected_prompt = []
        else:
            raise ValueError("Invalid select_policy")

        return self.assemble_prompt(error_msg, selected_prompt)

    def _llm_select_prompt(self, error_msg) -> list:
        pass

    def _random_select_prompt(self) -> list:
        pass

    def _process_error_msg(self, error_msg) -> str:
        pass

    def assemble_prompt(self, error_msg, template_list):
        error_msg = self._process_error_msg(error_msg)
        error_prompt = f"""
        The agent running in the sandbox encountered an error: {error_msg}.
        """
        if template_list:
            template_prompt = self._process_template_list(template_list)
            template_prompt = f"""
            We can provide the following prompt to help you debug the error:
            {template_prompt}
            """
        else:
            template_prompt = ""
        return error_prompt + template_prompt

    def _process_template_list(self, template_list) -> str:
        pass
