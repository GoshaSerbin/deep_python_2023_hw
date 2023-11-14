import argparse
import weakref
import time
import numpy as np


from layers import Linear, SlotsLinear, WeakrefLinear


def print_time_ms(name: str, t: float):
    print(f"{name + ':' : <10}{1000*t:>10.4f}")


def test(repeats_number: int, model_depth: int):
    feature_size = 5
    x = np.random.rand(feature_size)
    b = np.ones_like(x)
    w = np.identity(feature_size)

    print(f"INSTANCES CREATION ({model_depth} objects): in msec")

    t1 = time.time()
    for _ in range(repeats_number):
        layers = [Linear(w, b) for _ in range(model_depth)]
    t2 = time.time()
    print_time_ms("Default", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        slots_layers = [SlotsLinear(w, b) for _ in range(model_depth)]
    t2 = time.time()
    print_time_ms("Slots", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        weakref_layers = [WeakrefLinear(w, b) for _ in range(model_depth)]
    t2 = time.time()
    print_time_ms("Weakref", (t2 - t1) / repeats_number)

    print(f"READ OPERATION ({model_depth} objects): in msec")

    t1 = time.time()
    for _ in range(repeats_number):
        x = np.random.rand(feature_size)
        for layer in layers:
            x = layer.forward(x)
    t2 = time.time()
    print_time_ms("Default", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        x = np.random.rand(feature_size)
        for layer in slots_layers:
            x = layer.forward(x)
    t2 = time.time()
    print_time_ms("Slots", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        x = np.random.rand(feature_size)
        for layer in weakref_layers:
            x = layer.forward(x)
    t2 = time.time()
    print_time_ms("Weakref", (t2 - t1) / repeats_number)

    print(f"WRITE OPERATION ({model_depth} objects): in msec")

    t1 = time.time()
    for _ in range(repeats_number):
        for layer in layers:
            layer.weights = w
            layer.biases = b
    t2 = time.time()
    print_time_ms("Default", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        for layer in slots_layers:
            layer.weights = w
            layer.biases = b
    t2 = time.time()
    print_time_ms("Slots", (t2 - t1) / repeats_number)

    t1 = time.time()
    for _ in range(repeats_number):
        for layer in weakref_layers:
            layer.weights = weakref.ref(w)
            layer.biases = weakref.ref(b)
    t2 = time.time()
    print_time_ms("Weakref", (t2 - t1) / repeats_number)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repeats_number", default=15)
    parser.add_argument("-n", "--objects_number", default=100000)
    args = parser.parse_args()
    test(int(args.repeats_number), int(args.objects_number))
