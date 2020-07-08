import asyncio
import concurrent.futures
import time

from juneau_extension.test_json import update_exec_status


def instance(pid):
    if pid % 2 == 0:
        print(update_exec_status("done", pid))
    else:
        print(update_exec_status("operating", pid))
        time.sleep(3)
        print(update_exec_status("done", pid))


async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        # futures = [
        #     loop.run_in_executor(executor, instance, '1'),
        #     loop.run_in_executor(executor, instance, '2')
        #     # loop.run_in_executor(executor, request, '3')
        # ]
        # for response in await asyncio.gather(*futures):
        #     pass
        for i in range(10):
            loop.run_in_executor(executor, instance, i)

time.sleep(2)
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.close()
