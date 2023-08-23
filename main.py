import sys
import os
import csv
import random
from datetime import datetime

class ascrape:
    """Overall class for running a scraping job, parsing it, etc."""

    cache_settings = None
    charles = None
    config = None
    history = None
    http_tools = None
    log_id = None
    manifest = None
    script = None
    settings = None
    progress_file = "completed_line_items.csv"
    
    def __init__(self):
        """Constructor"""
        self.pid = str(os.getpid())

    def read_csv_file(self, file_name):
        with open('employee_data1.csv') as csvfile:
            csv_reader = csv.reader(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f"Columns are {', '.join(row)}")
                    line_count += 1
                else:
                    print(f"\t{row[0]} works in the {row[1]} department, and was born in {row[2]} and lives in {row[3]}.")
                    line_count += 1
            print(f"Processed {line_count} lines")    
        

if __name__ == "__main__":
    # Make an instance and run it
    # ascrape = None
    script_start = datetime.now()
    print(f'Running Time: {script_start}')
    try:
        # Put the file name
        flname = 'employee_data1.csv'
        ascrape = ascrape()
        ascrape.read_csv_file(flname)
        
    except Exception as error:
        # print stack trace
        print(f'Exception: {error}')
        sys.exit(1)  # tell os that the job did not complete successfully    
