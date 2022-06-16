"""
Given an array of integers, find all pairs in the array that sum up to a given target value.
In other words, given an array arr and a target value target, return all pairs a, b such that a + b = target.
Assumptions:
- input array is not sorted
- elements are unique in the input array
Example:
Input array: [7, 12, 3, 1, 2, -6, 5, -8, 6]
Target sum: 0
Output: [(-6,6)]
-6 6
Target sum: 8
Output: [(7,1), (3,5), (2, 6)]
7 1
3 5
2 6
"""


def find_pairs(arr, arr_size, res):
    hashmap = {}

    for i in range(0, arr_size):
        temp = res - arr[i]
        if (temp in hashmap):
            print(f'Pair with given sum {res} is ({temp},{arr[i]}) at indices ({hashmap[temp]},{i})')
        hashmap[arr[i]] = i


data = [7, 12, 3, 1, 2, -6, 5, -8, 6]
n = 0
find_pairs(data, len(data), n)
