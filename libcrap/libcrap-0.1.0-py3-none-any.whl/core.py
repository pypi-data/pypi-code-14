from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm
from typing import List, Iterable, Tuple, Callable, Any, TypeVar

T1 = TypeVar('T1')
T2 = TypeVar('T2')


def _decorate_for_enumeration(func: Callable[[T1], T2]) \
-> Callable[[Tuple[int, T1]], Tuple[int, T2]]:
    def decorated(pair: Tuple[int, T1]) -> Tuple[int, T2]:
        index, elem = pair
        return (index, func(elem))
    return decorated


def _enumerated_sort_key(pair: Tuple[int, Any]) -> int:
    index, elem = pair
    return index


def map_thread_parallel(
    func: Callable[[T1], T2],
    iterable: Iterable[T1],
    use_progress_bar: bool = False
) -> List[T2]:
    """Maps func over iterable in a multithreaded way. It is useful
    if func performance is bounded because of IO operations or sleeping
    or something like that. Returns a list. Very similar to map function.

    If use_progress_bar == True, then it uses tqdm to print a nice
    progress bar that works in terminal and in jupyter notebook."""
    with ThreadPoolExecutor() as executor:
        if use_progress_bar:
            decorated_func = _decorate_for_enumeration(func)
            futures = [executor.submit(decorated_func, pair)
                       for pair in enumerate(iterable)]
            results = [future.result() for future in tqdm(
                as_completed(futures), total=len(futures))]
            return [pair[1] for pair
                    in sorted(results, key=_enumerated_sort_key)]
        else:
            return list(executor.map(func, iterable))
