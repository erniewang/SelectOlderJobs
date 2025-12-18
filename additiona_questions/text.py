from selenium.webdriver.common.by import By


def try_handle_text(self, question, ctx):
    # Questions check
    try:
        question_text = question.find_element(By.TAG_NAME, 'label').text.lower()
        print(question_text)  # TODO: Put logging behind debug flag

        txt_field_visible = False
        try:
            txt_field = question.find_element(By.TAG_NAME, 'input')
            txt_field_visible = True
        except:
            try:
                txt_field = question.find_element(By.TAG_NAME, 'textarea')  # TODO: Test textarea
                txt_field_visible = True
            except:
                raise Exception("Could not find textarea or input tag for question")

        if 'numeric' in txt_field.get_attribute('id').lower():
            # For decimal and integer response fields, the id contains 'numeric' while the type remains 'text'
            text_field_type = 'numeric'
        elif 'text' in txt_field.get_attribute('type').lower():
            text_field_type = 'text'
        else:
            raise Exception("Could not determine input type of input field!")

        # Persist into ctx immediately to mimic original single-scope behavior
        # (so later blocks in the same question iteration can "see" it if it was computed).
        ctx["text_field_type"] = text_field_type

        to_enter = ''
        if 'experience' in question_text or 'how many years in' in question_text:
            no_of_years = None
            for experience in self.experience:
                if experience.lower() in question_text:
                    no_of_years = int(self.experience[experience])
                    break
            if no_of_years is None:
                self.record_unprepared_question(text_field_type, question_text)
                no_of_years = int(self.experience_default)
            to_enter = no_of_years

        elif 'grade point average' in question_text:
            to_enter = self.university_gpa

        elif 'first name' in question_text:
            to_enter = self.personal_info['First Name']

        elif 'last name' in question_text:
            to_enter = self.personal_info['Last Name']

        elif 'name' in question_text:
            to_enter = self.personal_info['First Name'] + " " + self.personal_info['Last Name']

        elif 'pronouns' in question_text:
            to_enter = self.personal_info['Pronouns']

        elif 'phone' in question_text:
            to_enter = self.personal_info['Mobile Phone Number']

        elif 'linkedin' in question_text:
            to_enter = self.personal_info['Linkedin']

        elif 'message to hiring' in question_text or 'cover letter' in question_text:
            to_enter = self.personal_info['MessageToManager']

        elif 'website' in question_text or 'github' in question_text or 'portfolio' in question_text:
            to_enter = self.personal_info['Website']

        elif 'notice' in question_text or 'weeks' in question_text:
            if text_field_type == 'numeric':
                to_enter = int(self.notice_period)
            else:
                to_enter = str(self.notice_period)

        elif 'salary' in question_text or 'expectation' in question_text or 'compensation' in question_text or 'CTC' in question_text:
            if text_field_type == 'numeric':
                to_enter = int(self.salary_minimum)
            else:
                to_enter = float(self.salary_minimum)
            self.record_unprepared_question(text_field_type, question_text)

        # Since no response can be determined, we use AI to generate a response if available, falling back to 0 or empty string if the AI response is not available
        if text_field_type == 'numeric':
            if not isinstance(to_enter, (int, float)):
                ai_response = self.ai_response_generator.generate_response(
                    question_text,
                    response_type="numeric"
                )
                to_enter = ai_response if ai_response is not None else 0
        elif to_enter == '':
            ai_response = self.ai_response_generator.generate_response(
                question_text,
                response_type="text"
            )
            to_enter = ai_response if ai_response is not None else " ‏‏‎ "

        self.enter_text(txt_field, to_enter)
        return True
    except:
        print("An exception occurred while filling up text field")  # TODO: Put logging behind debug flag

    return False


