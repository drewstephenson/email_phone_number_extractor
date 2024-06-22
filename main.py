import re
import pyperclip


class Extractor:
    """A class for extracting emails and phone numbers from your clipboard."""
    def __init__(self):
        """Initializes the Extractor class attributes."""
        self.text = str(pyperclip.paste())  # Get the text from the clipboard and convert it to a string

        # Define the phone pattern using re.VERBOSE
        self.phone_pattern = re.compile(r'''(
            (\d{3}|\(\d{3}\))?   # area code with or without parentheses, optional
            (\s|-|\.)?    # separator such as a space, hyphen, or period, optional
            (\d{3})    # first 3 digits
            (\s|-|\.)  # separator
            (\d{4})  # last 4 digits
            (\s*(ext|x|ext.)\s*(\d{2,5}))?   # extension, optional
        )''', re.VERBOSE)

        # Define the email pattern also using re.VERBOSE
        self.email_pattern = re.compile(r'''(
            [a-zA-Z0-9._%+-]+   # username containing letters, numbers, and some special characters (._%+-)
            @   # @ symbol
            [a-zA-Z0-9.-]+    # domain containing letters, numbers, and special characters (-.)
            (\.[a-zA-Z]{2,4})   # dot something, must be 2 to 4 characters long
        )''', re.VERBOSE)

        self.matches = []  # empty list to store phone numbers and emails

    def extract_emails(self):
        """Extract emails from text."""
        emails = self.email_pattern.findall(self.text)
        for group in emails:
            self.matches.append(group[0])  # add the email to the matches list

    def extract_numbers(self):
        """Extract phone numbers from text."""
        numbers = self.phone_pattern.findall(self.text)
        for group in numbers:
            if group[1]:  # if there is an area code
                phone_number = '-'.join([group[1], group[3], group[5]])
            else:
                phone_number = '-'.join([group[3], group[5]])
            if group[8] != '':  # if there is an extension
                phone_number += ' x' + group[8]
            self.matches.append(phone_number)  # add the formatted phone number

    def extract(self):
        """Extract emails and phone numbers from text."""
        # Call the extracting methods
        self.extract_emails()
        self.extract_numbers()

        # Copy the extracted emails and phone numbers to the clipboard
        if len(self.matches) > 0:
            pyperclip.copy('\n'.join(self.matches))  # join the emails and phone numbers with a newline character
            print('Emails and phone numbers have been copied to the clipboard.')
            print('\n'.join(self.matches))
        else:
            print('No emails or phone numbers found.')


if __name__ == '__main__':
    extractor = Extractor()
    extractor.extract()
