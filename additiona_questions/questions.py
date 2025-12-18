from selenium.webdriver.common.by import By

from .checkbox import try_handle_checkbox
from .date_field import try_handle_date
from .dropdown import try_handle_dropdown
from .radio import try_handle_radio
from .text import try_handle_text


def questions(self, form):
    print("Trying to fill up additional questions")

    questions = form.find_elements(By.CLASS_NAME, 'fb-dash-form-element')
    for question in questions:
        ctx = {}
        if try_handle_radio(self, question):
            continue
        if try_handle_text(self, question, ctx):
            continue
        if try_handle_date(self, question):
            continue
        if try_handle_dropdown(self, question, ctx):
            continue
        try_handle_checkbox(self, question)


