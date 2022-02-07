import random


class Zobrist:
    def __init__(self):
        self.table = [[random.randint(1, 2 ** 64 - 1) for _ in range(4)] for _ in range(101)]

    def compute_hash(self, board):
        h = 0
        for i in range(100):
            if board[i] != "0":
                piece = int(board[i]) - 1
                h ^= self.table[i][piece]
        return h
