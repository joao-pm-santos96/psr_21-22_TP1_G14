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
import sys

"""
NamedTuple definition
"""
Input = namedtuple('Input', ['requested', 'received', 'duration'])

"""
Functions definition
"""
def check_game_end(args, start_date, num_types):
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
        return num_types==args.max_value

def welcome(args):
    """Print welcome message.

    Args:
        args (argparse.Namespace): Input arguments.
    """

    # Inverts the display of arguments to be the same as in the example
    argr = args.__dict__.copy()
    argr1 = argr.popitem()
    argr2 = argr.popitem()
    argr = dict([argr1, argr2])
    print(argr)

    if args.__dict__['max_value']<=0:
        print("The Maximum Value must be positive value")
        sys.exit()

    print(Fore.RED + 'PSR' + Style.RESET_ALL + " Typing test, group 14, October 2021")
    print(f"Test running up to {args.max_value} {'seconds' if args.use_time_mode else 'inputs'}.")


def main():

    # Define argparse inputs
    parser = argparse.ArgumentParser(description='Definition of test mode')
    parser.add_argument('-utm','--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.', required=False)
    parser.add_argument('-mv','--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.', required=True)

    # Parse arguments
    args = parser.parse_args()

    # Generate lowercase ascii possibilities
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
    while not check_game_end(args, start_date, types):
        prompted = random.choice(lowercase)
        print('Type letter ' + Fore.BLUE + prompted + Style.RESET_ALL)

        start_timer = time.time()
        typed = readchar.readkey()
        type_duration = time.time()-start_timer

        if typed==' ':
            break

        color = Fore.GREEN if prompted == typed else Fore.RED 
        print('You typed letter ' + color + typed + Style.RESET_ALL) 
    
        statistics['inputs'].append(Input(requested=prompted, received=typed, duration=type_duration))

        types += 1
        if prompted==typed:
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

    # Print end messages
    if args.use_time_mode and statistics['test_duration']>args.max_value:
        print(f"Current test duration ({statistics['test_duration']}) exceeds maximum of {args.max_value}")
    elif types==args.max_value:
        print(f"Current number of inputs ({statistics['number_of_types']}) reaches maximum of {args.max_value}")
    
    print(Fore.BLUE + 'Test finished!' + Style.RESET_ALL) 

    # Print statistics
    pprint(statistics)

# Main
if __name__ == '__main__':
    main()