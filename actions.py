import re


def get_action(trigger_location, location, target, action_type, board, player):
    return {
        "trigger_location": trigger_location,
        "location": location,
        "target": target,
        "type": action_type,
        "next_state": get_next_state(location, target, action_type, board, player)
    }


def get_adjacent_pawns(board, player, player2):
    return set([m.start(0) + 1 for m in re.finditer(player2 + player, board) if m.start(0) % 10 < 9] + \
               [m.start(0) + 11 for m in re.finditer(player2 + r"(?=\d{10}" + player + ")", board) if
                m.start(0) % 10 < 9] + \
               [m.start(0) + 10 for m in re.finditer(player2 + r"(?=\d{9}" + player + ")", board)] + \
               [m.start(0) + 9 for m in re.finditer(player2 + r"(?=\d{8}" + player + ")", board) if
                m.start(0) % 10 > 0] + \
               [m.start(0) for m in re.finditer(player + player2, board) if m.start(0) % 10 < 9] + \
               [m.start(0) for m in re.finditer(player + r"(?=\d{10}" + player2 + ")", board) if m.start(0) % 10 < 9] + \
               [m.start(0) for m in re.finditer(player + r"(?=\d{9}" + player2 + ")", board)] + \
               [m.start(0) for m in re.finditer(player + r"(?=\d{8}" + player2 + ")", board) if m.start(0) % 10 > 0])


def pawn_move_tl(board, player):
    return [get_action(m.start(0) + 11, m.start(0) + 11, m.start(0), "PM", board, player) for m in
            re.finditer(r"0(?=\d{10}" + player + ")", board) if
            (m.start(0) + 11) % 10 > 0]


def pawn_move_t(board, player):
    return [get_action(m.start(0) + 10, m.start(0) + 10, m.start(0), "PM", board, player) for m in
            re.finditer(r"0(?=\d{9}" + player + ")", board)]


def pawn_move_tr(board, player):
    return [get_action(m.start(0) + 9, m.start(0) + 9, m.start(0), "PM", board, player) for m in
            re.finditer(r"0(?=\d{8}" + player + ")", board) if
            (m.start(0) + 9) % 10 < 9]


def pawn_move_br(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 11, "PM", board, player) for m in
            re.finditer(player + r"(?=\d{10}0)", board) if m.start(0) % 10 < 9]


def pawn_move_b(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 10, "PM", board, player) for m in
            re.finditer(player + r"(?=\d{9}0)", board) if
            m.start(0) % 10]


def pawn_move_bl(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 9, "PM", board, player) for m in
            re.finditer(player + r"(?=\d{8}0)", board) if
            m.start(0) % 10 > 0]


def pawn_capture_l(board, pawn, opponent, capture_type):
    return [get_action(m.start(0) + 1, m.start(0) + 1, m.start(0), capture_type, board, pawn) for m in
            re.finditer(opponent + pawn, board) if (m.start(0) + 1) % 10 > 0]


def pawn_capture_tl(board, pawn, opponent, capture_type):
    return [get_action(m.start(0) + 11, m.start(0) + 11, m.start(0), capture_type, board, pawn) for m in
            re.finditer(opponent + r"(?=\d{10}" + pawn + ")", board) if (m.start(0) + 11) % 10 > 0]


def pawn_capture_t(board, pawn, opponent, capture_type):
    return [get_action(m.start(0) + 10, m.start(0) + 10, m.start(0), capture_type, board, pawn) for m in
            re.finditer(opponent + r"(?=\d{9}" + pawn + ")", board)]


def pawn_capture_tr(board, pawn, opponent, capture_type):
    return [get_action(m.start(0) + 9, m.start(0) + 9, m.start(0), capture_type, board, pawn) for m in
            re.finditer(opponent + r"(?=\d{8}" + pawn + ")", board) if (m.start(0) + 9) % 10 < 9]


def pawn_capture_r(board, pawn, opponent, capture_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 1, capture_type, board, pawn) for m in
            re.finditer(pawn + opponent, board) if m.start(0) % 10 < 9]


def pawn_capture_br(board, pawn, opponent, capture_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 11, capture_type, board, pawn) for m in
            re.finditer(pawn + r"(?=\d{10}" + opponent + ")", board) if m.start(0) % 10 < 9]


def pawn_capture_b(board, pawn, opponent, capture_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 10, capture_type, board, pawn) for m in
            re.finditer(pawn + r"(?=\d{9}" + opponent + ")", board)]


def pawn_capture_bl(board, pawn, opponent, capture_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 9, capture_type, board, pawn) for m in
            re.finditer(pawn + r"(?=\d{8}" + opponent + ")", board) if m.start(0) % 10 > 0]


def black_pawn_retreat(board):
    adjacent_pawns = get_adjacent_pawns(board, "1", "2")

    return [get_action(m.start(0), m.start(0), m.start(0) + 18, "PR", board, "1") for m in
            re.finditer(r"1(?=\d{8}0\d{8}0)", board)
            if m.start(0) % 10 > 1 and m.start(0) in adjacent_pawns] + \
           [get_action(m.start(0), m.start(0), m.start(0) + 20, "PR", board, "1") for m in
            re.finditer(r"1(?=\d{9}0\d{9}0)", board)
            if m.start(0) in adjacent_pawns] + \
           [get_action(m.start(0), m.start(0), m.start(0) + 22, "PR", board, "1") for m in
            re.finditer(r"1(?=\d{10}0\d{10}0)", board) if m.start(0) % 10 < 8 and m.start(0) in adjacent_pawns]


def red_pawn_retreat(board):
    adjacent_pawns = get_adjacent_pawns(board, "2", "1")

    return [get_action(m.start(0) + 18, m.start(0) + 18, m.start(0), "PR", board, "2") for m in
            re.finditer(r"0(?=\d{8}0\d{8}2)", board)
            if m.start(0) % 10 > 1 and (m.start(0) + 18) in adjacent_pawns] + \
           [get_action(m.start(0) + 20, m.start(0) + 20, m.start(0), "PR", board, "2") for m in
            re.finditer(r"0(?=\d{9}0\d{9}2)", board)
            if (m.start(0) + 20) in adjacent_pawns] + \
           [get_action(m.start(0) + 22, m.start(0) + 22, m.start(0), "PR", board, "2") for m in
            re.finditer(r"0(?=\d{10}0\d{10}2)", board) if m.start(0) % 10 < 8 and (m.start(0) + 22) in adjacent_pawns]


def cannon_move_l(board, player):
    return [get_action(m.start(0) + 1, m.start(0) + 3, m.start(0), "CM", board, player) for m in
            re.finditer(f"0{player * 3}", board) if m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 2, m.start(0) + 3, m.start(0), "CM", board, player) for m in
            re.finditer(f"0{player * 3}", board) if m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 3, m.start(0) + 3, m.start(0), "CM", board, player) for m in
            re.finditer(f"0{player * 3}", board) if m.start(0) % 10 < 7]


def cannon_move_tl(board, player):
    return [get_action(m.start(0) + 11, m.start(0) + 33, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board) if
            m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 22, m.start(0) + 33, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board) if
            m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 33, m.start(0) + 33, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board) if
            m.start(0) % 10 < 7]


def cannon_move_t(board, player):
    return [get_action(m.start(0) + 10, m.start(0) + 30, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
           [get_action(m.start(0) + 20, m.start(0) + 30, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
           [get_action(m.start(0) + 30, m.start(0) + 30, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)]


def cannon_move_tr(board, player):
    return [get_action(m.start(0) + 9, m.start(0) + 27, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 2] + \
           [get_action(m.start(0) + 18, m.start(0) + 27, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 2] + \
           [get_action(m.start(0) + 27, m.start(0) + 27, m.start(0), "CM", board, player) for m in
            re.finditer(r"0(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 2]


def cannon_move_r(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 3, "CM", board, player) for m in
            re.finditer(f"{player * 3}0", board) if m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 1, m.start(0), m.start(0) + 3, "CM", board, player) for m in
            re.finditer(f"{player * 3}0", board) if m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 2, m.start(0), m.start(0) + 3, "CM", board, player) for m in
            re.finditer(f"{player * 3}0", board) if m.start(0) % 10 < 7]


def cannon_move_br(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 33, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0)", board) if
            m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 11, m.start(0), m.start(0) + 33, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0)", board) if
            m.start(0) % 10 < 7] + \
           [get_action(m.start(0) + 22, m.start(0), m.start(0) + 33, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0)", board) if
            m.start(0) % 10 < 7]


def cannon_move_b(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 30, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0)", board)] + \
           [get_action(m.start(0) + 10, m.start(0), m.start(0) + 30, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0)", board)] + \
           [get_action(m.start(0) + 20, m.start(0), m.start(0) + 30, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0)", board)]


def cannon_move_bl(board, player):
    return [get_action(m.start(0), m.start(0), m.start(0) + 27, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0)", board) if
            m.start(0) % 10 > 2] + \
           [get_action(m.start(0) + 9, m.start(0), m.start(0) + 27, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0)", board) if
            m.start(0) % 10 > 2] + \
           [get_action(m.start(0) + 18, m.start(0), m.start(0) + 27, "CM", board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0)", board) if
            m.start(0) % 10 > 2]


def shoot_l(board, player, opponent, shoot_type):
    return [get_action(m.start(0) + 2, m.start(0) + 4, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}0{player * 3}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 3, m.start(0) + 5, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}00{player * 3}", board) if m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 3, m.start(0) + 4, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}0{player * 3}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 4, m.start(0) + 5, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}00{player * 3}", board) if m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 4, m.start(0) + 4, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}0{player * 3}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 5, m.start(0) + 5, m.start(0), shoot_type, board, player) for m in
            re.finditer(f"{opponent}00{player * 3}", board) if m.start(0) % 10 < 5]


def shoot_tl(board, player, opponent, shoot_type):
    return [get_action(m.start(0) + 22, m.start(0) + 44, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 33, m.start(0) + 55, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")",
                        board) if
            m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 33, m.start(0) + 44, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 44, m.start(0) + 55, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")",
                        board) if
            m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 44, m.start(0) + 44, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 55, m.start(0) + 55, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{10}0\d{10}0\d{10}" + player + r"\d{10}" + player + r"\d{10}" + player + ")",
                        board) if
            m.start(0) % 10 < 5]


def shoot_t(board, player, opponent, shoot_type):
    return [get_action(m.start(0) + 20, m.start(0) + 40, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
           [get_action(m.start(0) + 30, m.start(0) + 50, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")",
                        board)] + \
           [get_action(m.start(0) + 30, m.start(0) + 40, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
           [get_action(m.start(0) + 40, m.start(0) + 50, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")",
                        board)] + \
           [get_action(m.start(0) + 40, m.start(0) + 40, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
           [get_action(m.start(0) + 50, m.start(0) + 50, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{9}0\d{9}0\d{9}" + player + r"\d{9}" + player + r"\d{9}" + player + ")",
                        board)]


def shoot_tr(board, player, opponent, shoot_type):
    return [get_action(m.start(0) + 18, m.start(0) + 36, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0) + 27, m.start(0) + 45, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")",
                        board) if
            m.start(0) % 10 > 4] + \
           [get_action(m.start(0) + 27, m.start(0) + 36, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0) + 36, m.start(0) + 45, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")",
                        board) if
            m.start(0) % 10 > 4] + \
           [get_action(m.start(0) + 36, m.start(0) + 36, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0) + 45, m.start(0) + 45, m.start(0), shoot_type, board, player) for m in
            re.finditer(opponent + r"(?=\d{8}0\d{8}0\d{8}" + player + r"\d{8}" + player + r"\d{8}" + player + ")",
                        board) if
            m.start(0) % 10 > 4]


def shoot_r(board, player, opponent, shoot_type):
    return [get_action(m.start(0), m.start(0) + 2, m.start(0) + 4, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}0{opponent}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0), m.start(0) + 2, m.start(0) + 5, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}00{opponent}", board) if m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 1, m.start(0) + 2, m.start(0) + 4, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}0{opponent}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 1, m.start(0) + 2, m.start(0) + 5, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}00{opponent}", board) if m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 2, m.start(0) + 2, m.start(0) + 4, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}0{opponent}", board) if m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 2, m.start(0) + 2, m.start(0) + 5, shoot_type, board, player) for m in
            re.finditer(f"{player * 3}00{opponent}", board) if m.start(0) % 10 < 5]


def shoot_br(board, player, opponent, shoot_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 44, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}" + opponent + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0), m.start(0), m.start(0) + 55, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}0\d{10}" + opponent + ")",
                        board) if
            m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 11, m.start(0), m.start(0) + 44, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}" + opponent + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 11, m.start(0), m.start(0) + 55, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}0\d{10}" + opponent + ")",
                        board) if
            m.start(0) % 10 < 5] + \
           [get_action(m.start(0) + 22, m.start(0), m.start(0) + 44, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}" + opponent + ")", board)
            if
            m.start(0) % 10 < 6] + \
           [get_action(m.start(0) + 22, m.start(0), m.start(0) + 55, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{10}" + player + r"\d{10}" + player + r"\d{10}0\d{10}0\d{10}" + opponent + ")",
                        board) if
            m.start(0) % 10 < 5]


def shoot_b(board, player, opponent, shoot_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 40, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}" + opponent + ")", board)] + \
           [get_action(m.start(0), m.start(0), m.start(0) + 50, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}0\d{9}" + opponent + ")",
                        board)] + \
           [get_action(m.start(0) + 10, m.start(0), m.start(0) + 40, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}" + opponent + ")", board)] + \
           [get_action(m.start(0) + 10, m.start(0), m.start(0) + 50, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}0\d{9}" + opponent + ")",
                        board)] + \
           [get_action(m.start(0) + 20, m.start(0), m.start(0) + 40, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}" + opponent + ")", board)] + \
           [get_action(m.start(0) + 20, m.start(0), m.start(0) + 50, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{9}" + player + r"\d{9}" + player + r"\d{9}0\d{9}0\d{9}" + opponent + ")",
                        board)]


def shoot_bl(board, player, opponent, shoot_type):
    return [get_action(m.start(0), m.start(0), m.start(0) + 36, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}" + opponent + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0), m.start(0), m.start(0) + 45, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}0\d{8}" + opponent + ")",
                        board) if
            m.start(0) % 10 > 4] + \
           [get_action(m.start(0) + 9, m.start(0), m.start(0) + 36, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}" + opponent + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0) + 9, m.start(0), m.start(0) + 45, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}0\d{8}" + opponent + ")",
                        board) if
            m.start(0) % 10 > 4] + \
           [get_action(m.start(0) + 18, m.start(0), m.start(0) + 36, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}" + opponent + ")", board) if
            m.start(0) % 10 > 3] + \
           [get_action(m.start(0) + 18, m.start(0), m.start(0) + 45, shoot_type, board, player) for m in
            re.finditer(player + r"(?=\d{8}" + player + r"\d{8}" + player + r"\d{8}0\d{8}0\d{8}" + opponent + ")",
                        board) if
            m.start(0) % 10 > 4]


def get_cannon_count(board, player):
    return len([1 for m in re.finditer(f"{player * 3}", board) if m.start(0) % 10 < 7] + \
            [1 for m in re.finditer(r"(?=" + player + r"\d{10}" + player + r"\d{10}" + player + ")", board) if
            m.start(0) % 10 < 7] + \
            [1 for _ in re.finditer(r"(?=" + player + r"\d{9}" + player + r"\d{9}" + player + ")", board)] + \
            [1 for m in re.finditer(r"(?=" + player + r"\d{8}" + player + r"\d{8}" + player + ")", board) if
            m.start(0) % 10 > 2])


def black_town_place(board):
    return [
            get_action("100", 100, 91, "TP", board, "3"),
            get_action("100", 100, 92, "TP", board, "3"),
            get_action("100", 100, 93, "TP", board, "3"),
            get_action("100", 100, 94, "TP", board, "3"),
            get_action("100", 100, 95, "TP", board, "3"),
            get_action("100", 100, 96, "TP", board, "3"),
            get_action("100", 100, 97, "TP", board, "3"),
            get_action("100", 100, 98, "TP", board, "3")] if "".join(set(board[90:100])) == "0" else []


def red_town_place(board):
    return [
            get_action("101", 101, 1, "TP", board, "4"),
            get_action("101", 101, 2, "TP", board, "4"),
            get_action("101", 101, 3, "TP", board, "4"),
            get_action("101", 101, 4, "TP", board, "4"),
            get_action("101", 101, 5, "TP", board, "4"),
            get_action("101", 101, 6, "TP", board, "4"),
            get_action("101", 101, 7, "TP", board, "4"),
            get_action("101", 101, 8, "TP", board, "4")] if "".join(set(board[:10])) == "0" else []


def get_town_captures(board, player, opponent_town):
    if player == "1":
        return pawn_capture_l(board, player, opponent_town, "TC") + \
               pawn_capture_tl(board, player, opponent_town, "TC") + \
               pawn_capture_t(board, player, opponent_town, "TC") + \
               pawn_capture_tr(board, player, opponent_town, "TC") + \
               pawn_capture_r(board, player, opponent_town, "TC")

    return pawn_capture_l(board, player, opponent_town, "TC") + \
           pawn_capture_bl(board, player, opponent_town, "TC") + \
           pawn_capture_b(board, player, opponent_town, "TC") + \
           pawn_capture_br(board, player, opponent_town, "TC") + \
           pawn_capture_r(board, player, opponent_town, "TC")


def get_town_shoots(board, player, opponent_town):
    return shoot_l(board, player, opponent_town, "TS") + \
           shoot_tl(board, player, opponent_town, "TS") + \
           shoot_t(board, player, opponent_town, "TS") + \
           shoot_tr(board, player, opponent_town, "TS") + \
           shoot_r(board, player, opponent_town, "TS") + \
           shoot_br(board, player, opponent_town, "TS") + \
           shoot_b(board, player, opponent_town, "TS") + \
           shoot_bl(board, player, opponent_town, "TS")


def get_shoots(board, player, opponent):
    return shoot_l(board, player, opponent, "S") + \
           shoot_tl(board, player, opponent, "S") + \
           shoot_t(board, player, opponent, "S") + \
           shoot_tr(board, player, opponent, "S") + \
           shoot_r(board, player, opponent, "S") + \
           shoot_br(board, player, opponent, "S") + \
           shoot_b(board, player, opponent, "S") + \
           shoot_bl(board, player, opponent, "S")


def get_pawn_captures(board, player, opponent):
    if player == "1":
        return pawn_capture_l(board, player, opponent, "PC") + \
               pawn_capture_tl(board, player, opponent, "PC") + \
               pawn_capture_t(board, player, opponent, "PC") + \
               pawn_capture_tr(board, player, opponent, "PC") + \
               pawn_capture_r(board, player, opponent, "PC")

    return pawn_capture_l(board, player, opponent, "PC") + \
           pawn_capture_bl(board, player, opponent, "PC") + \
           pawn_capture_b(board, player, opponent, "PC") + \
           pawn_capture_br(board, player, opponent, "PC") + \
           pawn_capture_r(board, player, opponent, "PC")


def get_retreats(board, player):
    return black_pawn_retreat(board) if player == "1" else red_pawn_retreat(board)


def get_cannon_moves(board, player):
    return cannon_move_l(board, player) + \
           cannon_move_tl(board, player) + \
           cannon_move_t(board, player) + \
           cannon_move_tr(board, player) + \
           cannon_move_r(board, player) + \
           cannon_move_br(board, player) + \
           cannon_move_b(board, player) + \
           cannon_move_bl(board, player)


def get_pawn_moves(board, player):
    if player == "1":
        return pawn_move_tl(board, player) + \
               pawn_move_t(board, player) + \
               pawn_move_tr(board, player)

    return pawn_move_bl(board, player) + \
           pawn_move_b(board, player) + \
           pawn_move_br(board, player)

def play_action(current_state, action_location, action_target, location_replacement, target_replacement):
    if action_location < action_target:
        return f"{current_state[:action_location]}{location_replacement}{current_state[action_location + 1:action_target]}{target_replacement}{current_state[action_target + 1:]}"

    return f"{current_state[:action_target]}{target_replacement}{current_state[action_target + 1:action_location]}{location_replacement}{current_state[action_location + 1:]}"


def play_place_town_action(current_state, action_target, target_replacement):
    return f"{current_state[:action_target]}{target_replacement}{current_state[action_target + 1:]}"


def get_next_state(action_location, action_target, action_type, current_state, player):
    if action_type == "TP":
        return play_place_town_action(current_state, action_target, player) + (
            "1" if player == "4" else "2")

    location_replacement = "0"
    target_replacement = current_state[action_location]

    if action_type == "S":
        location_replacement = current_state[action_location]
        target_replacement = "0"

    return play_action(current_state, action_location, action_target, location_replacement, target_replacement) + (
        "1" if player == "2" else "2")
