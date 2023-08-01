###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here

    with open(filename, 'r') as cow_data:
        cow_dict = {}
        for line in cow_data.read().split('\n'):
            data = line.split(',')
            cow_dict[data[0]] = int(data[1])

    return cow_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here

    avail_cows, trips = sorted(cows.keys(), key=lambda i: cows[i], reverse=True), []
    while avail_cows != []:
        cur_limit, trip, unused_cows = limit, [], []
        for cow in avail_cows:
            if cur_limit - cows[cow] >= 0:
                trip.append(cow)
                cur_limit -= cows[cow]
            else:
                unused_cows.append(cow)
        trips.append(trip)
        avail_cows = unused_cows.copy()

    return trips


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here

    for trips in get_partitions(cows):
        if all(sum(cows[cow] for cow in trip) <= limit for trip in trips):
            return trips


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here

    data = load_cows('ps1_cow_data.txt')
    s = time.time()
    n_trips = len(greedy_cow_transport(data))
    e = time.time()
    print(f'Greedy\'s number of trips: {n_trips} trips, '
          f'found in {round(e-s, 4)}s.')

    s = time.time()
    n_trips = len(brute_force_cow_transport(data))
    e = time.time()
    print(f'Brute\'s number of trips: {n_trips} trips, '
          f'found in {round(e-s, 4)}s.')


if __name__ == '__main__':
    main_dict = load_cows('ps1_cow_data.txt')
    test_dict = {'a': 6, 'b': 3, 'c': 2, 'd': 5}

    print(main_dict)
    print(dict(sorted(main_dict.items(), key=lambda dict: dict[1], reverse=True)))

    print(greedy_cow_transport(test_dict))
    print(greedy_cow_transport(main_dict), '\n\n')

    print(brute_force_cow_transport(test_dict))
    print(brute_force_cow_transport(main_dict), '\n\n')

    compare_cow_transport_algorithms()
