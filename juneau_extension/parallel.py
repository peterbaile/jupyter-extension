import asyncio
from juneau_extension.jupyter import exec_ipython_asyncio


# Adapted from https://docs.python.org/3/library/asyncio-queue.html#examples
async def worker(name, queue):
    while True:
        # Step 1: Get a "work item" out of the queue
        proc_info = await queue.get()
        kid = proc_info.get('kid')
        var_name = proc_info.get('var_name')

        # Step 2: do the task
        output, error = await exec_ipython_asyncio(kid, var_name, 'connect_psql')

        if output:
            print(f'[stdout]\n{output.decode()}')
        if error:
            print(f'[stderr]\n{error.decode()}')

        # Step 3: Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has indexed {var_name}')


async def main():
    queue = asyncio.Queue()

    for i in range(5):
        queue.put_nowait({'kid': '169ee0d2-3046-4af9-8064-c8fe0be28b52', 'var_name': f'df{i}'})

    tasks = []

    for i in range(queue.qsize()):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
