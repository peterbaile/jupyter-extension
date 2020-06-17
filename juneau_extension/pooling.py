import json
import asyncio
import concurrent.futures


def get_status(pid):
    while True:
        with open("data_file.json", "r") as file:
            try:
                data = json.load(file)
                if data.get(str(pid)):
                    print(f'process {pid}: {data[str(pid)]}')

                if data.get(str(pid)) == "done":
                    break

            except Exception as e:
                continue


def instance(pid):
    get_status(pid)


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


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.close()

