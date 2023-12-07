from chainstream.interfaces import ContextInterface


class TextContext(ContextInterface):
    def __init__(self, text):
        self.text = text

    def to_prompt(self):
        return self.text

