from selenium.webdriver.common.by import By

from additiona_questions.checkbox import try_handle_checkbox
from additiona_questions.date_field import try_handle_date
from additiona_questions.dropdown import try_handle_dropdown
from additiona_questions.radio import try_handle_radio
from additiona_questions.text import try_handle_text


def questions(self, form):
    print("Trying to fill up additional questions")

    questions = form.find_elements(By.CLASS_NAME, 'fb-dash-form-element')
    for question in questions:
        ctx = {}
        if try_handle_radio(self, question):
            continue
        elif try_handle_text(self, question, ctx):
            continue
        elif try_handle_date(self, question):
            continue
        elif try_handle_dropdown(self, question, ctx):
            continue
        try_handle_checkbox(self, question)


