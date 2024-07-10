class EvaluatorBase:
    def __init__(self, sandbox_log_paths):
        self.sandbox_reports = []
        if isinstance(sandbox_log_paths, str):
            sandbox_log_paths = [sandbox_log_paths]
        self.sandbox_log_paths = sandbox_log_paths

    def _process_sandbox_logs(self):
        for log_path in self.sandbox_log_paths:
            self._process_sandbox_log(log_path)

    def _process_sandbox_log(self, log_path):
        pass
