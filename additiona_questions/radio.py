from selenium.webdriver.common.by import By
import yaml

with open('alias.yaml', 'r') as file:
    alias_data = yaml.safe_load(file)

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

        # Try to determine answer using existing logic
        if 'driver\'s licence' in radio_text or 'driver\'s license' in radio_text:
            answer = self.get_answer('driversLicence')
        elif any(keyword in radio_text.lower() for keyword in
                 [
                     'Aboriginal', 'native', 'indigenous', 'tribe', 'first nations',
                     'native american', 'native hawaiian', 'inuit', 'metis', 'maori',
                     'aborigine', 'ancestral', 'native peoples', 'original people',
                     'first people', 'gender', 'race', 'disability', 'latino', 'torres',
                     'do you identify'
                 ]):
            negative_keywords = ['prefer', 'decline', 'don\'t', 'specified', 'none', 'no']
            answer = next((option for option in radio_options if
                           any(neg_keyword in option[1].lower() for neg_keyword in negative_keywords)), None)

        elif 'assessment' in radio_text:
            answer = self.get_answer("assessment")

        elif 'clearance' in radio_text:
            answer = self.get_answer("securityClearance")

        elif 'north korea' in radio_text:
            answer = self.get_answer('northKorea')

        elif 'previously employ' in radio_text or 'previous employ' in radio_text:
            answer = self.get_answer('previouslyEmployed')

        elif 'authorized' in radio_text or 'authorised' in radio_text or 'legally' in radio_text:
            answer = self.get_answer('legallyAuthorized')

        elif any(keyword in radio_text.lower() for keyword in
                 ['certified', 'certificate', 'cpa', 'chartered accountant', 'qualification']):
            answer = self.get_answer('certifiedProfessional')

        elif 'urgent' in radio_text:
            answer = self.get_answer('urgentFill')

        elif 'commut' in radio_text or 'on-site' in radio_text or 'hybrid' in radio_text or 'onsite' in radio_text:
            answer = self.get_answer('commute')

        elif 'remote' in radio_text:
            answer = self.get_answer('remote')

        elif 'background check' in radio_text:
            answer = self.get_answer('backgroundCheck')

        elif 'drug test' in radio_text:
            answer = self.get_answer('drugTest')

        elif 'currently living' in radio_text or 'currently reside' in radio_text or 'right to live' in radio_text:
            answer = self.get_answer('residency')

        elif 'level of education' in radio_text:
            for degree in self.checkboxes['degreeCompleted']:
                if degree.lower() in radio_text:
                    answer = "yes"
                    break

        elif 'experience' in radio_text:
            if self.experience_default > 0:
                answer = 'yes'
            else:
                for experience in self.experience:
                    if experience.lower() in radio_text:
                        answer = "yes"
                        break

        elif 'data retention' in radio_text:
            answer = self.get_answer('dataRetention')

        elif 'sponsor' in radio_text:
            answer = self.get_answer('requireVisa')

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


