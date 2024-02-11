import get_stock_data
from datetime import datetime
from global_var import *
current_date = datetime.now()

formatted_date = current_date.strftime('%Y%m%d')

if(train):
    start_date = train_start_date
    end_date   = train_end_date #str(formatted_date)
    file_name = "STOCK_TRAIN_DATA.csv"
else:
    start_date = test_start_date
    end_date   = str(formatted_date)
    file_name = "STOCK_TEST_DATA.csv"

