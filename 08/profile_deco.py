import cProfile
import pstats
import io


def profile_deco(func):
    profiler = cProfile.Profile()

    def print_stat():
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.print_stats()
        print("\n".join(s.getvalue().splitlines()[4:-3]))

    def inner(*args, **kwargs):
        profiler.enable()
        res = func(*args, **kwargs)
        profiler.disable()
        return res

    setattr(inner, "print_stat", print_stat)

    return inner


@profile_deco
def func1(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


func1(21, 2)
func1(21, 2)
func1(21, 2)
func1(21, 2)

sub(2, 2)

func1.print_stat()
sub.print_stat()
