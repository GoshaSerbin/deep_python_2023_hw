import argparse
from comparison import test
from memory_profiler import profile


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repeats_number", default=15)
    parser.add_argument("-n", "--objects_number", default=100000)
    args = parser.parse_args()
    test = profile(test)
    test(int(args.repeats_number), int(args.objects_number))
