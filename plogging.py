"""
A simple performance logging/output class for load tests.

"""
import csv
import threading
import time

class Log(object):
    
    debug_flag = False
    
    def __init__(self, debug_flag):
        self.debug_flag = debug_flag
        self.performance_logs = []
        
    def debug(self, text):
        """
        Debug output.
        
        """
        if self.debug_flag is True:
            t = threading.current_thread()
            print '{0}[DEBUG]{1} -- {2} '.format(time.strftime('%d-%m-%y %H:%M:%S'), t.name, text)
            
    def perflog(self, tuple):
        """
        Record a performance log.
        
        """
        self.performance_logs.append(tuple)
        
    def perfcsv(self, file, headers):
        """
        Write performance logs to csv.
        
        """
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        for tuple in self.performance_logs:
            writer.writerow(tuple)
