from chainstream.runtime.runtime_core import RuntimeCore

chainstream_core: RuntimeCore = None


def set_core(core):
    global chainstream_core
    chainstream_core = core
