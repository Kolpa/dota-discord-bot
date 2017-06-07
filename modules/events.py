class EventHandler(object):
    def __init__(self, sender):
        self.callbacks = []
        self.sender = sender

    def __call__(self, *args):
        return [callback(*args) for callback in self.callbacks]

    def __iadd__(self, callback):
        self.add(callback)
        return self

    def __isub__(self, callback):
        self.remove(callback)
        return self

    def __len__(self):
        return len(self.callbacks)

    def __getitem__(self, index):
        return self.callbacks[index]

    def __setitem__(self, index, value):
        self.callbacks[index] = value

    def __delitem__(self, index):
        del self.callbacks[index]

    def add(self, callback):
        if not callable(callback):
            raise TypeError("callback mus be callable")
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)


class AsyncEventHandler(object):
    def __init__(self, sender):
        self.callbacks = []
        self.sender = sender

    async def __call__(self, *args):
        return [await callback(*args) for callback in self.callbacks]

    def __iadd__(self, callback):
        self.add(callback)
        return self

    def __isub__(self, callback):
        self.remove(callback)
        return self

    def __len__(self):
        return len(self.callbacks)

    def __getitem__(self, index):
        return self.callbacks[index]

    def __setitem__(self, index, value):
        self.callbacks[index] = value

    def __delitem__(self, index):
        del self.callbacks[index]

    def add(self, callback):
        if not callable(callback):
            raise TypeError("callback mus be callable")
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)