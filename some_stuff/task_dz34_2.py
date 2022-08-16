# import asyncio
#
#
# async def calculate(a):
#     return a**a
#
#
# async def dots_printer():
#     for i in range(100):
#         print(".", end="")
#
#
# async def stop_event_loop(loop):
#     loop.stop()
#     print("Endloop")
#
#
# async def set_future(future):
#     print("Future set result..")
#     future.set_result(10)
#
#
# async def wait_for_future(future):
#     result = await future
#     print("Future set result {}".format(result))
#
#
# event_loop = asyncio.get_event_loop()
# fut = asyncio.Future()
# event_loop.create_task(dots_printer())
#
# event_loop.create_task(calculate(11111))
#
# event_loop.create_task(set_future(fut))
#
# event_loop.create_task(wait_for_future(fut))
#
# event_loop.run_forever()
# event_loop.close()

# def rec(a, b, c):
#     if a == b:
#         print(c)
#         return
#     c += b
#     return rec(a, b-1, c)
#
# rec(0, 10, 0)

# def rec(n):
#     if n == 0:
#         return
#     a = rec(n-1)
#     a += 1
#     print(a * '*')
#     return rec(n-1)
#
#
# rec(4)

# def fibonacci(n):
#     if n == 0:
#         return 0
#     if n == 1:
#         return 1
#     return fibonacci(n-1) + fibonacci(n-2)
#
# print(fibonacci(37))


# class Dog:
#
#     def __init__(self, name, weight, age, paws_number=4):
#         self.paws_number = paws_number
#         self.ears_number = 2
#         self.tail_number = 1
#         self.__voice = 'Yaff!'
#         self.name = name
#         self.weight = weight
#         self.age = age
#
#     def speak(self, woof='Woof!'):
#         print(f'dog says: {woof}')
#
#     def speak_voice(self):
#         print(f'dog.say: {self.__voice}')
#
#     def move(self):
#         print('run')

# def set_inner_voice(self, voice):
#     self.__voice = voice
#
# def get_inner_voice(self):
#     return self.__voice

# jack = Dog('jack', 34, 3, 3)
#
# print(jack.paws_number)
# print(jack.name)
# jack.speak()
# jack.speak('Grrr')
#
#
# jack.speak_voice()
# # jack.set_inner_voice('Argh!')
# # print(jack.get_inner_voice())
# jack.speak_voice()
#
#
# class Shephard(Dog):
#
#     def speak(self, voice='Arhghrhghhrr'):
#         return super(Shephard, self).speak(voice)
#
#
# rex = Shephard('Rex', 45, 5, 4)
# rex.paws_number = 3
# rex.owner = 'Jim'
# print(rex.paws_number)
# rex.speak()
# Написать два класса
#
# Pen & Paper
#
# ручка имеет запас чернил
#
# её можно заправлять или менять стержень
#
# ручка пишет, расходуя чернила
#
# ручка пишет на бумаге,
#
# пишет пока есть место на бумаге
#
# пробелы в тексте не вычитаются из запасов чернил
#
# бумага имеет место, чтобы на ней писать
#
# бумага хранит текст
#
#
# текст, написанный на бумаге, можно прочитать(отдельным методом)


# class Paper:
#     def __init__(self):
#         self.space = 100
#         self.text = ''
#
#     def read(self):
#         return print(self.text)
#
#
# class Pen:
#     def __init__(self, paper: Paper):
#         self.ink = 100
#         self.paper = paper
#
#     def write(self, paper, letters=''):
#         if self.ink >= len(letters) and paper.space >= len(letters):
#             for i in letters:
#                 if i == ' ':
#                     continue
#                 self.ink -= 1
#                 paper.space -= 1
#             if paper.space < 100:
#                 paper.text += ' ' + letters
#             else:
#                 paper.text += letters
#         else:
#             return print('it seems there is not enough space for writing or ink in pen.')
#
#     def refill(self, inks=0):
#         if self.ink == 100:
#             return print('Your pen already full')
#         if (self.ink + inks) <= 100 and inks > 0:
#             self.ink += inks
#             return print(f'Your pen has been refilled with {inks} value')
#         else:
#             return print('It seems your ink input is more than pen can receive')
#
#
# paper1 = Paper()
# pen1 = Pen(paper1)
# pen1.write(paper1, 'Hello OOP')
# paper1.read()
# print(pen1.ink)
# pen1.refill((9))
# print(pen1.ink)
# pen1.write(paper1, 'Hello OOP')
# paper1.read()
# print(pen1.ink)


# class BelowZeroError(Exception):
#     pass
#
#
# class Thermometr:
#     scale = 'K'
#     object_count = 0
#
#     @classmethod
#     def get_object_count(cls):
#         return cls.object_count
#
#     def __init__(self, temp=0):
#         if temp == 0:
#             raise BelowZeroError('Please use Kelvin scale')
#         self.__temp = temp
#         Thermometr.object_count += 1
#
#     def get_temp(self):
#         if Thermometr.scale == 'F':
#             return (self.__temp - 273) * 9 / 5 + 32
#         if Thermometr.scale == 'C':
#             return self.__temp - 273
#         return self.__temp
#
#     def __del__(self):
#         Thermometr.object_count -= 1
#
#
# if __name__ == '__main__':
#     therm1 = Thermometr(273)
#     Thermometr.scale = 'C'
#     print(therm1.get_temp())
#     print(Thermometr.object_count)
#     del therm1
#     print(Thermometr.get_object_count())


# class Node:
#
#     def __init__(self, value):
#         self.value = value
#         self.next = None
#
#
# class Llist:
#
#     def __init__(self):
#         self.head = None
#         self.tail = None
#         self.current = None
#
#     def append(self, node):
#         if self.head is None:
#             self.head = node
#             self.tail = node
#             self.current = self.head
#         else:
#             if self.tail == self.head:
#                 self.tail = node
#                 self.head.next = self.tail
#             else:
#                 self.tail.next = node
#             self.tail = node
#
#     def showlist(self):
#         node = self.head
#         print(node.value)
#         while node.next:
#             print(node.next.value)
#             node = node.next
#
#     def __add__(self, node):
#         if isinstance(node, Node):
#             self.append(node)
#         else:
#             self.append(Node(node))
#
#     def next(self):
#         current, self.current = self.current, self.current.next
#         return current
#
#     def __repr__(self):
#         node = self.head
#         repr_ = [self.head.value]
#         while node.next:
#             repr_.append(node.next.value)
#             node = node.next
#         return ' -> '.join(repr_)
#
#
# n1 = Node('a')
# n2 = Node('b')
# n3 = Node('c')
# n4 = Node('d')
# llist = Llist()
#
# llist.append(n1)
# llist.append(n2)
# llist.append(n3)
#
# llist + n4
# llist + 'e'
# # llist.showlist()
#
# # print(llist.next().value)
# # print(llist.next().value)
# # print(llist.next().value)
# # print(llist.next().value)
# print(llist)


# class Node:
#     def __init__(self, data=None, right=None, left=None):
#         self.data = data
#         self.left = left
#         self.right = right
#
#     def __str__(self):
#         return 'Node ['+str(self.data)+']'
#
#
# class Tree:
#     def __init__(self):
#         self.root = None
#
#     def newNode(self, data):
#         return Node(data, None, None)


# def move_zeros(lst):
#     hashmap = []
#     n = 0
#     for i in lst:
#         if i != 0:
#             n += 1
#             hashmap.append(i)
#     zero_lst = [0 for x in range(0, n)]
#     fin = hashmap + zero_lst
#     return fin
#
#
# lst = [9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]
# move_zeros(lst)

# def balanced_parens(n):
#     res = []
#     elem = "()"
#     if n == 0:
#         return [""]
#
#
#
# balanced_parens(1)
# import itertools


# def jumbled_string(s, num):
#     n = 0
#     k = -3
#     res = []
#     mylist = list(s)
#     num -= 1
#     for idx, i in enumerate(mylist):
#         k -= 1
#         if idx % 2 == 0:
#             res.insert(n, i)
#             n += 1
#         else:
#             res.insert(k, i)
#
#     fin = ''.join(reversed(res))
#     if num == 0:
#         return print(fin)
#     return jumbled_string(fin, num)
#
#
# s = "Such Wow!"
#
# jumbled_string(s, 105)
