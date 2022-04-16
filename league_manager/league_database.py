import csv
import os.path
import pickle

from team import Team
from team_member import TeamMember


class LeagueDatabase:
    _sole_instance = None

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @property
    def leagues(self):
        return self._leagues

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as file:
                cls._sole_instance = pickle.load(file)
                return cls._sole_instance
        except FileNotFoundError:
            print("ugh, sorry, it would be better to use the logging framework here but I don't want to go into it")
            try:
                with open(file_name + ".backup", mode="rb") as file:
                    cls._sole_instance = pickle.load(file)
                    return cls._sole_instance
            except FileNotFoundError:
                cls._sole_instance = LeagueDatabase()
                return cls._sole_instance

    def add_league(self, league):
        self._leagues.append(league)

    def remove_league(self, league):
        if league in self._leagues:
            self._leagues.remove(league)

    def league_named(self, name):
        for league in self._leagues:
            if name == league.name:
                return league
        return None

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        if os.path.exists(file_name):
            os.rename(file_name, file_name + ".backup")

        with open(file_name, mode="wb") as file:
            pickle.dump(self, file)

    def import_league_teams(self, league, file_name):
        if not self.league_named(league.name):
            print("League does not exist")
            return None

        try:
            with open(file_name, mode="r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                header = next(csv_reader)
                for row in csv_reader:
                    team_name = row[0]
                    member_name = row[1]
                    member_email = row[2]

                    if not league.team_named(team_name):
                        team = Team(self.next_oid(), team_name)
                        league.add_team(team)
                        print("\nTeam:", team_name, "added to League:", league.name)

                    if not team.member_named(member_name):
                        team_member = TeamMember(self.next_oid(), member_name, member_email)
                        team.add_member(team_member)
                        print(member_name, " added to ", team_name)
                    else:
                        print(f"Member {member_name} already added to team {team_name}")
        except FileNotFoundError:
            print("Error importing league team csv file")

    def export_league_teams(self, league, file_name):
        if not self.league_named(league.name):
            print("League does not exist")
            return None

        header = ["Team name", "Member name", "Member email"]
        with open(file_name, mode="w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(header)

            for team in league.teams:
                for member in team.members:
                    csv_writer.writerow([team.name, member.name, member.email])
            print(f"\nLeague exported into {file_name}")


# if __name__ == '__main__':
#     lg = League(1, "test1")
#     # lg2 = League(2, "test2")
#
#     # from league_database import LeagueDatabase
#     db = LeagueDatabase.instance()
#     db.add_league(lg)
#     # db.save("test_file")
#     #
#     # db.add_league(lg2)
#     # print(len(db.leagues))
#     # LeagueDatabase.load("test_file")
#     # print(len(LeagueDatabase.instance().leagues))
#     db.import_league_teams(lg, "Teams.csv")
#     db.export_league_teams(lg, "export.csv")
