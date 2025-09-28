from game.agents.participant import Participant


class DumbParticipant(Participant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

