from itertools import chain, zip_longest, tee, islice
from functools import partial


class LastItem(object):
    pass


def kwurry(fn):
    kwurried = lambda *args, **kwargs: fn(*args, **kwargs) if len(args) else kwurried


last = LastItem()
ident = lambda x: x
# flatten = chain.from_iterable
join = lambda it: zip(*list(iter(it)))
join_max = lambda it, fill=None: zip_longest(*list(iter(it)), fillvalue=fill)
join_max.partial = partial(partial, join_max)
copy = lambda it, n=2: tee(it, n)
copy.partial = partial(partial, copy)
chop = lambda it, start=0, stop=None, step=1: islice(it, start, stop, step)
chop.partial = partial(partial, chop)
# TODO: Add a buffer fn that buffers a certain number of items, and adds a peek fn to the iterable to peek into the buffer.

def flatten(it):
    for i in it:
        try:
            yield from i
        except TypeError:
            yield i

def take(it, n=1):
    for _ in range(n):
        yield next(it)
take.partial = partial(partial, take)

def every(it, n=1):
    for idx, i in enumerate(it, 1):
        if idx % n == 0:
            yield i
every.partial = partial(partial, every)

def each(it, fn=ident):
    try:
        fns = iter(fn)
    except TypeError:
        fns = (fn,)
#     fns = fn if len(fn) else (fn,)
    for fn, i in zip(fns, it):
        yield fn(i)
    for i in it:
        yield fn(i)
each.partial = partial(partial, each)

def keep(it, fn=ident):
    for i in it:
        if fn(i):
            yield i
keep.partial = partial(partial, keep)

def compose(*fns):
    def composed(it):
        for fn in fns:
            it = fn(iter(it))
        return it
    return composed

# c = compose(every.partial(n=5))
# list(c(iter(range(1, 30))))

