""" Server for providing HTTP interface to Battleships game. """
import bottle
from bottle import Bottle, static_file, request
from bottle import mako_template as template
from demo import BattleshipsAI
import json

# Set up templates
bottle.TEMPLATE_PATH.insert(0, 'server/views')

from competition import Competition, Entry


class EntryEncoder(json.JSONEncoder):

    """ JSON Encoder that knows how to encode Entries. """

    def default(self, o):
        if isinstance(o, Entry):
            return {"id": o.id, "name": o.id, "wins": o.wins,
                    "losses": o.losses}
        return o



num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
            11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
            15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
            19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
            50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
            90: 'Ninety', 0: 'Zero'}

def n2w(n):
    """ Convert a number to the word representation. """
    try:
        return num2words[n]
    except KeyError:
        return num2words[n-n%10] + num2words[n%10].lower()

class BattleshipsServer(object):

    """ A server for providing a dashboard to Battleships game. """

    def __init__(self, host, port, competition=None):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

        self.competition = competition
        if not self.competition:
            self.competition = Competition(games_to_run=100)

            # Have a default AI for people to play against
            self.competition.add("Internal Demo", BattleshipsAI)

    def _route(self):
        """ Set up bottle routes for the app. """
        self._app.route('/', method="GET", callback=self.index)
        self._app.route('/entries', method="GET", callback=self.entries)
        self._app.route('/enter', method="POST", callback=self.add_entry)
        self._app.route('/static/bower_components/<filepath:path>',
                        callback=self.serve_bower)
        self._app.route('/static/<filepath:path>', callback=self.serve_static)

    def start(self):
        """ Start the bottle server. """
        self._app.run(host=self._host, port=self._port)

    def serve_bower(self, filepath):
        """ Serve bower components. """
        return static_file(filepath, root='server/bower_components')

    def serve_static(self, filepath):
        """ Server /static files. """
        return static_file(filepath, root='server/static')

    def index(self):
        """ The game dashboard. """
        return template('index')

    def entries(self):
        """ Dump all entries as json. """
        return json.dumps(self.competition.entries.values(), cls=EntryEncoder)

    def add_entry(self, code=None, forms=None):
        """ Add an entry to the competition. """
        if code is None:
            code = request.files.get("filedata").file.read()
        if forms is None:
            forms = request.forms
        exec(code, globals())
        team_name = BattleshipsAI.TEAM_NAME
        if team_name in self.competition.entries and\
                not forms.get('replace') == "1":
            increment = 1
            while team_name + " " + n2w(increment) in self.competition.entries:
                increment += 1
            team_name = team_name + " " + n2w(increment)
        self.competition.add(team_name, BattleshipsAI)

if __name__ == "__main__":
    server = BattleshipsServer(host="localhost", port=8080)
    server.start()