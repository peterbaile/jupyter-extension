import asyncio
import concurrent.futures


def instance(pid):
    while True:
        if pid % 2 == 0:
            print("this is an even number")
        else:
            print("hi!")


async def index():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        # futures = [
        #     loop.run_in_executor(executor, instance, '1'),
        #     loop.run_in_executor(executor, instance, '2')
        #     # loop.run_in_executor(executor, request, '3')
        # ]
        # for response in await asyncio.gather(*futures):
        #     pass
        for i in range(5):
            loop.run_in_executor(executor, instance, i)


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(index())
event_loop.close()
