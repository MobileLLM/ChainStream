from queue import Queue, Empty
from .llm_recorder import LLMRecorder
import threading
from enum import Enum


# an enum to mark the llm instance from cloud or local
class LLMInstanceType(Enum):
    CLOUD = 1
    LOCAL = 2




class LLMInstanceMessageBase:
    model_name = None
    model_type = None

    def __init__(self):
        self.input_queue = Queue()
        self.router_list = []
        self.lock = threading.Lock()
        self.processing_thread = None
        self.stop_event = threading.Event()

        self.recorder = LLMRecorder()

    def process_query(self, prompt_message) -> object:
        raise NotImplementedError("process_query method not implemented")

    def release_resources(self):
        raise NotImplementedError("release_resources method not implemented")

    def init_resources(self):
        raise NotImplementedError("init_resources method not implemented")

    def _start_processing(self):
        self.recorder.record_start()
        self.stop_event.clear()
        self.init_resources()
        self.processing_thread = threading.Thread(target=self._process_input_queue)

    def _process_input_queue(self):
        while not self.stop_event.is_set():
            try:
                prompt_message, response_queue = self.input_queue.get(timeout=1)
                self.recorder.record_query(prompt_message)
                response, prompt_tokens, completion_tokens = self.process_query(prompt_message)
                self.recorder.record_response(response, prompt_tokens, completion_tokens)
                response_queue.put(response)

            except Empty:
                continue

    def _stop_processing(self):
        self.recorder.record_stop()
        self.stop_event.set()
        if self.processing_thread is not None:
            self.processing_thread.join()
            self.release_resources()
            self.processing_thread = None

    def send_query(self, prompt, response_queue):
        self.input_queue.put((prompt, response_queue))

    def _add_router(self, router):
        with self.lock:
            self.router_list.append(router)
            if len(self.router_list) == 1:
                self._start_processing()

    def _remove_router(self, router):
        with self.lock:
            self.router_list.remove(router)
            if len(self.router_list) == 0:
                self._stop_processing()
