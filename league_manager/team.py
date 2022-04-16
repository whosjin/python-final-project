from exceptions import DuplicateOid, DuplicateEmail
from identified_object import IdentifiedObject


class Team(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._members = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is not None:
            self._name = name

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        if member in self._members:
            raise DuplicateOid("Duplicate OID", member.oid)

        for mem in self._members:
            if member.email == mem.email:
                raise DuplicateEmail("Duplicate Email", member.email)

        if member not in self._members and member is not None:
            self._members.append(member)

    def member_named(self, s):
        for member in self._members:
            if s == member.name:
                return member
        return None

    def remove_member(self, member):
        for mem in self._members:
            if member == mem:
                self._members.remove(member)

    def send_email(self, emailer, subject, message):
        emails = [member.email for member in self._members if member.email is not None]
        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        return f"{self.name}: {len(self._members)} members"
