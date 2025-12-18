import time
from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def try_handle_date(self, question):
    # Date Check
    try:
        date_picker = question.find_element(By.CLASS_NAME, 'artdeco-datepicker__input ')
        date_picker.clear()
        date_picker.send_keys(date.today().strftime("%m/%d/%y"))
        time.sleep(3)
        date_picker.send_keys(Keys.RETURN)
        time.sleep(2)
        return True
    except:
        print("An exception occurred while filling up date picker field")  # TODO: Put logging behind debug flag

    return False


