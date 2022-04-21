from src.league_manager.identified_object import IdentifiedObject


class Competition(IdentifiedObject):

    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams = teams
        self._location = location
        self._datetime = datetime

    @property
    def teams_competing(self):
        return self._teams

    @property
    def date_time(self):
        return self._datetime

    @date_time.setter
    def date_time(self, datetime):
        if datetime is not None:
            self._datetime = datetime

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if location is not None:
            self._location = location

    def send_email(self, emailer, subject, message):
        emails = []

        for team in self._teams:
            for member in team.members:
                if member.email not in emails and member.email is not None:
                    emails.append(member.email)

        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        string = f"Competition at {self._location} "
        if self._datetime is not None:
            string += f"on {self._datetime} "

        string += f"with {len(self._teams)} teams"
        return string

    # if __name__ == "__main__":
#     now = datetime.datetime.now()
#     t1 = Team(1, "Team 1")
#     t2 = Team(2, "Team 2")
#     t3 = Team(3, "Team 3")

#     tm1 = TeamMember(5, "f", "f@foo.com")
#     tm2 = TeamMember(6, "g", "g@bar.com")
#     tm3 = TeamMember(6, "a", "test@gmail.com")

#     t1.add_member(tm1)
#     t2.add_member(tm2)
#     t2.add_member(tm3)
#     t3.add_member(tm3)

#     c1 = Competition(1, [t1, t2], "Arena 1", None)
#     c2 = Competition(2, [t2, t3], "Arena 2", now)
#     c3 = Competition(2, [t1, t3], "Arena 3", now)

#     fe = FakeEmailer()

#     c3.send_email(fe, "test", "testing")

#     print(c1)
#     print(c2)
#     print(c3)
