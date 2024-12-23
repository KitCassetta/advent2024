from log_util import get_logger

logger = get_logger(__name__)

from collections import defaultdict

FILENAME = "d23.txt"


def parse_input(filename):
    with open(filename) as input_file:
        data = [row.split("-") for row in input_file.read().split("\n")]
    graph = defaultdict(set)
    for node, neighbor in data:
        graph[node].add(neighbor)
        graph[neighbor].add(node)
    return graph


def get_three_membered_cycles(graph):
    three_membered_cycles = set()
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            common_neighbours = neighbours & graph[neighbour]
            if common_neighbours:
                three_membered_cycles |= {
                    tuple(sorted([node, neighbour, common_neighbour]))
                    for common_neighbour in common_neighbours
                }
    return three_membered_cycles


def part_one(three_membered_cycles):
    return sum(
        any(node.startswith("t") for node in cycle) for cycle in three_membered_cycles
    )


def part_two(graph):
    parties = {frozenset({node}) for node in graph.keys()}
    while len(parties) > 1:
        new_parties = set()
        for party in parties:
            for node in graph.keys():
                if party <= graph[node]:
                    new_parties.add(party | {node})
        parties = new_parties
    return ",".join(sorted(list(parties)[0]))


def main():
    graph = parse_input(FILENAME)
    three_membered_cycles = get_three_membered_cycles(graph)
    logger.info(part_one(three_membered_cycles))
    logger.info(part_two(graph))


if __name__ == "__main__":
    main()
# ref bakibol
# ref https://topaz.github.io/paste/#XQAAAQAeBgAAAAAAAAAzHIoib6pXbueH4X9F244lVRDcOZab5q1+VXY/ex42qR7D+RY2M8BnG/wd6
# /9gu6yJ2pXv5xAtKp4IgK+gWrjT2/4QaKJwedNfpU1I/cS7Nm/JvC6FHJGZCp3fEGcc0awWqa5DbsOm5kFSs3Z7mUoFi7JfrcVzhAdFXJKjZTUZNFDG
# +hc5qF2LRHvfmpVNX6NYDuVviBmXNDWDgsZ6wzqQOQSyRJRHbcpjyiDjC1dSz+KESrBtdvrqZCvBn35lb2ScfjsvWyPmtlEfRmGy2mYGsEb+HbkQ
# /lIt0LW6jX/922+tJD563TeHegS+s24prpW48YvHA5tcg2rhRR7PUV3G2zcpdeQ/iMtdB9ekE+slaN4JHEqYTq8KNAgVqXf6vnWT
# /khJGd3rMiJAQszkOI5Ouv6OQheMAaBrYzRWgcBsVQxhlo3DxNKtxyaYZKzgOlGhUZwAFme0GWIJBe47KYc3ce4AvkkZARF5BBVkrlaMelnKR25qmDv7JtJ5lQ8jBDIiBLh32nkGpzsLKnRoBKPI5U9G3AEDQP2kqExu1jCqbiOaT+iEGYNJaRkQdACb8ngxQSithzLo+kMzsYjLxI52R/Z6qaNI2x6jCetQdXs9vsbbhdyGelZqEjNHVJ8rDmBGKHY2WK+Eb9I/179qSQR8tOSqHMiWf+QZEoq7zSev3GQDgJX52sQ6MH7P9VR2VRwbjyS6A2R7zgqIntqDqS2yICr0OH+SHzBn2Xcrdq0JxFTpQ+90nvelV4twBZpwULU9uPtc9mUl/5lkCWw=
