from  dask.distributed import (
    as_completed,
    Client,
    wait
)
from itertools import islice

def parallel_for(iterables,
                 task_fn,
                 *task_args,
                 task_completed=None,
                 chunk_size=None,
                 client=None):
    """
    Parallelise l'appel de task_fn sur chaque element de iterables.

    iterables:
        elements sur lesquels task_fn va etre appele

    *task_args:
        arguments passes a task_fn en plus de l'iterable courant

    task_completed:
        callback appele apres que chaque appel a task_fn ait termine

    client:
        dask client

    chunk_size:
        au lieu de faire l'appel a task_fn pour chaque iterable, decoupe
        iterables en chunk_size elements. task_fn sera reponsable de faire
        la 'sous iteration'
    """
    exec = Client() if client is None else client

    def chunkify_iterables():
        if chunk_size is None:
            yield from iterables
        else:
            it = iter(iterables)
            yield from iter(lambda: list(islice(it, chunk_size)), [])

    def generate_futures():
        if task_args is None or len(task_args) == 0:
            for i in chunkify_iterables():
                yield exec.submit(task_fn, i)
        else:
            for i in chunkify_iterables():
                yield exec.submit(task_fn, *task_args, i)

    futures = [f for f in generate_futures()]

    if task_completed is None:
        wait(futures)
    else:
        for f in as_completed(futures):
            task_completed(f.result())

    if client is None:
        exec.close()

def create_dask_local_client(**kwargs):
    return Client(**kwargs)
