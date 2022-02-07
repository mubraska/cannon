from state import State


class Game:
    def __init__(self):
        self.prev_states = []
        self.current_state_seed = "00000000000202020202020202020202020202020000000000000000000010101010101010101010101010101000000000001"
        self.current_state = State(self.current_state_seed, [])
        self.next_states = []

    def execute_action(self, action):
        self.prev_states.append(self.current_state)
        self.current_state_seed = action["next_state"]
        print(self.current_state_seed)
        self.current_state = State(self.current_state_seed, self.current_state.previous_actions + [action])
        self.next_states = []

    def undo(self):
        self.next_states.append(self.current_state)
        self.current_state = self.prev_states.pop()

    def redo(self):
        self.prev_states.append(self.current_state)
        self.current_state = self.next_states.pop()

    def reset_game(self):
        self.prev_states = []
        self.current_state_seed = "00000000000202020202020202020202020202020000000000000000000010101010101010101010101010101000000000001"
        self.current_state = State(self.current_state_seed, [])
        self.next_states = []
