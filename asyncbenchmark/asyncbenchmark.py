import time
import asyncio
import random


async def async_run_test_plan(plan, max_concurrent=None, skip_on_max_concurrent=False):
    async def timemethod(timedata, semaphore, counter, func, times=1):
        try:
            if semaphore:
                if semaphore.locked() and skip_on_max_concurrent:
                    return
                await semaphore.acquire()
            times_tmp = []
            for _ in range(times):
                s = time.perf_counter()
                await func()
                e = time.perf_counter()
                times_tmp.append(e - s)
            timedata.setdefault(func, []).extend(times_tmp)
        except Exception as e:
            # TODO handle this
            timedata.setdefault(func, []).append(e)
        finally:
            counter[0] -= 1
            if semaphore:
                semaphore.release()

    current_time = 0.0
    timedata = {}
    counter = [len(plan)]
    plan = sorted(plan, key=lambda x: x[0])
    if max_concurrent:
        semaphore = asyncio.Semaphore(max_concurrent)
    else:
        semaphore = None

    for timestamp, func in plan:
        if not timestamp == current_time:
            await asyncio.sleep(timestamp - current_time)
        current_time = timestamp
        asyncio.ensure_future(timemethod(timedata, semaphore, counter, func))

    while counter[0] != 0:
        await asyncio.sleep(1)

    results = {}
    for func, times in timedata.items():
        min_time = min(times)
        max_time = max(times)
        median_time = sorted(times)[len(times) // 2]
        mean_time = sum(times) / len(times)
        results[func.__name__] = {'min': min_time, 'max': max_time, 'median': median_time, 'mean': mean_time, 'items': len(times) }

    return results


def run_test_plan(*args, **kwargs):
    return asyncio.get_event_loop().run_until_complete(async_run_test_plan(*args, **kwargs))


# TODO support setting times parameter ?
def create_test_plan(funcs, how_long=5, max_jobs_at_timestamp=5, chance_for_more_job_at_timestamp=0.5, chance_for_jobs_at_timestamp=0.2, minimal_time_step=0.001):
    if isinstance(funcs, dict):
        funcs = funcs
    elif isinstance(funcs, (list, tuple)):
        funcs = {x: 1 / len(funcs) for x in funcs}
    else:
        funcs = {funcs: 1}

    test_plan = []
    current_time = 0.0
    while current_time < how_long:
        cmds = []
        chance = random.random()
        if chance < chance_for_jobs_at_timestamp:
            for _ in range(max_jobs_at_timestamp):
                chance = random.random()
                if chance < chance_for_more_job_at_timestamp:
                    which = random.random()
                    now = 0.0
                    for func, chance in funcs.items():
                        now += chance
                        # TODO <= ?
                        if which < now:
                            break
                    cmds.append(func)
        test_plan.extend([(current_time, x) for x in cmds])
        current_time += minimal_time_step
    return test_plan


def formalize_test_plan(plan, funcs):
    ret = []
    for item in plan:
        item = list(item)
        item[1] = funcs[item[1]]
        ret.append(item)
    return ret


if __name__ == "__main__":
    import pprint

    async def func1():
        await asyncio.sleep(0.5)

    async def func2():
        await asyncio.sleep(0.2)

    #example = [(0.01, func1), (0.01, func2), (0.5, func1)]
    example = create_test_plan(('func1', 'func2'))

    example1 = formalize_test_plan(example, {'func1': func1, 'func2': func2})

    results1 = run_test_plan(example1)#, 1, True)

    pprint.pprint(results1)
