## What?
An asynchronous benchmark library for Python 3.6+

Please note that this project is currently alpha quality and the API is not finalized. Please provide feedback if you think the API is convenient enough or not. A permissive license will be chosen once the API will be more mature for wide spread consumption.

## Roadmap
- [ ] API Finalization
- [ ] Choose license
- [ ] Resolve all TODO in code
- [ ] More test coverage and test out network I/O failure and concurrency

## Installing
For now you can install this via this github repository by pip installing or adding to your requirements.txt file:

```
git+git://github.com/tzickel/asyncbenchmark@master#egg=asyncbenchmark
```

Replace master with the specific branch or version tag you want.

## Example
```python
from asyncbenchmark import create_test_plan, formalize_test_plan, run_test_plan
import asyncio


async def func1():
    await asyncio.sleep(0.5)


async def func2():
    await asyncio.sleep(0.2)


async def main():
    example = create_test_plan(('func1', 'func2'))

    example = formalize_test_plan(example, {'func1': func1, 'func2': func2})

    results = await async_run_test_plan(example1)

    pprint.pprint(results)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```

You can check the [tests](tests/test.py) for some more examples.

## API
This is all the API in a nutshell:

```python
async async_run_test_plan(plan, max_concurrent=None, skip_on_max_concurrent=False)
run_test_plan(*args, **kwargs):
create_test_plan(funcs, how_long=5, max_jobs_at_timestamp=5, chance_for_more_job_at_timestamp=0.5, chance_for_jobs_at_timestamp=0.2, minimal_time_step=0.001)
formalize_test_plan(plan, funcs)
```
