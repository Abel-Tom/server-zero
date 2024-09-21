import asyncio

async def data_generator():
    for i in range(10):
        yield f"Data chunk {i}\n"
        await asyncio.sleep(1)

async def consume_data(data_stream):
    async for data in data_stream:
        print(data)

async def main():
    data_stream = data_generator()
    consumer_task = asyncio.create_task(consume_data(data_stream))
    await consumer_task


asyncio.run(main())

