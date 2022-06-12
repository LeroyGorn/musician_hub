import random
import string


class MyIterator:
    class MyIter:
        def __init__(self, iterable):
            self._iterable = iterable
            self.counter = 0

        def __next__(self):
            if self.counter == len(self._iterable.mydict):
                raise StopIteration()
            result = list(map(lambda kv: (kv[0], kv[1]), self._iterable.mydict.items()))[self.counter]
            self.counter += 1
            return result

    def __init__(self):
        self.mydict = {}

    def add_dict(self, item):
        self.mydict = item

    def __iter__(self):
        return self.MyIter(self)


my_dictionary = {'a': 2, 'v': 3, 'b': 33}
d = MyIterator()
d.add_dict(my_dictionary)
it = iter(d)
print(next(it))
print(next(it))
print(next(it))


def sample_list(num):
    your_list = []
    length = random.randint(2, 10)
    letters = string.ascii_lowercase
    for i in range(num):
        rand_string = ''.join(random.choice(letters) for j in range(length))
        your_list.append(rand_string)

    return your_list


print(sample_list(5))
