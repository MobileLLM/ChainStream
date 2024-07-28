import datetime


class SandboxEvent:
    def __init__(self):
        self.event_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    def to_dict(self):
        new_dict = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                if k == "inspect_stack":
                    v = [str(x) for x in v]
                else:
                    v = str(v)
                new_dict[k] = v

        return new_dict


class GetModelEvent(SandboxEvent):
    def __init__(self, model_class_name, inspect_stack):
        super().__init__()
        self.model_class_name = model_class_name
        self.inspect_stack = [x for x in inspect_stack]


class MakePromptEvent(SandboxEvent):
    def __init__(self, prompt, input_args, inspect_stack):
        super().__init__()
        self.prompt = prompt
        self.input_args = input_args
        self.inspect_stack = [x for x in inspect_stack]


class QueryEvent(SandboxEvent):
    def __init__(self, args, kwargs, res, error, inspect_stack):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.res = res
        self.error = error
        self.inspect_stack = [x for x in inspect_stack]


class GetStreamEvent(SandboxEvent):
    def __init__(self, agent, stream_id, is_stream_manager, find_stream, inspect_stack):
        super().__init__()
        self.agent = agent
        self.stream_id = stream_id
        self.is_stream_manager = is_stream_manager
        self.find_stream = find_stream
        self.inspect_stack = [x for x in inspect_stack]


class CreateStreamEvent(SandboxEvent):
    def __init__(self, agent_id, stream_id, listener_id, success_create, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.stream_id = stream_id
        self.listener_id = listener_id
        self.success_create = success_create
        self.inspect_stack = [x for x in inspect_stack]


class ForEachEvent(SandboxEvent):
    def __init__(self, agent_id, stream_id, listener_id, success_create, to_stream_id, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.stream_id = stream_id
        self.listener_id = listener_id
        self.success_create = success_create
        self.to_stream_id = to_stream_id
        self.inspect_stack = [x for x in inspect_stack]


class BatchEvent(SandboxEvent):
    def __init__(self, agent_id, stream_id, listener_id, listener_params, to_stream_id, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.stream_id = stream_id
        self.listener_id = listener_id
        self.listener_params = listener_params
        self.to_stream_id = to_stream_id
        self.inspect_stack = [x for x in inspect_stack]


class AddItemEvent(SandboxEvent):
    def __init__(self, agent_id, stream_id, item, func_id, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.stream_id = stream_id
        self.item = item
        self.func_id = func_id
        self.inspect_stack = [x for x in inspect_stack]


class FunctionInstantiateEvent(SandboxEvent):
    def __init__(self, agent_id, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.inspect_stack = [x for x in inspect_stack]


class FunctionStartEvent(SandboxEvent):
    def __init__(self, agent_id, start_res, inspect_stack):
        super().__init__()
        self.agent_id = agent_id
        self.start_res = start_res
        self.inspect_stack = [x for x in inspect_stack]


class FunctionCallEvent(SandboxEvent):
    def __init__(self, func_id, output_stream_id, agent_id, args, kwargs, func_result, inspect_stack):
        super().__init__()
        self.func_id = func_id
        self.output_stream_id = output_stream_id
        self.agent_id = agent_id
        self.args = args
        self.kwargs = kwargs
        self.func_result = func_result
        self.inspect_stack = [x for x in inspect_stack]


class SandboxRecorder:
    def __init__(self):
        self.event_recordings = {
            "llm": {
                "get_model": [],
                "make_prompt": [],
                "query": [],
            },
            "stream": {
                "get_stream": [],
                "create_stream": [],
                "create_anonymous_stream": [],
                "for_each": [],
                "batch": [],
                "add_item": [],
            },
            "agent": {
                "instantiate": [],
                "start": []
            },
            "function": {
                "call": [],
                "return": []
            },
        }

    def record_get_model(self, model_class_name, inspect_stack):
        event = GetModelEvent(model_class_name, inspect_stack).to_dict()
        self.event_recordings["llm"]["get_model"].append(event)

    def record_make_prompt(self, prompt, input_args, inspect_stack):
        event = MakePromptEvent(prompt, input_args, inspect_stack).to_dict()
        self.event_recordings["llm"]["make_prompt"].append(event)

    def record_query(self, args, kwargs, res, error, inspect_stack):
        event = QueryEvent(args, kwargs, res, error, inspect_stack).to_dict()
        self.event_recordings["llm"]["query"].append(event)

    def record_get_stream(self, agent, stream_id, is_stream_manager, find_stream, inspect_stack):
        event = GetStreamEvent(agent, stream_id, is_stream_manager, find_stream, inspect_stack).to_dict()
        self.event_recordings["stream"]["get_stream"].append(event)

    def record_create_stream(self, agent_id, stream_id, is_stream_manager, success_create, inspect_stack):
        event = CreateStreamEvent(agent_id, stream_id, is_stream_manager, success_create, inspect_stack).to_dict()
        self.event_recordings["stream"]["create_stream"].append(event)

    def record_create_anonymous_stream(self, agent_id, stream_id, listener_id, success_create, inspect_stack):
        event = CreateStreamEvent(agent_id, stream_id, listener_id, success_create, inspect_stack).to_dict()
        self.event_recordings["stream"]["create_anonymous_stream"].append(event)

    def record_for_each(self, agent_id, stream_id, listener_id, success_create, to_stream_id, inspect_stack):
        event = ForEachEvent(agent_id, stream_id, listener_id, success_create, to_stream_id, inspect_stack).to_dict()
        self.event_recordings["stream"]["for_each"].append(event)

    def record_batch(self, agent_id, stream_id, listener_id, listener_params, to_stream_id, inspect_stack):
        event = BatchEvent(agent_id, stream_id, listener_id, listener_params, to_stream_id, inspect_stack).to_dict()
        self.event_recordings["stream"]["batch"].append(event)

    def record_add_item(self, agent_id, stream_id, item, func_id, inspect_stack):
        event = AddItemEvent(agent_id, stream_id, item, func_id, inspect_stack).to_dict()
        self.event_recordings["stream"]["add_item"].append(event)

    def record_instantiate(self, agent_id, inspect_stack):
        event = FunctionInstantiateEvent(agent_id, inspect_stack).to_dict()
        self.event_recordings["agent"]["instantiate"].append(event)

    # TODO: something wrong with this function combining with decorator
    def record_start(self, agent_id, start_res, inspect_stack):
        event = FunctionStartEvent(agent_id, start_res, inspect_stack).to_dict()
        self.event_recordings["agent"]["start"].append(event)

    def record_call(self, func_id, output_stream_id, agent_id, args, kwargs, func_result, inspect_stack):
        event = FunctionCallEvent(func_id, output_stream_id, agent_id, args, kwargs, func_result, inspect_stack).to_dict()
        self.event_recordings["function"]["call"].append(event)

    def record_return(self):
        pass

    def get_event_recordings(self):
        return self.event_recordings
