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
import signal


# namedtuple definition
Input = namedtuple('Input', ['requested', 'received', 'duration'])


def raise_timeout(signum, frame):
    raise TimeoutError

# functions definition
def checkGameEnd(args, num_types):
    """ 
    Args:
        args (argparse.Namespace): Input arguments.
        num_types (int): Number of user types.

    Returns:
        bool: True if should end, False otherwise
    """    
    return not args.use_time_mode and num_types==args.max_value
        

def welcome(args):
    """ Print welcome messages.

    Args:
        args (argparse.Namespace): Input arguments.
    """

    pprint(vars(args))

    if args.max_value <= 0:
        print("Maximum Value must be positive.")
        exit(1)

    print(Fore.RED + 'PSR' + Style.RESET_ALL + " Typing test, group 14, October 2021")
    print(f"Test running up to {args.max_value} {'seconds' if args.use_time_mode else 'inputs'}.")

def computeStatistics(statistics, types, hits, hit_durations, miss_durations, start_date):
    
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

    return statistics


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
        'type_hit_average_duration': None,
        'type_miss_average_duration': None,
        'accuracy': 0.0
    }

    # Initialize durantios and counters
    hit_durations, miss_durations = [], []
    types, hits = 0, 0

    # Print welcome messages
    welcome(args)
    
    # Wait key press for game start
    print("Press any key to start the test")
    if str(readchar.readkey()) == ' ':
        print(Fore.RED + 'Test aborted!' + Style.RESET_ALL)
        exit(0)

    # Loop
    print_statistics = True

    # Update starting time
    statistics['test_start'] = datetime.now().ctime()
    start_date = time.time()

    # conditinal timeout
    if args.use_time_mode: # activate timer
        signal.signal(signal.SIGALRM, raise_timeout)
        signal.alarm(args.max_value)

    try:
        while not checkGameEnd(args, types):
            prompted = random.choice(lowercase)
            print('Type letter ' + Fore.BLUE + prompted + Style.RESET_ALL)

            start_timer = time.time()
            typed = readchar.readkey()
            type_duration = time.time()-start_timer

            if typed==' ':
                print_statistics = False
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

    except TimeoutError:
        pass


    # Update end statistics
    if print_statistics:
        statistics = computeStatistics(statistics, types, hits, hit_durations, miss_durations, start_date)   

        # Print end messages
        if args.use_time_mode and types==args.max_value:
            print(f"Current test duration ({statistics['test_duration']}) exceeded maximum of {args.max_value}")
        else:
            print(f"Current number of inputs ({statistics['number_of_types']}) reached")
        
        print(Fore.BLUE + 'Test finished!' + Style.RESET_ALL) 

        # Print statistics
        pprint(statistics)
    else:
        print(Fore.RED + 'Test aborted!' + Style.RESET_ALL)

# Main
if __name__ == '__main__':
    main()