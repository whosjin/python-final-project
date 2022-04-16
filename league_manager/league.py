# from competition import Competition
from league_manager.identified_object import IdentifiedObject
from league_manager.exceptions import DuplicateOid
# from team import Team
# from team_member import TeamMember


class League(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self._league_name = name
        self._teams = []
        self._competitions = []

    @property
    def name(self):
        return self._league_name

    @name.setter
    def name(self, name):
        if name is not None:
            self._league_name = name

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        if team in self._teams:
            raise DuplicateOid("Duplicate OID", team.oid)
        if team not in self._teams and team is not None:
            self._teams.append(team)

    def remove_team(self, team):
        for comp in self._competitions:
            if team in comp.teams_competing:
                raise ValueError("Cannot remove team, team is part of competition")

        if team in self._teams:
            self._teams.remove(team)

    def team_named(self, s):
        for team in self._teams:
            if s == team.name:
                return team
        return None

    def add_competition(self, competition):
        if competition in self._competitions:
            raise DuplicateOid("Duplicate OID", competition.oid)

        for team in competition.teams_competing:
            if team not in self._teams:
                raise ValueError("One or more team is not part of the league")

        self._competitions.append(competition)

    def teams_for_member(self, member):
        return [team for team in self._teams if member in team.members]

    def competitions_for_team(self, team):
        return [competition for competition in self._competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        comp = []

        for competition in self._competitions:
            for team in competition.teams_competing:
                if member in team.members:
                    comp.append(competition)

        return comp

    def __str__(self):
        return f"{self._league_name}: {len(self._teams)} teams, {len(self._competitions)} competitions"


# if __name__ == "__main__":
#     league = League(1, "Some league")
#     t1 = Team(1, "t1")
#     t2 = Team(2, "t2")
#     t3 = Team(3, "t3")
#     t4 = Team(5, "t4")
#     all_teams = [t1, t2, t3, t4]
#     league.add_team(t1)
#     league.add_team(t2)
#     league.add_team(t3)
#     # league.add_team(t4)
#     tm1 = TeamMember(1, "Fred", "fred")
#     tm2 = TeamMember(2, "Barney", "barney")
#     tm3 = TeamMember(3, "Wilma", "wilma")
#     tm4 = TeamMember(4, "Betty", "betty")
#     tm5 = TeamMember(5, "Pebbles", "pebbles")
#     tm6 = TeamMember(6, "Bamm-Bamm", "bam-bam")
#     tm7 = TeamMember(7, "Dino", "dino")
#     tm8 = TeamMember(8, "Mr. Slate", "mrslate")
#     t1.add_member(tm1)
#     t1.add_member(tm2)
#     t2.add_member(tm3)
#     t2.add_member(tm4)
#     t2.add_member(tm5)
#     t3.add_member(tm6)
#     t3.add_member(tm7)
#     t3.add_member(tm8)

    # c1 = Competition(2, [t1, t2], "Arena", "10/20/22")
    # league.add_competition(c1)
    # c2 = Competition(1, [t1, t4], "Arena", "10/20/22")
    # league.add_competition(c2)

    # oid = 1
    #
    # for c in [Competition(oid := oid + 1, [team1, team2], team1.name + " vs " + team2.name, None)
    #           for team1 in all_teams
    #           for team2 in all_teams
    #           if team1 != team2]:
    #     league.add_competition(c)
    #     # league.add_competition(c)
    #
    # t = league.teams[0]
    # # league.remove_team(t4)
    # cs = league.competitions_for_team(t)
    # cs_names = {c.location for c in cs}
    #
    # print(cs_names)
