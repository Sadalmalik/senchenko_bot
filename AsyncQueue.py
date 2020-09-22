import asyncio


class AsyncQueue:
    def __init__(self):
        self.futures_queue = []
        self.messages_queue = []

    def add_message(self, message):
        self.messages_queue.append(message)
        self.try_resolve()

    def get_message(self):
        future = asyncio.Future()
        self.futures_queue.append(future)
        self.try_resolve()
        return future

    def try_resolve(self):
        if len(self.futures_queue) > 0 and len(self.messages_queue) > 0:
            future: asyncio.Future = self.futures_queue.pop(0)
            result = self.messages_queue.pop(0)
            future.set_result(result)


def Create():
    return AsyncQueue()
