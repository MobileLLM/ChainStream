available_memories = {}


def get_memory(memory_id):
    return fetch_memory(memory_id)


def fetch_memory(memory_id):
    if memory_id in available_memories:
        return available_memories[memory_id]
    else:
        raise RuntimeError(f'unknown memory_id: {memory_id}')


def create_memory(memory_id, type, columns_and_setting=None):
    memory = None
    if type == 'kv':
        from .kv_memory import KVMemory
        memory = KVMemory(memory_id)
    elif type == 'seq':
        if columns_and_setting is None:
            raise RuntimeError('columns_and_setting must be provided for sequential memory')
        from .sequential_memory import SequentialMemory
        memory = SequentialMemory(memory_id, columns_and_setting)
    # elif type == 'relational':
    #     from .relational_memory import RelationalMemory
    #     memory = RelationalMemory(memory_id)
    available_memories[memory_id] = memory
    return memory
