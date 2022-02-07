import time

import state
from zobrist import Zobrist
from state import State


class Network:
    def __init__(self):
        self.zobrist = Zobrist()
        self.transposition_table = {}
        self.killer_moves = {}
        self.move_ordering = {}

    def refresh(self):
        self.transposition_table = {}
        self.killer_moves = {}
        self.move_ordering = {}

    def get_best_action(self, current_state):
        self.iterative_deepening(current_state, 10)
        return self.transposition_table[self.zobrist.compute_hash(current_state.board)]["action"]

    def get_table_entry(self, table, board, player, depth):
        board_hash = self.zobrist.compute_hash(board)

        if board_hash not in table:
            return None

        if table[board_hash]["player"] != player:
            return None

        if depth is not None and table[board_hash]["depth"] < depth:
            return None

        return table[board_hash]

    def get_board_state_value(self, current_state, player, searching_player):
        move_ordering_entry = self.get_table_entry(self.move_ordering, current_state.board, player, None)
        if move_ordering_entry is not None:
            return move_ordering_entry["value"] * (1 if player == move_ordering_entry["player"] else -1)

        return state.evaluate_state(current_state, player, searching_player)

    def iterative_deepening(self, current_state, search_time):
        depth = 1
        start = time.time()
        while True:
            current_state.actions["reward"] = current_state.actions.apply(
                lambda x: self.get_board_state_value(State(x["next_state"], current_state.previous_actions + [x]),
                                                     current_state.opponent, current_state.player),
                axis=1)

            current_state.actions = current_state.actions.sort_values(by="reward", ascending=False)

            value = self.negascout(current_state, depth, -100, 100, current_state.player, start, search_time)

            if abs(value) == 9999:
                break

            depth += 1

        print("depth: " + str(depth))

    def negascout(self, current_state, depth, alpha, beta, searching_player, start, search_time):
        if time.time() - start > search_time:
            return 9999

        killer_moves_entry = self.get_table_entry(self.killer_moves, current_state.board, current_state.player, depth)

        if killer_moves_entry is not None and killer_moves_entry["depth"] >= depth:
            return killer_moves_entry["value"]

        transposition_table_entry = self.get_table_entry(self.transposition_table, current_state.board,
                                                         current_state.player, depth)

        a = alpha
        b = beta

        if transposition_table_entry is not None:
            transposition_table_value = transposition_table_entry["value"]

            if transposition_table_entry["flag"] == "Exact":
                return transposition_table_value

            elif transposition_table_entry["flag"] == "LowerBound":
                a = max(a, transposition_table_value)

            elif transposition_table_entry["flag"] == "UpperBound":
                beta = min(beta, transposition_table_value)

            if a >= beta:
                return transposition_table_value

        terminal_node = current_state.get_game_result() is not None

        if terminal_node or depth == 0:
            terminal_value = state.evaluate_state(current_state, searching_player, current_state.player)
            return terminal_value

        best_action = None

        check_actions = current_state.actions.copy()

        for i in range(0, len(check_actions)):
            action = check_actions.iloc[i]
            child = State(action["next_state"], current_state.previous_actions + [action])
            value = -self.negascout(child, depth - 1, -b, -a, searching_player, start, search_time)
            if abs(value) == 9999:
                return value

            if a < value < beta and i > 0:
                a = -self.negascout(child, depth - 1, -beta, -value, searching_player, start, search_time)
                if abs(value) == 9999:
                    return value

            if value > a or best_action is None:
                best_action = action
                a = value

            self.move_ordering[self.zobrist.compute_hash(child.board)] = {
                "value": value,
                "player": child.player,
                "depth": depth
            }

            if a >= beta:
                self.killer_moves[self.zobrist.compute_hash(current_state.board)] = {
                    "value": a,
                    "player": current_state.player,
                    "depth": depth
                }
                break

            b = a + 1

        if a <= alpha:
            flag = "UpperBound"

        elif a >= b:
            flag = "LowerBound"

        else:
            flag = "Exact"

        self.transposition_table[self.zobrist.compute_hash(current_state.board)] = {
            "action": best_action if best_action is not None else check_actions.iloc[0],
            "value": a,
            "flag": flag,
            "player": current_state.player,
            "depth": depth
        }

        return a
