from game import Game
from card import Card
from typing import NamedTuple, List, Dict, Any
import sys


class GameManager:
    def __init__(self):
        self.game = Game.new_game()
        self.previous = []
        self.wins = 0
        self.losses = 0
        self.line_buffer = 0
        self.update_text = ["ROUND 1 START!"]

    def print_line(self, s: str):
        print(s)
        self.line_buffer += 1

    def clear_screen(self):
        if self.line_buffer > 0:
            sys.stdout.write("\033[K" + "\033[F\033[K" * self.line_buffer)
        self.line_buffer = 0

    def print_game_state(self):
        self.print_line(
            f"ROUND {self.game.round}\t\t"
            f"DECK {len(self.game.deck)}/52\t\t"
            f"RECORD {self.wins} - {self.losses}"
        )
        for l in self.game.get_field_text():
            self.print_line(l)
        self.print_line("")
        for l in self.update_text:
            self.print_line(l)
        self.print_line("")

    def reset_game(self):
        self.clear_screen()
        self.previous = []
        self.update_text = ["ROUND 1 START!"]
        self.game = Game.new_game()

    def play(self):
        while True:
            while self.game.state == "active":
                self.clear_screen()
                self.print_game_state()
                moves = self.game.get_moves()
                for i, move in enumerate(moves):
                    self.print_line(f"({i}) {self.game.get_move_text(move)}")

                can_undo = False
                if (
                    len(self.previous) > 0
                    and self.previous[-1].round == self.game.round
                ):
                    can_undo = True
                    self.print_line("(u) UNDO")

                self.print_line("(q) QUIT")

                while True:
                    move = input().strip().lower()
                    self.line_buffer += 1
                    if move == "q":
                        return
                    elif can_undo and move == "u":
                        break
                    try:
                        move = int(move)
                        if move >= 0 and move < len(moves):
                            break
                    except:
                        pass

                if can_undo and move == "u":
                    self.game = self.previous.pop()
                    self.update_text = ["REVERSED previous action!"]
                else:
                    self.previous.append(self.game)
                    self.game, self.update_text = self.game.apply_move(moves[move])

            self.clear_screen()
            self.print_game_state()
            if self.game.state == "loss":
                self.losses = self.losses + 1
                self.print_line("You lose!")
            if self.game.state == "win":
                self.wins = self.wins + 1
                self.print_line("You win!")
            self.print_line("Would you like to play again?")
            self.print_line("(y) Yes")
            self.print_line("(n) No")
            while True:
                again = input().strip().lower()
                self.line_buffer += 1
                if again == "n":
                    return
                elif again == "y":
                    break

            self.reset_game()


if __name__ == "__main__":
    GameManager().play()
