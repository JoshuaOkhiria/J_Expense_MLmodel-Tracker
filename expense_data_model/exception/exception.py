import sys
from expense_data_model.logging import logger

class ExpenseDataModelException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occoured in python script name [{0}] line number [{1}] with error message [{2}]".format(
            self.filename, self.lineno, str(self.error_message)
        )
    

if __name__ == "__main__":
    try:
        logger.logging.info("About to execute a code... Tracking details")
        a = 1/1
        print(a)
        logger.logging.info("successfully exceuted code")
    except Exception as e:
        raise ExpenseDataModelException(e, sys)