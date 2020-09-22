import asyncio


class AsyncQueue:
    def __init__(self):
        self.future = []
        self.queue = []

    def add_message(self, message):
        self.queue.append(message)
        self.try_resolve()

    def get_message(self):
        future = asyncio.Future()
        self.future.append(future)
        self.try_resolve()
        return future

    def try_resolve(self):
        if len(self.future) > 0 and len(self.queue) > 0:
            future: asyncio.Future = self.future.pop(0)
            result = self.queue.pop(0)
            future.set_result(result)


def Create():
    return AsyncQueue()
