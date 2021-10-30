#!/usr/bin/python3
"""
IMPORTS
"""
import argparse
import readchar
import random
import string
import time
from datetime import datetime
from collections import namedtuple
from pprint import pprint
from colorama import Fore, Style

"""
NamedTuple definition
"""
Input = namedtuple('Input', ['requested', 'received', 'duration'])

"""
Functions definition
"""
def checkEndgame(args, start_date, num_types):
    """Check if game should end

    Args:
        args (argparse.Namespace): Input arguments.
        start_date (float): Start time.
        num_types (int): Number of user types.

    Returns:
        bool: True if should end, False otherwise
    """    

    if args.use_time_mode:
        return time.time()-start_date>args.max_value 
    else:
        return num_types>args.max_value

def welcome(args):
    """Print welcome message.

    Args:
        args (argparse.Namespace): Input arguments.
    """    

    print(args.__dict__)
    print(Fore.RED + 'PSR' + Style.RESET_ALL + " Typing test, group 14, October 2021")
    print(f"Test running up to {args.max_value} {'seconds' if args.use_time_mode else 'inputs'}.")


def main():

    # Define argparse inputs
    parser = argparse.ArgumentParser(description='Definition of test mode')
    parser.add_argument('-utm','--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.', required=False)
    parser.add_argument('-mv','--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.', required=True)

    # Parse arguments
    args = parser.parse_args()

    # Generate lowerca ascii possibilities
    lowercase = string.ascii_lowercase

    # Initialize statistics
    statistics = {
        'inputs': [],
        'type_hit_average_duration': 0.0,
        'type_miss_average_duration': 0.0,
        'accuracy': 0.0
    }

    # Initialize durantios and counters
    hit_durations, miss_durations = [], []
    types, hits = 0, 0

    # Print welcome messages
    welcome(args)
    
    # Wait key press for game start
    print("Press any key to start the test")
    readchar.readkey()

    # Update starting time
    statistics['test_start'] = datetime.now().ctime()
    start_date = time.time()

    # Loop
    while not checkEndgame(args, start_date, types):
        next = random.choice(lowercase)
        print('Type letter ' + Fore.BLUE + next + Style.RESET_ALL)

        start_timer = time.time()
        char = readchar.readkey()
        type_duration = time.time()-start_timer

        if char==' ':
            break

        color = Fore.GREEN if next == char else Fore.RED 
        print('You typed letter ' + color + char + Style.RESET_ALL) 
    
        statistics['inputs'].append(Input(requested=next, received=char, duration=type_duration))

        types += 1
        if next==char:
            hits += 1
            hit_durations.append(type_duration)
        else:
            miss_durations.append(type_duration)

    # Update end statistics
    statistics['test_end'] =  datetime.now().ctime()
    statistics['test_duration'] = time.time()-start_date

    if types:
        statistics['type_average_duration'] = (sum(hit_durations)+sum(miss_durations))/types
        statistics['accuracy'] = hits/types
    
    if hit_durations:
        statistics['type_hit_average_duration'] = sum(hit_durations)/len(hit_durations)

    if miss_durations:
        statistics['type_miss_average_duration'] = sum(miss_durations)/len(miss_durations)
    
    statistics['number_of_hits'] = hits
    statistics['number_of_types'] = types

    # Print statistics
    pprint(statistics)

# Main
if __name__ == '__main__':
    main()