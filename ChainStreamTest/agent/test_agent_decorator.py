class ClassNote:
    def __init__(self, note):
        self.note = note

    def __call__(self, cls):
        cls.__class_note__ = self.note
        return cls


class StreamFuncNote:
    def __init__(self, note):
        self.note = note

    def __call__(self, func):
        func.__stream_func_note__ = self.note
        return func


@ClassNote("this class is for xxx")
class A:
    def __init__(self):

        pass

    def start(self):
        @StreamFuncNote("this func is for xxx")
        def new_fun():
            name = "John"
            pass

        return new_fun


# Example usage
a = A()
func = a.start()
print(a.__class_note__)  # Output: "this class is for xxx"
print(func.__stream_func_note__)  # Output: "this func is for xxx" (note for the nested function 'new_fun')
