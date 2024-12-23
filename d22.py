import sys
from collections import defaultdict

# we run into "RecursionError: maximum recursion depth exceeded" after 1000 numbers otherwise
sys.setrecursionlimit(3000)


def mix_n_prune(number, secret):
    secret = number ^ secret
    secret = secret % 16777216
    return secret


def calculate_next_number(secret):
    number = secret * 64
    secret = mix_n_prune(number, secret)

    number = secret // 32
    secret = mix_n_prune(number, secret)

    number = secret * 2048
    secret = mix_n_prune(number, secret)

    return secret


def recurse(secret, depth):
    global pricelist
    if depth == 0:
        return secret

    pricelist.append(secret % 10)  # %10 effectively gets the last digit
    depth -= 1
    return recurse(calculate_next_number(secret), depth)


# read in my input; a bunch of integers like 4832674, 14802956, 7210529, ...
with open("d22.txt") as fname:
    buyers = fname.read().splitlines()
buyers = map(int, buyers)

global pricelist
# defaultdict allows you to += values even when a key doesn't exist yet
dict_of_sequences = defaultdict(int)
part1_accumulator = 0

for buyer in buyers:
    pricelist = []  # resets for each buyer
    seen_seq = set()  # restes for each buyer
    # resets for each buyer, we need a dummy value to start with so the lists line up later
    difflist = [-999]

    part1_accumulator += recurse(buyer, 2000)  # this populates the pricelist

    # generate difflist
    for i in range(1, len(pricelist)):
        difflist.append(pricelist[i] - pricelist[i - 1])

    # rolling window, get the price and the sequence that led up to it
    for i in range(4, len(pricelist) + 1):
        # needs to be a tuple for a dictionary key
        sequence = tuple(difflist[i - 4: i])
        price = pricelist[i - 1]

        if sequence in seen_seq:  # only take the FIRST time we see that sequence
            continue
        else:
            seen_seq.add(sequence)
            # add that sequence price to a running total from all buyers
            dict_of_sequences[sequence] += price

print("Part 1:", part1_accumulator)

# find the key that corresponds to the max value, then look up that key in the dictionary
print("Part 2:", dict_of_sequences[max(dict_of_sequences, key=dict_of_sequences.get)])
# ref: https://topaz.github.io/paste/#XQAAAQDjCAAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXY/ex42qR7D
# +RLbGM8VWwmFQzJAgb3vYR+Sz5vF7x7iofpu//GGMwOBUviuc30Fe4NTLNS8DNAsXj1ULESzuKxiH7dnbzIGJe9hbxqDEIeJhOF70nDC8i+hoZjzbQ
# +FH1Ym6tKCnoyRYKeDBjwCSnj5+uTaUwgaR8RTO4m5PepHDry2cmQ1iw7rKsDcqiVjOWm03jC+XWZ22kDgqT4BMoSRtfNZtgJpFbFz
# /spKQjgOZHtYJZhR3xK3nT26AKhrcCUpCYuHy+zlPTRLPcOXG1LQtpG9qnImzqN45MexunAcXWwo5HJlWbx+Xg138qjRRfPsbrIbNGPqTlQhFrbsBAh
# /QpkYE56kdmAD9nPzwHLTLK92W5gtQHj7M8U2pp6bj/XsJ7sfAmzUPgZw8rBBentGvrlLScEqE1
# +eoAFeo95LLOQfwjsfJeXpxXASXKFn0CHssKMjxbU1zwmkHAVG5jhMcUdCjE3Iih8Fn/mAN1tgMy1NQnCc612AD8Q0qIOkhGnPuYtt
# +8djDVcvBeoRpJ1GvndXa/aFyDDGsLhBRTuxzw87MbkRRlidlivL+cOamJ7KnpIM3WE+noulcQglEbkV0+l40
# +M4VvU1vclHhDIW5LQtjWwvdi9cRot6yH1cIvXen16P9v1o9lIiXQyuJxNUPlpRUy724PGVv+zzKJa
# +eIOqkM62U0hihbEOgg2GYNVSeZoEQWa4Yr2x74yxBZ4X1m30f0xc5cWQBlpH8xhvm7vZMQMU7e3M4hdoVveyUHfWJJJbTh0h8TSFbN5qa
# /AuMHlAHKTSCZNHkeCoMOjVCAXL1Ybic1SizGvhsqhnx8BgqIKLWg/zhx5FkqTyv2/qlxGJdJz7/RGwfFLw6Po+OCupcvRFK35UjJC
# +YBnQqeHFMhlazieHXzl3iqfDBtX1yAwJTkI6IJqDfJphlv1/DTvNw0m/i4vp5WEaEhixkxe8Wwqx
# /E7uNebXMFE3SCpQfSjoEVT6bBcNGiIqxqfQtuaTF6/z2zBObcOJbd3wgA4Tb65CitliS6C3M/LMR1CJ2U2hspHhNixjFKAoM1h0
# +mKy9kwk6Kagb0iRM0jMZHwAZu1T8JtEbgzvCP7/7rIILZxGc7nqXNneeHgFuWJvUmNHEEjeBQ6lOsqjmi5gAuqe52JHq/xHRyqfNd9GI9cDQk
# /zsN9MKhSk8U93oIJXbQbGPIql5A8lV12opme4aHXLB91SgU9J/AQWReZvMMQvB8/ZSIyKc6gx9J3NbpfNmcw5lcoGXIupawQU9d
# /ke4xhkaoC3rK04mhMsEGYaGrMgCmhPYP/akThAA==
