from unittest import TestCase
from ..server import BattleshipsServer
from ..competition import Competition
from ..game import AI
import json


class TestServer(TestCase):
    def test_server_returns_index_view(self):
        """ Test that the index view is rendered. """
        competition = Competition(threaded=False)
        server = BattleshipsServer("localhost", 8080, competition=competition)
        self.assertTrue("<h1>Battleships</h1>" in server.index())

    def test_server_dumps_entries(self):
        """ Test that the current entries are dumped. """
        competition = Competition(threaded=False)
        server = BattleshipsServer("localhost", 8080, competition=competition)
        entries = json.loads(server.entries())
        self.assertEquals(entries, [])
        competition.add("ai1", AI)
        entries = json.loads(server.entries())
        self.assertEquals(len(entries), 1)
        self.assertEquals(entries[0]["wins"] + entries[0]["losses"], 0)
        competition.add("ai2", AI)
        entries = json.loads(server.entries())
        self.assertEquals(len(entries), 2)
        self.assertIsNot(entries[0]["wins"] + entries[0]["losses"], 0)

    def test_server_adds_entries(self):
        """ Test that the server can add an uploaded entry. """
        competition = Competition(threaded=False)
        server = BattleshipsServer("localhost", 8080, competition=competition)
        server.add_entry(code="""
from game import AI

class BattleshipsAI(AI):
    TEAM_NAME = "Test AI"
""", forms={})
        self.assertEquals(competition.entries["Test AI"].id, "Test AI")

        # Test the incrementing names
        server.add_entry(code="""
from game import AI

class BattleshipsAI(AI):
    TEAM_NAME = "Test AI"
""", forms={})
        self.assertEquals(competition.entries["Test AI 1"].id, "Test AI 1")

        # Test replacing names
        server.add_entry(code="""
from game import AI

class BattleshipsAI(AI):
    TEAM_NAME = "Test AI"
""", forms={"replace": "1"})
        self.assertEquals(len(competition.entries), 2)