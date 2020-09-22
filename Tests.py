import asyncio
from AsyncQueue import AsyncQueue


async def producer(queue: AsyncQueue):
    print(f"Production start!")
    for i in range(50, 55):
        await asyncio.sleep(1)
        print(f"Produce message {i}")
        queue.add_message(i)
    queue.add_message(None)
    print(f"Production complete!")


async def consumer(queue: AsyncQueue):
    print(f"Consuming start!")
    message = await queue.get_message()
    while message is not None:
        print(f"Consumed message: {message}")
        message = await queue.get_message()
    print(f"Consuming complete!")


async def Start():
    queue = AsyncQueue()
    await asyncio.gather(
        consumer(queue),
        producer(queue)
    )


if __name__ == '__main__':
    asyncio.run(Start())
    print("Started!")
