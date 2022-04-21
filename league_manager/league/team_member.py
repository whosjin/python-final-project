from league_manager.league.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is not None:
            self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email is not None:
            self._email = email

    def send_email(self, emailer, subject, message):
        emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        return f"{self.name}<{self.email}>"
