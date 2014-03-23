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
            return {"id": o.id, "name": o.name, "wins": o.wins,
                    "losses": o.losses}
        return o


class BattleshipsServer(object):

    """ A server for providing a dashboard to Battleships game. """

    def __init__(self, host, port, competition=None):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

        self.competition = competition
        if not self.competition:
            self.competition = Competition()

            # Have a default AI for people to play against
            self.competition.add("default-demo-ai", BattleshipsAI, name="Demo")

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

    def add_entry(self):
        """ Add an entry to the competition. """
        ai_id = request.forms.get("id")
        name = request.forms.get("name")
        code = request.files.get("filedata").file.read()
        exec(code, globals())
        self.competition.add(ai_id, BattleshipsAI, name=name)

if __name__ == "__main__":
    server = BattleshipsServer(host="localhost", port=8080)
    server.start()