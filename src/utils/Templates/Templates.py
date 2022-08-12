class Email():
    url = ""

    def __init__(self, url) -> None:
        self.url = url


class ActivateEmail(Email):
    def create_mail(self) -> str:
        with open('activate_email.html', 'r') as file:
            file_content = file.read()
            file_content.replace('{URL}', self.url)
        return file_content
    
class RecoverEmail(Email):
    def create_mail(self) -> str:
        with open('recover_email.html', 'r') as file:
            file_content = file.read()
            file_content.replace('{URL}', self.url)
        return file_content
