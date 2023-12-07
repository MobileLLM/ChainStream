available_memories = {}


def fetch(memory_id):
    if memory_id in available_memories:
        return available_memories[memory_id]
    else:
        raise RuntimeError(f'unknown memory_id: {memory_id}')


def create(memory_id, type=None):
    if type is 'video':
        from .kv_memory import KV_Memory
        memory = KV_Memory()
    else:
        from .sequential_memory import SequentialMemory
        memory = SequentialMemory()
    available_memories[memory_id] = memory
    return memory

