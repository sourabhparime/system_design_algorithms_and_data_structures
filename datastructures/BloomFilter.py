"""
Youtube Video: https://www.youtube.com/watch?v=Bay3X9PAX5k
Bloom Filter Configurator: https://hur.st/bloomfilter/
Bloom Filter GFG: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
@classmethod decorator: https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/

A. Bloom Filter is a probablistic hashmap - like data structure that had two methods:
1. add : adds an emlement to the set
2. contains: return False with 1.0 confidence but True with  < 1.0 confidence

NOTE: Elements from Bloom Filter cannot be removed.
B. Bloom Filter is space efficient to fit in memory to execute membership test.
"""

import math
from random import shuffle

import mmh3
from bitarray import bitarray


# mmh is a fast non cryptographic hashing algorithm and bitarray is the binary bits represented as an array

class BloomFilter(object):

    def __init__(self, item_count, fault_tolerance=0.05):
        self.item_count = item_count
        self.fault_tolerance = fault_tolerance

        # need to assign the size of the array
        self.size = self.get_size(item_count, fault_tolerance)

        # need to assign the number of hash functions needed
        self.hash_count = self.get_hash_count(self.size, item_count)

        # initialize the bit array
        self.bitarray = bitarray(self.size)
        self.bitarray.setall(0)

    # public methods to add and check for membership
    def add(self, element):

        for hash_index in range(self.hash_count):
            # mmh3 is the hash function
            digest = mmh3.hash(element, hash_index) % self.size
            self.bitarray[digest] = True

    def check(self, element):
        #print("Printing bit array for debug")
        #print(self.bitarray)
        for hash_inex in range(self.hash_count):
            digest = mmh3.hash(element, hash_inex) % self.size

            if not self.bitarray[digest]: return False

        return True

    @staticmethod
    def get_size(n, fault_tol):
        """
        Size is returned based on a formula
        :param n:
        :param fault_tol:
        :return:
        """
        m = -(n * math.log(fault_tol)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(size, n):
        """
        Size is the derived size and n is the number of items
        :param size:
        :param n:
        :return:
        """

        hash_count = (size / n) * math.log(2)
        return int(hash_count)


def test_bloom_filter():
    n = 20  # no of items to add
    p = 0.05  # false positive probability

    bloomf = BloomFilter(n, p)
    print("Size of bit array:{}".format(bloomf.size))
    print("False positive Probability:{}".format(bloomf.fault_tolerance))
    print("Number of hash functions:{}".format(bloomf.hash_count))

    # words to be added
    word_present = ['abound', 'abounds', 'abundance', 'abundant', 'accessable',
                    'bloom', 'blossom', 'bolster', 'bonny', 'bonus', 'bonuses',
                    'coherent', 'cohesive', 'colorful', 'comely', 'comfort',
                    'gems', 'generosity', 'generous', 'generously', 'genial']

    # word not added
    word_absent = ['bluff', 'cheater', 'hate', 'war', 'humanity',
                   'racism', 'hurt', 'nuke', 'gloomy', 'facebook',
                   'geeksforgeeks', 'twitter']

    for item in word_present:
        bloomf.add(item)

    shuffle(word_present)
    shuffle(word_absent)

    test_words = word_present[:10] + word_absent
    shuffle(test_words)
    for word in test_words:
        if bloomf.check(word):
            if word in word_absent:
                print("'{}' is a false positive!".format(word))
            else:
                print("'{}' is probably present!".format(word))
        else:
            print("'{}' is definitely not present!".format(word))


print("Testing Bloom Filter")
test_bloom_filter()
