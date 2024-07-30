from ChainStreamSandBox.evaluator.evaluator_base import EvaluatorBase


class EvalSuccessRate(EvaluatorBase):
    def __init__(self, log_path):
        super().__init__()
        self.log_path = log_path
        self.all_reports = self.load_sandbox_log(log_path)

    def calculate_success_rate(self) -> float:
        pass

