from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def try_handle_dropdown(self, question, ctx):
    # Dropdown check
    try:
        question_text = question.find_element(By.TAG_NAME, 'label').text.lower()
        print(f"Dropdown question text: {question_text}")  # TODO: Put logging behind debug flag
        dropdown_field = question.find_element(By.TAG_NAME, 'select')

        select = Select(dropdown_field)
        options = [options.text for options in select.options]
        print(f"Dropdown options: {options}")  # TODO: Put logging behind debug flag

        if 'proficiency' in question_text:
            proficiency = "None"
            for language in self.languages:
                if language.lower() in question_text:
                    proficiency = self.languages[language]
                    break
            self.select_dropdown(dropdown_field, proficiency)

        elif 'clearance' in question_text:
            answer = self.get_answer('securityClearance')

            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                # Preserve original behavior: `text_field_type` may or may not exist depending
                # on how far the text-field block got before failing.
                if "text_field_type" in ctx:
                    text_field_type = ctx["text_field_type"]
                    self.record_unprepared_question(text_field_type, question_text)
                else:
                    # Intentionally reference an undefined name to mirror the original NameError path.
                    self.record_unprepared_question(text_field_type, question_text)
            self.select_dropdown(dropdown_field, choice)

        elif 'assessment' in question_text:
            answer = self.get_answer('assessment')
            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            # if choice == "":
            #    choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'commut' in question_text or 'on-site' in question_text or 'hybrid' in question_text or 'onsite' in question_text:
            answer = self.get_answer('commute')

            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            # if choice == "":
            #    choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'country code' in question_text:
            self.select_dropdown(dropdown_field, self.personal_info['Phone Country Code'])

        elif 'north korea' in question_text:
            answer = self.get_answer('northKorea')
            choice = next((opt for opt in options if answer in opt.lower()), "")
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'previously employed' in question_text or 'previous employment' in question_text:
            answer = self.get_answer('previouslyEmployed')
            choice = next((opt for opt in options if answer in opt.lower()), "")
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'sponsor' in question_text:
            answer = self.get_answer('requireVisa')
            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'above 18' in question_text.lower():  # Check for "above 18" in the question text
            answer = self.get_answer('above18')
            choice = next((opt for opt in options if answer in opt.lower()), "")
            if choice == "":
                choice = options[0]
            self.select_dropdown(dropdown_field, choice)

        elif 'currently living' in question_text or 'currently reside' in question_text:
            answer = self.get_answer('residency')
            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'authorized' in question_text or 'authorised' in question_text:
            answer = self.get_answer('legallyAuthorized')
            choice = ""
            for option in options:
                if answer == 'yes':
                    # find some common words
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'citizenship' in question_text:
            answer = self.get_answer('legallyAuthorized')
            choice = ""
            for option in options:
                if answer == 'yes':
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        elif 'clearance' in question_text:
            answer = self.get_answer('clearance')
            choice = ""
            for option in options:
                if answer == 'yes':
                    choice = option
                else:
                    if 'no' in option.lower():
                        choice = option
            if choice == "":
                choice = options[len(options) - 1]

            self.select_dropdown(dropdown_field, choice)

        elif any(keyword in question_text.lower() for keyword in
                 [
                     'aboriginal', 'native', 'indigenous', 'tribe', 'first nations',
                     'native american', 'native hawaiian', 'inuit', 'metis', 'maori',
                     'aborigine', 'ancestral', 'native peoples', 'original people',
                     'first people', 'gender', 'race', 'disability', 'latino'
                 ]):
            negative_keywords = ['prefer', 'decline', 'don\'t', 'specified', 'none']

            choice = next(
                (
                    option
                    for option in options
                    if any(neg_keyword in option.lower() for neg_keyword in negative_keywords)
                ),
                None
            )
            if not choice:
                self.record_unprepared_question("dropdown", question_text)
                choice = options[len(options) - 1]

            self.select_dropdown(dropdown_field, choice)

        elif 'email' in question_text:
            return True  # assume email address is filled in properly by default

        elif 'experience' in question_text or 'understanding' in question_text or 'familiar' in question_text or 'comfortable' in question_text or 'able to' in question_text:
            answer = 'no'
            if self.experience_default > 0:
                answer = 'yes'
            else:
                for experience in self.experience:
                    if experience.lower() in question_text and self.experience[experience] > 0:
                        answer = 'yes'
                        break
            if answer == 'no':
                # record unlisted experience as unprepared questions
                self.record_unprepared_question("dropdown", question_text)

            choice = ""
            for option in options:
                if answer in option.lower():
                    choice = option
            if choice == "":
                choice = options[len(options) - 1]
            self.select_dropdown(dropdown_field, choice)

        else:
            print(f"Unhandled dropdown question: {question_text}")
            self.record_unprepared_question("dropdown", question_text)

            # Since no response can be determined, we use AI to identify the best responseif available, falling back "yes" or the final response if the AI response is not available
            choice = options[len(options) - 1]
            choices = [(i, option) for i, option in enumerate(options)]
            ai_response = self.ai_response_generator.generate_response(
                question_text,
                response_type="choice",
                options=choices
            )
            if ai_response is not None:
                choice = options[ai_response]
            else:
                choice = ""
                for option in options:
                    if 'yes' in option.lower():
                        choice = option

            print(f"Selected option: {choice}")
            self.select_dropdown(dropdown_field, choice)
        return True
    except:
        print("An exception occurred while filling up dropdown field")  # TODO: Put logging behind debug flag

    return False


