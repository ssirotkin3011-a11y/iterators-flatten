import types


# ======================
# 1. Итератор (1 уровень)
# ======================

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer = 0
        self.inner = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.outer >= len(self.list_of_list):
            raise StopIteration

        current_list = self.list_of_list[self.outer]

        if self.inner >= len(current_list):
            self.outer += 1
            self.inner = 0
            return self.__next__()

        item = current_list[self.inner]
        self.inner += 1
        return item


# ======================
# 2. Генератор (1 уровень)
# ======================

def flat_generator(list_of_lists):
    for sublist in list_of_lists:
        for item in sublist:
            yield item


# ======================
# 3. Итератор (любой уровень)
# ======================

class FlatIteratorRecursive:

    def __init__(self, list_of_list):
        self.stack = [iter(list_of_list)]

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            try:
                item = next(self.stack[-1])
            except StopIteration:
                self.stack.pop()
                continue

            if isinstance(item, list):
                self.stack.append(iter(item))
            else:
                return item

        raise StopIteration


# ======================
# 4. Генератор (любой уровень)
# ======================

def flat_generator_recursive(list_of_list):
    for item in list_of_list:
        if isinstance(item, list):
            yield from flat_generator_recursive(item)
        else:
            yield item


# ======================
# ТЕСТЫ
# ======================

def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    assert list(FlatIterator(list_of_lists_1)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None
    ]


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    assert list(flat_generator(list_of_lists_1)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None
    ]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    assert list(FlatIteratorRecursive(list_of_lists_2)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!'
    ]


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    assert list(flat_generator_recursive(list_of_lists_2)) == [
        'a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!'
    ]

    assert isinstance(flat_generator_recursive(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
    print("✅ Все тесты пройдены")