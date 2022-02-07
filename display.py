from functools import reduce
from threading import Thread
import pygame
import numpy as np
import pandas as pd
from network import Network
from game import Game

image_dict = {
    "white-pawn": pygame.image.load("images/white-pawn.png"),
    "black-pawn": pygame.image.load("images/black-pawn.png"),
    "castle": pygame.image.load("images/castle.png"),
    "pawn-move": pygame.image.load("images/pawn-move.png"),
    "capture-pawn": pygame.image.load("images/capture-pawn.png"),
    "pawn-retreat": pygame.image.load("images/pawn-retreat.png"),
    "cannon-move": pygame.image.load("images/cannon-move.png"),
    "shoot": pygame.image.load("images/shoot.png"),
    "town-kill": pygame.image.load("images/town-kill.png"),
    "town-place": pygame.image.load("images/build.png")
}

piece_dict = {
    "0": {
        "type": "blank"
    },
    "1": {
        "type": "pawn",
        "color": (64, 64, 64),
        "player": "1",
        "icon": image_dict["white-pawn"]
    },
    "2": {
        "type": "pawn",
        "color": (254, 48, 0),
        "player": "2",
        "icon": image_dict["black-pawn"]
    },
    "3": {
        "type": "town",
        "color": (64, 64, 64),
        "player": "1",
        "icon": image_dict["castle"]
    },
    "4": {
        "type": "town",
        "color": (254, 48, 0),
        "player": "2",
        "icon": image_dict["castle"]
    }
}

action_dict = {
    "PM": {
        "color": (74, 134, 198),
        "icon": image_dict["pawn-move"]
    },
    "PC": {
        "color": (255, 87, 34),
        "icon": image_dict["capture-pawn"]
    },
    "PR": {
        "color": (255, 255, 255),
        "icon": image_dict["pawn-retreat"]
    },
    "CM": {
        "color": (197, 235, 152),
        "icon": image_dict["cannon-move"]
    },
    "S": {
        "color": (239, 239, 239),
        "icon": image_dict["shoot"]
    },
    "TS": {
        "color": (255, 208, 91),
        "icon": image_dict["town-kill"]
    },
    "TC": {
        "color": (255, 208, 91),
        "icon": image_dict["town-kill"]
    },
    "TP": {
        "color": (225, 225, 227),
        "icon": image_dict["town-place"]
    },
}


def get_board_positions(padding, side_length, town_width):
    return np.array(
        [(padding + (i % 10) * side_length / 9, padding + int(i / 10) * side_length / 9) for i in range(100)] +
        [(side_length / 2 + padding, side_length + padding * 1.5 + town_width / 2 + (padding / 2 - town_width) / 2)] +
        [(side_length / 2 + padding, (padding / 2 - town_width) / 2 + town_width / 2)])


def draw_piece(piece, screen, clicked_piece, hovered_piece):
    border_color = (0, 0, 0)
    border_width = 1

    if clicked_piece == piece["index"]:
        border_color = (216, 247, 255)
        border_width = 5

    elif hovered_piece == piece["index"]:
        border_color = (255, 247, 125)
        border_width = 5

    if piece["type"] == "pawn":
        pygame.draw.circle(screen, border_color, piece["position"], piece["width"] / 2 + border_width,
                           width=border_width)
        pygame.draw.circle(screen, piece["color"], piece["position"], piece["width"] / 2)

        icon_width = pawn_icon_width
    else:
        pygame.draw.rect(screen, border_color,
                         pygame.Rect(piece["position"][0] - (piece["width"] / 2) - border_width,
                                     piece["position"][1] - (piece["width"] / 2) - border_width,
                                     piece["width"] + border_width * 2,
                                     piece["width"] + border_width * 2), border_width, 5)

        pygame.draw.rect(screen, piece["color"],
                         pygame.Rect(piece["position"][0] - (piece["width"] / 2),
                                     piece["position"][1] - (piece["width"] / 2), piece["width"], piece["width"]), 0, 5)

        icon_width = int(pawn_icon_width * 1.1)

    icon_position = (piece["position"][0] - icon_width / 2, piece["position"][1] - icon_width / 2)
    screen.blit(pygame.transform.scale(piece["icon"], (icon_width, icon_width)), icon_position)


def get_piece(piece_str, index):
    piece = piece_dict[piece_str].copy()
    piece["index"] = index
    piece["position"] = board_positions[index]
    piece["width"] = tile_side_length * 0.7 if piece["type"] == "pawn" else tile_side_length * 0.8
    piece["collision"] = get_collision(board_positions[index][0] - piece["width"] / 2,
                                       board_positions[index][1] - piece["width"] / 2, piece["width"], piece["width"])

    return piece


def get_pieces(board):
    board_state = pd.DataFrame([get_piece(p, i) for i, p in enumerate(list(board))])
    pieces = board_state[board_state["type"] != "blank"]

    if "3" not in board:
        black_town = piece_dict["3"].copy()
        black_town["index"] = "100"
        black_town["position"] = board_positions[100]
        black_town["width"] = tile_side_length * 0.8
        black_town["collision"] = get_collision(board_positions[100][0] - black_town["width"] / 2,
                                                board_positions[100][1] - black_town["width"] / 2, black_town["width"],
                                                black_town["width"])
        pieces = pieces.append(black_town, ignore_index=True)

    if "4" not in board:
        red_town = piece_dict["4"].copy()
        red_town["index"] = "101"
        red_town["position"] = board_positions[101]
        red_town["width"] = tile_side_length * 0.8
        red_town["collision"] = get_collision(board_positions[101][0] - red_town["width"] / 2,
                                              board_positions[101][1] - red_town["width"] / 2, red_town["width"],
                                              red_town["width"])
        pieces = pieces.append(red_town, ignore_index=True)
    return pieces


def get_hovered_component(components, mouse_position):
    for i, p in components.iterrows():
        if p["collision"](mouse_position):
            return p["index"] if "index" in p else p.name

    return None


def get_collision(x, y, width, height, rect=None):
    if rect is not None:
        return rect.collidepoint

    return pygame.Rect(x, y, width, height).collidepoint


def get_double_action_indexes(series):
    return reduce(lambda x, y: x + [y], series, [])


tile_side_length = 60
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
playground_side_length = tile_side_length * 9
playground_padding = tile_side_length * 2
board_positions = get_board_positions(playground_padding, playground_side_length, tile_side_length * 0.8)
pygame.font.init()
board_position_font = pygame.font.SysFont('Helvetica', int(tile_side_length * 0.18))
pawn_radius = int(tile_side_length * 0.35)
pawn_icon_width = int(tile_side_length * 0.5)
action_icon_width = int(tile_side_length * 0.6)
action_rect_width = pawn_radius * 2 + 4


class Display:
    def __init__(self, game, is_black_human, is_red_human):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((780, 780))
        self.running = False
        self.game = game
        self.pieces = get_pieces(self.game.current_state.board)
        self.hovered_piece = None
        self.hovered_action = None
        self.clicked_piece = None
        self.available_pieces = self.pieces[
            self.pieces["index"].isin(self.game.current_state.actions["trigger_location"].unique())]
        self.available_actions = None
        double_action_grouped = self.game.current_state.actions.reset_index().groupby(["trigger_location", "target"])
        self.double_actions = double_action_grouped.agg({"index": get_double_action_indexes})
        self.double_actions["size"] = double_action_grouped.size()
        self.double_actions = self.double_actions[self.double_actions["size"] > 1].reset_index()
        self.is_black_human = is_black_human
        self.is_red_human = is_red_human
        self.calculating = False
        self.network = Network()

    def refresh_game_state(self):
        self.pieces = get_pieces(self.game.current_state.board)
        self.hovered_piece = None
        self.hovered_action = None
        self.clicked_piece = None
        self.available_pieces = self.pieces[
            self.pieces["index"].isin(self.game.current_state.actions["trigger_location"])]
        self.available_actions = None
        double_action_grouped = self.game.current_state.actions.reset_index().groupby(["trigger_location", "target"])
        self.double_actions = double_action_grouped.agg({"index": get_double_action_indexes})
        self.double_actions["size"] = double_action_grouped.size()
        self.double_actions = self.double_actions[self.double_actions["size"] > 1].reset_index()
        self.calculating = False

    def draw_axis(self, point, length, axis):
        if axis == 1:
            self.screen.blit(board_position_font.render(str(10 - int(point[2])), False, (0, 0, 0)),
                             (tile_side_length + 15, point[1] - 8))
            pygame.draw.line(self.screen, (0, 0, 0), (point[0], point[1]), (point[0] + length, point[1]))
        else:
            self.screen.blit(board_position_font.render(letters[int(point[2])], False, (0, 0, 0)),
                             (point[0] - 2, tile_side_length + 10))
            pygame.draw.line(self.screen, (0, 0, 0), (point[0], point[1]), (point[0], point[1] + length))

    def draw_board(self):
        pygame.display.set_caption('Cannon Game')
        self.screen.fill((0, 0, 0))

        board_side_length = playground_side_length + tile_side_length * 2

        pygame.draw.rect(self.screen, "#D88234",
                         pygame.Rect(tile_side_length, tile_side_length, board_side_length, board_side_length))
        pygame.draw.rect(self.screen, "#E8BF85",
                         pygame.Rect(playground_padding, playground_padding, playground_side_length,
                                     playground_side_length))

        np.apply_along_axis(lambda x: self.draw_axis(x, playground_side_length, 1), axis=1,
                            arr=np.append(board_positions[:100][np.array(range(100)) % 10 == 0],
                                          np.arange(10).reshape(10, 1),
                                          axis=1))
        np.apply_along_axis(lambda x: self.draw_axis(x, playground_side_length, 0), axis=1,
                            arr=np.append(board_positions[:10], np.arange(10).reshape(10, 1), axis=1))

    def draw_action(self, action):
        action_position = board_positions[action["target"]]
        action_props = action_dict[action["type"]]

        double_action = self.double_actions[
            (self.double_actions["trigger_location"] == action["trigger_location"]) & (self.double_actions["target"] ==
                                                                                       action["target"])]
        if len(double_action) > 0 and action.name == double_action.values[0][2][0]:
            bigger_rect_width = action_rect_width * 1.3
            bigger_icon_width = action_icon_width * 1.2
            icon_position = (
                action_position[0] - (bigger_rect_width / 2) + (bigger_rect_width / 2 - bigger_icon_width / 2) / 2,
                action_position[1] - (bigger_rect_width / 2) + (bigger_rect_width / 2 - bigger_icon_width / 2) / 2)
            action_rect = pygame.Rect(action_position[0] - (bigger_rect_width / 2),
                                      action_position[1] - (bigger_rect_width / 2), bigger_rect_width / 2,
                                      bigger_rect_width / 2)
            self.screen.blit(
                pygame.transform.scale(action_props["icon"], (int(bigger_icon_width / 2), int(bigger_icon_width / 2))),
                icon_position)
        elif len(double_action.values) > 0 and action.name == double_action.values[0][2][1]:
            bigger_rect_width = action_rect_width * 1.3
            bigger_icon_width = action_icon_width * 1.2
            icon_position = (action_position[0] + (bigger_rect_width / 2 - bigger_icon_width / 2) / 2,
                             action_position[1] + (bigger_rect_width / 2 - bigger_icon_width / 2) / 2)
            action_rect = pygame.Rect(action_position[0], action_position[1], bigger_rect_width / 2,
                                      bigger_rect_width / 2)
            self.screen.blit(
                pygame.transform.scale(action_props["icon"], (int(bigger_icon_width / 2), int(bigger_icon_width / 2))),
                icon_position)
        else:
            icon_position = (
                action_position[0] - action_icon_width / 2, action_position[1] - action_icon_width / 2)
            action_rect = pygame.Rect(action_position[0] - (action_rect_width / 2),
                                      action_position[1] - (action_rect_width / 2), action_rect_width,
                                      action_rect_width)
            self.screen.blit(
                pygame.transform.scale(action_props["icon"], (action_icon_width, action_icon_width)),
                icon_position)

        action["collision"] = get_collision(None, None, None, None, action_rect)
        if self.hovered_action == action.name:
            pygame.draw.rect(self.screen, action_props["color"], action_rect, 2, 5)

        return action

    def draw_previous_action(self, action):
        action_position = board_positions[action["target"]]
        action_location_position = board_positions[action["location"]]
        action_props = action_dict[action["type"]]
        icon_position = (
            action_position[0] - action_icon_width / 2, action_position[1] - action_icon_width / 2)
        action_rect = pygame.Rect(action_location_position[0] - (action_rect_width / 2),
                                  action_location_position[1] - (action_rect_width / 2), action_rect_width,
                                  action_rect_width)
        self.screen.blit(
            pygame.transform.scale(action_props["icon"], (action_icon_width, action_icon_width)),
            icon_position)
        pygame.draw.rect(self.screen, action_props["color"], action_rect, 2, 5)

    def play_network_action(self):
        if self.game.current_state.get_game_result() is not None:
            return

        print("im in")
        self.calculating = True

        best_action = self.network.get_best_action(self.game.current_state)

        if len(self.game.next_states) == 0:
            self.game.execute_action(best_action)

            if self.game.current_state.get_game_result() is not None:
                pygame.time.wait(3000)
                self.game = Game()
                self.network = Network()

            self.network.refresh()
            self.refresh_game_state()

        print("im done")

    def run(self):
        self.running = True

        while self.running:
            self.draw_board()

            if self.game.current_state.get_game_result() is not None:
                self.game = Game()
                self.refresh_game_state()

            self.pieces.apply(lambda x: draw_piece(x, self.screen, self.clicked_piece, self.hovered_piece), axis=1)

            if self.available_actions is not None:
                self.available_actions = self.available_actions.apply(lambda x: self.draw_action(x), axis=1)

            if self.game.current_state.previous_action is not None:
                self.draw_previous_action(self.game.current_state.previous_action)

            if ((self.game.current_state.player == "1" and not self.is_black_human) or (
                    self.game.current_state.player == "2" and not self.is_red_human)) and not self.calculating and len(
                self.game.next_states) == 0:
                t = Thread(target=self.play_network_action)
                t.start()
            else:
                self.hovered_piece = get_hovered_component(self.available_pieces, pygame.mouse.get_pos())

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        if self.clicked_piece is None:
                            if self.hovered_piece is not None:
                                self.available_actions = self.game.current_state.actions[
                                    self.game.current_state.actions["trigger_location"] == self.hovered_piece]
                            else:
                                self.available_actions = None

                        else:
                            try:
                                self.hovered_action = get_hovered_component(self.available_actions,
                                                                            pygame.mouse.get_pos())
                            except:
                                print("boom boom mouse position bug, won't fix that")

                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        if event.key == pygame.K_z:
                            if len(self.game.prev_states) > 0:
                                self.game.undo()
                                self.refresh_game_state()
                        if event.key == pygame.K_y:
                            if len(self.game.next_states) > 0:
                                self.game.redo()
                                self.refresh_game_state()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.hovered_action is not None:
                            self.game.execute_action(
                                self.available_actions[self.available_actions.index == self.hovered_action].squeeze())
                            self.refresh_game_state()
                        elif self.hovered_piece is not None:
                            self.clicked_piece = self.hovered_piece
                            self.available_actions = self.game.current_state.actions[
                                self.game.current_state.actions["trigger_location"] == self.clicked_piece]
                        else:
                            self.clicked_piece = None
                            self.available_actions = None

            pygame.display.flip()
            pygame.time.wait(5)
