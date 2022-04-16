import yagmail


class Emailer:
    _sender_address = None
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls._sender_address = sender_address

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        for recipient in recipients:
            yagmail.SMTP(self._sender_address).send(recipient, subject, message)
            print(f"Sending mail to: {recipient}")


# if __name__ == "__main__":
#     email1 = Emailer().instance()
#     email1.configure("orange.mango0422@gmail.com")
#     email_addresses = ['orange.mango0422@gmail.com', 'jin.hu.0422@gmail.com']
#     email1.send_plain_email(email_addresses, 'different subject', "does it work")

