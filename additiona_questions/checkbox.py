from selenium.webdriver.common.by import By


def try_handle_checkbox(self, question):
    # Checkbox check for agreeing to terms and service
    try:
        clickable_checkbox = question.find_element(By.TAG_NAME, 'label')
        clickable_checkbox.click()
    except:
        print("An exception occurred while filling up checkbox field")  # TODO: Put logging behind debug flag


