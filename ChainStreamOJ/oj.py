from chainstream.runtime import cs_server


class ExecError(Exception):
    def __init__(self, message):
        super().__init__(message)


class StartError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RunningError(Exception):
    def __init__(self, message):
        super().__init__(message)


class FindAgentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InitalizeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class OJ:
    def __init__(self, task, agent_file):
        cs_server.init(server_type='core')
        cs_server.start()
        self.runtime = cs_server.get_chainstream_core()
        self.task = task
        if isinstance(agent_file, str) and agent_file.endswith('.py'):
            with open(agent_file, 'r') as f:
                agent_file = f.read()
        self.agent_str = agent_file

        self.result = {}

    def start_test_agent(self):
        self.task.init_environment(self.runtime)

        res = self._start_agent()

        if res is not None:
            self.result['start_agent'] = res
            raise RunningError("Error while starting agent: " + str(res))

        try:
            self.task.start_task(self.runtime)
        except Exception as e:
            self.result['start_stream'] = e
            raise RunningError("Error while starting stream: " + str(e))

        self.task.evaluate_task(self.runtime)

    def _start_agent(self):
        try:
            namespace = {}
            try:
                exec(self.agent_str, globals(), namespace)
            except Exception as e:
                raise ExecError("Error while executing agent file: " + str(e))

            class_object = None
            # globals().update(namespace)
            for name, obj in namespace.items():
                if isinstance(obj, type):
                    class_object = obj
                    break

            if class_object is not None:
                try:
                    self.agent_instance = class_object()
                except Exception as e:
                    raise InitalizeError("Error while initializing agent: " + str(e))
            else:
                raise FindAgentError("Agent class not found in agent file")

        except Exception as e:
            return e
        return None


if __name__ == "__main__":
    from tasks import ALL_TASKS

    WorkSmsTaskConfig = ALL_TASKS['WorkSmsTask']

    agent_file = '''
import chainstream as cs

class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_oj_agent")
        self.input_stream = cs.get_stream("all_sms")
        self.output_stream = cs.get_stream("work_sms")
        
    def start(self):
        def process_sms(sms):
            print("test agent received sms: ", sms)
            self.output_stream.add_item(sms)
        self.input_stream.register_listener(self, process_sms)
    
    def stop(self):
        self.input_stream.unregister_listener(self)
            
    '''
    oj = OJ(WorkSmsTaskConfig(), agent_file)
    oj.start_test_agent()
