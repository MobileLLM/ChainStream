from .sandbox_recorder import SandboxRecorder

# IS_SANDBOX_RECORDING_ENABLED = False

SANDBOX_RECORDER = None


def start_sandbox_recording():
    global SANDBOX_RECORDER
    SANDBOX_RECORDER = SandboxRecorder()
    # global IS_SANDBOX_RECORDING_ENABLED
    # if not IS_SANDBOX_RECORDING_ENABLED:
    #     SANDBOX_RECORDER = SandboxRecorder()
    #     IS_SANDBOX_RECORDING_ENABLED = True


def stop_sandbox_recording():
    global SANDBOX_RECORDER
    del SANDBOX_RECORDER
    SANDBOX_RECORDER = None
