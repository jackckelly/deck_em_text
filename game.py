from typing import NamedTuple, List, Dict, Any, Tuple
from dataclasses import dataclass, astuple
from card import Card, Champ, Punch, Block, Health, Player
import random


@dataclass(frozen=True)
class Move:
    selected: str
    target: str


@dataclass(frozen=True)
class Game:
    field: Dict[str, Card]
    deck: List[Card]
    round: int
    state: str = "active"

    UPPER_ROW = ["A", "B", "C", "D"]
    LOWER_ROW = ["PUNCH", "PLAYER", "BLOCK", "CORNER"]
    RING = UPPER_ROW + LOWER_ROW
    NUM_ROUNDS = 12

    @staticmethod
    def starting_deck() -> List[Card]:
        deck = []
        for i in range(2, 15):
            deck.append(Champ(power=i))
            deck.append(Champ(power=i))
        for i in range(2, 11):
            deck.append(Health(health=i))
            deck.append(Block(protection=i, power_limit=15))
        for i in range(0, 4):
            deck.append(Punch(power=3, punch_name="Lucky"))
        for i in range(0, 2):
            deck.append(Punch(power=5, punch_name="Haymaker"))
        for i in range(0, 2):
            deck.append(Punch(punch_name="Sucker"))
        random.shuffle(deck)
        return deck

    @staticmethod
    def new_game() -> "Game":
        deck = Game.starting_deck()
        field = {
            **{slot: Card() for slot in Game.LOWER_ROW},
            **{slot: deck.pop() for slot in Game.UPPER_ROW},
        }
        field["PLAYER"] = Player(health=21)
        return Game(
            deck=deck,
            field=field,
            round=1,
        )

    def get_moves(self) -> List[Move]:
        moves = []
        for location in Game.RING:
            card = self.field[location]
            if card.name == "Champ":
                if self.field["BLOCK"].name != "Empty":
                    moves.append(Move(location, "BLOCK"))
                moves.append(Move(location, "PLAYER"))
            if card.name == "Health":
                moves.append(Move(location, "PLAYER"))
                if location != "CORNER":
                    moves.append(Move(location, "CORNER"))
            if card.name == "Block":
                if location != "BLOCK":
                    moves.append(Move(location, "BLOCK"))
                if location != "CORNER":
                    moves.append(Move(location, "CORNER"))
            if card.name == "Punch":
                if location != "PUNCH":
                    moves.append(Move(location, "PUNCH"))

                if location != "CORNER":
                    moves.append(Move(location, "CORNER"))
                    for slot in Game.UPPER_ROW:
                        if self.field[slot].name == "Champ":
                            moves.append(Move(location, slot))

        return moves

    def get_move_text(self, move: Move) -> str:
        selected, target = astuple(move)
        (selected_card, target_card) = (
            self.field[selected].name,
            self.field[target].name,
        )

        if (selected_card, target_card) in [("Champ", "Player"), ("Champ", "Block")]:
            return (
                f"[{selected} -> {target}]:"
                f"  DEFEND against {self.field[selected].display_text}"
                f" with {self.field[target].display_text}"
            )
        elif (selected_card, target_card) == ("Punch", "Champ"):
            return (
                f"[{selected} -> {target}]:"
                f"  PUNCH {self.field[target].display_text}"
                f" with {self.field[selected].display_text}"
            )
        elif (selected_card, target_card) == ("Health", "Player"):
            return (
                f"[{selected} -> {target}]:"
                f"  HEAL {self.field[target].display_text}"
                f" with {self.field[selected].display_text}"
            )
        elif selected_card in ["Health", "Block", "Punch"] and target_card in [
            "Health",
            "Block",
            "Punch",
            "Empty",
        ]:
            return (
                f"[{selected} -> {target}]:"
                f"  MOVE {self.field[selected].display_text}"
                f" to [{target}] ({self.field[target].display_text})"
            )

    def apply_move(self, move: Move) -> Tuple["Game", List[str]]:

        field = self.field.copy()
        deck = self.deck.copy()
        selected, target = astuple(move)

        (selected_card, target_card) = (field[selected], field[target])

        if (selected_card.name, target_card.name) == ("Champ", "Player"):
            field["PLAYER"] = Player(
                health=max(field["PLAYER"].health - field[selected].power, 0)
            )
            field[selected] = Card()

            update_text = [
                (
                    f"PLAYER took {selected_card.power} damage"
                    f" from {selected_card.display_text}!"
                    f" ({target_card.health} -> {field[target].health})"
                )
            ]

        elif (selected_card.name, target_card.name) == ("Champ", "Block"):
            if field[selected].power <= field["BLOCK"].power_limit:
                damage = max(field[selected].power - field["BLOCK"].protection, 0)
                field["BLOCK"] = Block(
                    protection=field["BLOCK"].protection,
                    power_limit=field[selected].power,
                )
                prefix = "BLOCK succeeded!"
            else:
                damage = field[selected].power
                field["BLOCK"] = Card()
                prefix = "BLOCK failed!"

            old_health = field["PLAYER"].health
            new_health = max(old_health - damage, 0)
            field["PLAYER"] = Player(health=new_health)
            field[selected] = Card()

            update_text = [
                (
                    f"{prefix}"
                    f" PLAYER took {damage} damage"
                    f" from {selected_card.display_text}!"
                    f" ({old_health} -> {new_health})"
                )
            ]

        elif (selected_card.name, target_card.name) == ("Health", "Player"):
            field["PLAYER"] = Player(
                health=field["PLAYER"].health + field[selected].health
            )
            field[selected] = Card()

            update_text = [
                (
                    f"HEALED PLAYER by {selected_card.health} HP"
                    f" ({target_card.health} -> {field[target].health})"
                )
            ]

        elif (selected_card.name, target_card.name) == ("Punch", "Champ"):
            if field[selected].punch_name != "Sucker":
                new_power = max(field[target].power - field[selected].power, 0)
                if new_power > 0:
                    field[target] = Champ(power=new_power)
                else:
                    field[target] = Card()
                suffix = (
                    f"reducing it's power by {selected_card.power}!"
                    f" ({target_card.power} -> {new_power})"
                )
            else:
                deck = deck.copy()
                deck.insert(random.randint(0, len(deck)), field[target])
                field[target] = Card()
                suffix = "sending it back into the deck!"

            field[selected] = Card()

            update_text = [
                (
                    f"PUNCHED {target_card.display_text}"
                    f" with {selected_card.display_text}, "
                    f"{suffix}"
                )
            ]

        elif (
            selected_card.name
            in [
                "Health",
                "Block",
                "Punch",
            ]
            and target_card.name in ["Health", "Block", "Punch", "Empty"]
        ):
            field[target] = field[selected]
            field[selected] = Card()

            if target_card.name != "Empty":
                suffix = f" (replaced {target_card.display_text})"
            else:
                suffix = ""

            update_text = [
                (f"MOVED {selected_card.display_text} to {target}" f"{suffix}")
            ]

        else:
            raise ValueError("Invalid move")

        if field["PLAYER"].health <= 0:
            return Game(field, deck, self.round, state="loss"), update_text

        next_round = True
        for loc in Game.UPPER_ROW:
            if field[loc].name != "Empty":
                next_round = False

        if next_round:
            if self.round == Game.NUM_ROUNDS:
                return Game(field, deck, self.round, state="win"), update_text
            else:
                for slot in Game.UPPER_ROW:
                    field[slot] = deck.pop()
                new_round = self.round + 1
                update_text.append(f"ROUND {new_round} START!")
                return Game(field, deck, new_round), update_text
        else:
            return Game(field, deck, self.round), update_text

    @staticmethod
    def h_concat(str_lists: List[List[str]], separator="\t") -> List[str]:
        return [separator.join(x) for x in zip(*str_lists)]

    def get_field_text(self) -> List[str]:
        ring_labels = [[slot.rjust(3).ljust(11)] for slot in Game.UPPER_ROW]
        ring_side = [self.field[loc].image for loc in Game.UPPER_ROW]
        player_side = [self.field[loc].image for loc in Game.LOWER_ROW]
        player_labels = [[slot.rjust(3).ljust(11)] for slot in Game.LOWER_ROW]

        return (
            Game.h_concat(ring_labels)
            + Game.h_concat(ring_side)
            + [""]
            + Game.h_concat(player_side)
            + Game.h_concat(player_labels)
        )
