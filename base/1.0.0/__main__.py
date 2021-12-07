"""   Starting point for running the program. """
# Import built-in modules
import os
from multiprocessing import Process

# Import third-party modules
import pretty_errors

# Import local modules
from StartASLM import start

if __name__ == '__main__':
    base_directory = os.path.dirname(os.path.abspath(__file__))
    verbose = True
    if verbose:
        print("The Base Directory is:", base_directory)

    # Start the monitor
    configuration_directory = os.path.join(base_directory, 'config')
    start(configuration_directory, 'configuration.yml', verbose)
    if verbose:
        print("Launching the StartMonitor")