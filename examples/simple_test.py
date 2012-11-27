import argparse
import httplib2

import runner

def main():
    
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('--url', default='http://www.google.com')
    parser.add_argument('--debug', default=runner.TestRunner.options['debug'], action='store_true')
    parser.add_argument('--num_threads', default=runner.TestRunner.options['num_threads'], type=int)
    parser.add_argument('--out_file', default=runner.TestRunner.options['out_file'])
    parser.add_argument('--num_runs', default=runner.TestRunner.options['num_runs'], type=int)
    parser.add_argument('--start_delay', default=runner.TestRunner.options['start_delay'], type=int)
    parser.add_argument('--run_delay', default=runner.TestRunner.options['run_delay'], type=int)
    args = vars(parser.parse_args())
    
    args['test_class'] = SimpleTestTransaction
    
    runner.TestRunner(args)

class SimpleTestTransaction(object):
    def __init__(self, options):
        self.options = options
    
    def run(self):
        h = httplib2.Http()
        h.request(self.options['url'])
        
if __name__ == "__main__":
    main()