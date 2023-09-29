import time


class InvalidArguments(Exception):
    pass


def mean(k: int):
    if k < 1:
        raise InvalidArguments("k must be positive integer")

    def mean_decorator(func):
        last_k_times = []

        def inner(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            last_time = end_time - start_time

            nonlocal last_k_times
            last_k_times.append(last_time)
            nonlocal k
            last_k_times = last_k_times[-k:]

            mean_time = 0
            if len(last_k_times) < k:
                mean_time = sum(last_k_times) / len(last_k_times)
            else:
                mean_time = sum(last_k_times) / k
            print(f"{mean_time}")

            return res

        return inner

    return mean_decorator
