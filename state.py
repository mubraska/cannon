import pandas as pd
import actions


def evaluate_state(evaluation_state, player, searching_player):
    opponent = "2"
    player_town = "3"
    opponent_town = "4"

    if player == "2":
        opponent = "1"
        player_town = "4"
        opponent_town = "3"

    material_score = 2 * (evaluation_state.board.count(player) - evaluation_state.board.count(opponent))

    if len(evaluation_state.previous_actions) > 2:
        material_score += 200 * (
                evaluation_state.board.count(player_town) - evaluation_state.board.count(opponent_town))

    opponent_actions = pd.DataFrame(evaluation_state.get_actions(opponent), columns=["trigger_location"])

    if len(opponent_actions) == 0:
        material_score += 200

    action_codes = list(map(lambda x: x["type"] + "-" + str(x["location"]) + "-" + str(x["target"]),
                            list(filter(lambda x: x["type"] == "CM", evaluation_state.previous_actions))))

    repetition_punishment = 20 * (len(action_codes) - len(set(action_codes)))

    player_pawn_positions = [i for i, ltr in enumerate(evaluation_state.board) if ltr == player]
    player_actions = pd.DataFrame(evaluation_state.get_actions(player), columns=["trigger_location"])
    player_isolated_pawns = len(list(filter(lambda y: y < 2,
                                            map(lambda x: len(player_actions[player_actions["trigger_location"] == x]),
                                                player_pawn_positions))))

    opponent_pawn_positions = [i for i, ltr in enumerate(evaluation_state.board) if ltr == opponent]
    opponent_isolated_pawns = len(
        list(filter(lambda y: y == 0, map(lambda x: len(opponent_actions[opponent_actions["trigger_location"] == x]),
                                          opponent_pawn_positions))))

    isolated_pawn_score = 0.5 * (player_isolated_pawns - opponent_isolated_pawns)

    mobility_score = 0.1 * (len(evaluation_state.get_actions(player)) - len(evaluation_state.get_actions(opponent)))

    score = ((material_score + mobility_score) - repetition_punishment - isolated_pawn_score) * (
        -1 if searching_player != player else 1)

    return score


class State:
    def __init__(self, seed, previous_actions):
        self.board = seed[:100]
        self.player = seed[100]
        self.opponent = "2" if self.player == "1" else "1"
        self.player_town = "3" if self.player == "1" else "4"
        self.opponent_town = "4" if self.player == "2" else "3"
        self.seed = seed
        self.previous_actions = previous_actions
        self.previous_action = previous_actions[-1] if len(previous_actions) > 0 else None
        self.actions = pd.DataFrame(self.get_actions(self.player),
                                    columns=["trigger_location", "location", "type", "target", "next_state"])
        self.actions["player"] = self.player
        self.best_action = None

    def get_game_result(self):
        if self.previous_action is not None and (
                self.previous_action["type"] == "TC" or self.previous_action["type"] == "TS"):
            return self.player
        elif len(self.actions) == 0:
            return "1" if self.player == "2" else "1"

        return None

    def get_actions(self, player):
        opponent = "1" if player == "2" else "2"
        opponent_town = "3" if player == "2" else "4"
        available_actions = []

        if self.previous_action is not None and (
                self.previous_action["type"] == "TC" or self.previous_action["type"] == "TS"):
            return available_actions

        if self.previous_action is None or self.previous_action["type"] == "TP":
            available_actions = actions.black_town_place(self.board) if player == "1" else actions.red_town_place(
                self.board)

        if len(available_actions) > 0:
            return available_actions

        return actions.get_town_shoots(self.board, player, opponent_town) + \
               actions.get_town_captures(self.board, player, opponent_town) + \
               actions.get_shoots(self.board, player, opponent) + \
               actions.get_pawn_captures(self.board, player, opponent) + \
               actions.get_pawn_moves(self.board, player) + \
               actions.get_retreats(self.board, player) + \
               actions.get_cannon_moves(self.board, player)
