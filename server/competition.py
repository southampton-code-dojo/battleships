""" Battleships competition with multiple entries. """
from game import GameRunner, Player
from Queue import Queue
from threading import Thread


class Entry(object):
    """ Represents an entry in the competition. """

    def __init__(self, ai_id, ai):
        self.id = ai_id
        self.ai = ai
        self._results = {}

    def win(self, opponent_id):
        if not opponent_id in self._results:
            self._results[opponent_id] = {"wins": 0, "losses": 0}
        self._results[opponent_id]["wins"] += 1

    def lose(self, opponent_id):
        if not opponent_id in self._results:
            self._results[opponent_id] = {"wins": 0, "losses": 0}
        self._results[opponent_id]["losses"] += 1

    def clear_results(self, opponent_id):
        self._results[opponent_id] = {"wins": 0, "losses": 0}

    @property
    def wins(self):
        return sum([o["wins"] for o in self._results.values()])

    @property
    def losses(self):
        return sum([o["losses"] for o in self._results.values()])

    @property
    def total_games(self):
        return self.wins + self.losses


class Competition(object):
    def __init__(self, games_to_run=1000, threaded=True):
        self.__games_to_run = games_to_run
        self.__entries = {}
        self.threaded = threaded

        if threaded:
            self.game_queue = Queue()

            def gamerunner():
                while True:
                    entries = self.game_queue.get()
                    self._play_game(entries[0], entries[1])
                    self.game_queue.task_done()

            t = Thread(target=gamerunner)
            t.daemon = True
            t.start()
            # TODO: Ensure the thread is killed

    def add(self, ai_id, ai):
        """ Add an ai into the competition.

        If the AI already exists it will be replaced.
        """
        self.__entries[ai_id] = Entry(ai_id, ai)
        self._run_games(ai_id)

    def _play_game(self, ai_1_id, ai_2_id):
        ai1 = self.entries[ai_1_id]
        ai2 = self.entries[ai_2_id]

        player1 = Player(ai=ai1.ai())
        player2 = Player(opponent=player1, ai=ai2.ai())
        player1.opponent = player2
        game = GameRunner(player1, player2)
        winner = game.play()
        if winner == player1:
            ai1.win(ai_2_id)
            ai2.lose(ai_1_id)
        else:
            ai1.lose(ai_2_id)
            ai2.win(ai_1_id)

    def _run_games(self, ai_id):
        """ Run (or re-run) all games for a given ai. """
        for k in self.entries.keys():
            if not k == ai_id:
                # First clear existing results with this AI
                self.entries[k].clear_results(ai_id)

                for i in range(self.__games_to_run / 2):
                    if self.threaded:
                        self.game_queue.put([ai_id, k])
                        self.game_queue.put([k, ai_id])
                    else:
                        self._play_game(ai_id, k)
                        self._play_game(k, ai_id)

    @property
    def entries(self):
        return self.__entries
