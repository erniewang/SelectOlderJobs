from pathlib import Path

import yaml
from selenium.webdriver.common.by import By

with open(Path(__file__).resolve().parent / 'alias.yaml', 'r', encoding='utf-8') as file:
    alias_data = yaml.safe_load(file) or {}


def resolve_keyword(text: str):
    """
    Returns the first matching canonical key from alias.yaml by substring match.
    """
    if not text:
        return None
    t = str(text).lower()
    for alias, canonical in alias_data.items():
        if str(alias).lower() in t:
            return canonical
    return None

def try_handle_radio(self, question):
    try:
        # Radio check
        radio_fieldset = question.find_element(By.TAG_NAME, 'fieldset')
        question_span = radio_fieldset.find_element(By.CLASS_NAME, 'fb-dash-form-element__label').find_elements(By.TAG_NAME, 'span')[0]
        radio_text = question_span.text.lower()
        print(f"Radio question text: {radio_text}")

        radio_labels = radio_fieldset.find_elements(By.TAG_NAME, 'label')
        radio_options = [(i, text.text.lower()) for i, text in enumerate(radio_labels)]
        print(f"radio options: {[opt[1] for opt in radio_options]}")

        if len(radio_options) == 0:
            raise Exception("No radio options found in question")

        answer = None

        # NEW EDIT: resolve via alias.yaml
        keyword = resolve_keyword(radio_text)
        if keyword == "__eeo_decline__":
            negative_keywords = ['prefer', 'decline', "don't", 'specified', 'none', 'no']
            choice = next(
                (
                    opt_text
                    for _, opt_text in radio_options
                    if any(neg in opt_text.lower() for neg in negative_keywords)
                ),
                None
            )
            answer = choice
        elif keyword == "__education_level__":
            for degree in self.checkboxes['degreeCompleted']:
                if degree.lower() in radio_text:
                    answer = "yes"
                    break
        elif keyword == "__experience__":
            if self.experience_default > 0:
                answer = 'yes'
            else:
                for experience in self.experience:
                    if experience.lower() in radio_text:
                        answer = "yes"
                        break
        elif keyword is not None:
            answer = self.get_answer(keyword)

        to_select = None
        if answer is not None:
            print(f"Choosing answer: {answer}")
            i = 0
            for radio in radio_labels:
                if answer in radio.text.lower():
                    to_select = radio_labels[i]
                    break
                i += 1
            if to_select is None:
                print("Answer not found in radio options")

        if to_select is None:
            print("No answer determined")
            self.record_unprepared_question("radio", radio_text)

            # Since no response can be determined, we use AI to identify the best responseif available, falling back to the final option if the AI response is not available
            ai_response = self.ai_response_generator.generate_response(
                radio_text,
                response_type="choice",
                options=radio_options
            )
            if ai_response is not None:
                to_select = radio_labels[ai_response]
            else:
                to_select = radio_labels[len(radio_labels) - 1]
        to_select.click()

        if radio_labels:
            return True
    except Exception as e:
        print("An exception occurred while filling up radio field")

    return False


