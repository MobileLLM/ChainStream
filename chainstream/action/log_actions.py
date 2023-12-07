from chainstream.interfaces import ActionInterface


class LogAction(ActionInterface):
    def __init__(self, agent, message) -> None:
        super().__init__()
        self.agent = agent
        self.message = message

    def execute(self):
        print(self.message)

