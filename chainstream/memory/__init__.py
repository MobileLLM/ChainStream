available_memories = {}


def fetch(memory_id):
    if memory_id in available_memories:
        return available_memories[memory_id]
    else:
        raise RuntimeError(f'unknown memory_id: {memory_id}')


def create(memory_id, type=None):
    if type == 'kv':
        from .kv_memory import KV_Memory
        memory = KV_Memory(memory_id)
    elif type == 'seq':
        from .sequential_memory import SequentialMemory
        memory = SequentialMemory(memory_id)
    elif type == 'relational':
        from .relational_memory import RelationalMemory
        memory = RelationalMemory(memory_id)
    available_memories[memory_id] = memory
    return memory

