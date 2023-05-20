### A class to make print more beautiful. Can be added on to log the print to another file

import inspect,sys
from datetime import datetime

# Print Log'
class PrintHandler():
    def __init__(self):
        self.console = sys.stdout

    def write(self, log_string):
        W  = '\033[0m'  # white (normal)
        R  = '\033[31m' # red
        G  = '\033[32m' # green
        O  = '\033[33m' # orange
        B  = '\033[34m' # blue
        P  = '\033[35m' # purple
        GY = '\033[37m' #grey
        try:
            # print(inspect.stack()[1][0])
            the_class  = inspect.stack()[1][0].f_locals["self"].__class__.__name__
            the_method = inspect.stack()[1][0].f_code.co_name
        except:
            # the_class  = inspect.stack()[1][3].f_locals.__class__.__name__
            the_class  = inspect.stack()[1][1]
            the_method = inspect.stack()[1][3]
        # sub_category = inspect.stack()[1][3]
        if log_string != '\n':
            printcontent = (O+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" | "+G+the_class +"."+B+the_method +" "+P+"=> "+ W + log_string)
            self.console.write ('{}'.format(printcontent))
        else:
            self.console.write (log_string)

    def flush(self): # needed for file like object
        pass