"""
Simple harness for running load tests.

"""
import atexit
import os
import threading
import time
import traceback

import plogging

class TestRunner(object):
    
    # Defaults
    options = {
        
        # Debugging output
        'debug' : False,

        # Number of threads. Each thread simulates an individual agent.
        'num_threads' : 1,
        
        # Results CSV
        'out_file' : None,
        
        # Number of test repeats PER thread.
        'num_runs' : 1,
        
        # Delay between starting multiple threads (seconds).
        'start_delay' : 0,

        # Delay between each run in a thread (seconds).
        'run_delay' : 0,

        # Test class is initialsied with test runner options. Must implement a run() method.
        'test_class' : None
    }
    
    def __init__(self, config={}):
        self.options.update(config)
        if 'log' not in self.options.keys():
            self.options['log'] = plogging.Log(self.options['debug'])
        atexit.register(self.on_exit)
        self.run()
    
    def run(self):
        """
        Run the test process.
        
        """
        options = self.options
        
        threads = []
        i = 0
        while i < options['num_threads']:
            # Create and initialise tests in serial to allow them all to be commenced at the same time
            test = TestThread(options)
            threads.append(test)
            i = i + 1
            
        for thread in threads:
            # Start all tests
            if options['start_delay'] > 0:
                # Delay between tests
                time.sleep(options['start_delay'])
            thread.start()
            options['log'].debug('Spawned Thread')
    
    def on_exit(self):
        """
        Generate CSV when all test threads have finished.
        
        """
        options = self.options
        options['log'].debug('Finished All Requests')
        out_csv = options['out_file'] or \
                'results/{0}_{1}_run_{2}_threads_{3}s_sdelay_{4}s_rdelay.csv'.format(options['test_class'].__name__, options['num_runs'], options['num_threads'], options['start_delay'], options['run_delay'])
        options['log'].perfcsv(open(out_csv, 'wb+'), ['System Time', 'Elapsed Run Time'])
    

class TestThread(threading.Thread):
    """
    A Test thread.
    
    """
    def __init__(self, options):
        """
        Setup the test.
        
        """
        super(TestThread, self).__init__()
        self.options = options
        self.log = options['log']
        self.timers = {}
        self.transaction = options['test_class'](options)
        
    def run(self):
        """
        Run the test (possibly multiple times).
        
        """
        options = self.options
        i = 0
        for i in range(0, options['num_runs']):
            start_timer = time.time()
            start_time = time.strftime('%d-%m-%y %H:%M:%S')
            try:    
                self.transaction.run()
                if hasattr(self.transaction, 'latency'):
                    self.log.perflog((start_time, time.time() - start_timer, self.transaction.latency))
                else:
                    self.log.perflog((start_time, time.time() - start_timer))
                if options['run_delay'] > 0:
                    self.log.debug('Delaying run....')
                    time.sleep(options['run_delay'])
            except:
                self.log.debug('Error Running Transaction')    
                traceback.print_exc()
                self.log.perflog((-1, -1, -1))