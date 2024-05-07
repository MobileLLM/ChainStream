from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt


class AppUsageStatistics(Agent):
    def __init__(self):
        super().__init__("app_usage_statistics")
        self.screen_snopshot_stream = get_stream("screen_snapshot_stream")
        self.clock = get_stream("clock_every_day")
        self.app_usage_memory = create_memory("app_usage_memory", type='kv')
        self.install_app_memory = create_memory("install_app_memory", type='seq')
        self.daily_app_usage_report_stream = create_stream("daily_app_usage_report_stream")

        self.last_use_app = None

        self.app_change_stream = get_stream("app_change_stream")

        self.llm = get_model(['text', 'image'])

    def start(self):
        def update_memory_when_install_app_change(change_action):
            if change_action['action'] == 'install':
                self.install_app_memory.add_item(change_action['app_name'])
            elif change_action['action'] == 'uninstall':
                self.install_app_memory.remove_item(change_action['app_name'])
        self.app_change_stream.register_listener(self, update_memory_when_install_app_change)

        def statistic_app_usage(screen_snapshot):
            prompt = make_prompt("The following apps are installed", self.install_app_memory, "Please indicate which "
                                                                                              "app are using in the "
                                                                                              "screenshot below: ",
                                 screen_snapshot['image'])
            response = self.llm.generate_response(prompt)

            if self.last_use_app is not None:
                if response == self.last_use_app['app_name']:
                    app_usage_time = self.app_usage_memory[response]
                    app_usage_time += screen_snapshot['time'] - self.last_use_app['time']
                    self.app_usage_memory[response] = app_usage_time
            else:
                self.last_use_app = {'app_name': response, 'time': screen_snapshot['time']}
            self.last_use_app['time'] = screen_snapshot['time']
        self.screen_snopshot_stream.register_listener(self, statistic_app_usage)

        def record_app_usage_time(clock_time):
            prompt = make_prompt("Give me a report of today app usage: ", self.install_app_memory)
            response = self.llm.generate_response(prompt)
            self.daily_app_usage_report_stream.add_item({'report': response, 'time': clock_time})
            self.app_usage_memory.clear()
        self.clock.register_listener(self, record_app_usage_time)

    def stop(self):
        self.screen_snopshot_stream.unregister_listener(self)
        self.clock.unregister_listener(self)
        self.app_change_stream.unregister_listener(self)

