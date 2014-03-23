from unittest import TestCase
from ..game import AI
from ..competition import Competition


class TestCompetition(TestCase):
    def test_competition_can_add_entry(self):
        """ Test the competition can add an entry. """
        competition = Competition()

        competition.add("ai", AI)

        self.assertEquals(len(competition.entries), 1)

    def test_competition_runs_games(self):
        """ Test the competition runs games when entries are added. """
        competition = Competition(games_to_run=100)

        competition.add("ai1", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 0)

        competition.add("ai2", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 100)
        self.assertEquals(competition.entries["ai2"].total_games, 100)

        competition.add("ai3", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 200)
        self.assertEquals(competition.entries["ai2"].total_games, 200)
        self.assertEquals(competition.entries["ai2"].total_games, 200)

    def test_competition_replaces_entries(self):
        """ Test that reusing an ID replaces the entry. """
        competition = Competition(games_to_run=100)

        competition.add("ai1", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 0)

        competition.add("ai2", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 100)
        self.assertEquals(competition.entries["ai2"].total_games, 100)

        competition.add("ai2", AI)

        self.assertEquals(competition.entries["ai1"].total_games, 100)
        self.assertEquals(competition.entries["ai2"].total_games, 100)