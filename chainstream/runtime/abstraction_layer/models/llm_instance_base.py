from queue import Queue, Empty
import threading


class LLMInstanceBase:
    def __init__(self):
        self.input_queue = Queue()
        self.router_list = []
        self.lock = threading.Lock()
        self.processing_thread = None
        self.stop_event = threading.Event()

    def process_query(self, input_data) -> object:
        raise NotImplementedError("process_query method not implemented")

    def release_resources(self):
        raise NotImplementedError("release_resources method not implemented")

    def init_resources(self):
        raise NotImplementedError("init_resources method not implemented")

    def _start_processing(self):
        self.stop_event.clear()
        self.init_resources()
        self.processing_thread = threading.Thread(target=self._process_input_queue)

    def _process_input_queue(self):
        while not self.stop_event.is_set():
            try:
                input_data, response_queue = self.input_queue.get(timeout=1)
                response = self.process_query(input_data)
                response_queue.put(response)

            except Empty:
                continue

    def _stop_processing(self):
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
