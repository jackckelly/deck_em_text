# Deck 'Em! Text

_Deck 'Em! Text_ is a command-line re-implementation of [Frosty Pop](https://frostypop.com/)'s boxing-themed solitaire game [_Deck 'Em!_](https://apps.apple.com/app/id1387588220) for iOS.

In _Deck 'Em!_ you play as an up-and-coming boxer tasked with fighting the reigning boxing champ. With your mismatch in skills, victory is off the table; instead, your goal is to prove your worth by making it through the entire fight without being knocked out. Do you have what it takes to go the distance?

## Rules

### Cards

The game is played with a 52-card deck consisting of 4 card-types: CHAMP, PUNCH, BLOCK, and HEALTH.

CHAMP cards are attacks from the champion. Each one has a strength value from 2 to 14 that represents the damage the attack will do to the player.

BLOCK cards enable the player to defend against attacks. A block card reduces the damage taken from an attack by a fixed amount from 2 to 10, and can be re-used against further attacks. However, each attack blocked must be less than or equal to the previous attack in strength; otherwise, the block fails and the BLOCK card is destroyed. Tactically sequencing BLOCK cards is the key to survival.

PUNCH cards are special counterattacks by the player. The LUCKY and HAYMAKER cards reduce the strength of a CHAMP card, while the SUCKER card returns a CHAMP card back to the deck.

HEALTH cards heal the player by 2 to 10 HP.

### Field

The field of play consists of two rows of four card slots.

The upper row has four slots (A through D) where newly drawn cards are placed at the start of each round.

The lower row has four distinct slots players can manipulate:

- The PUNCH slot stores a PUNCH card for future use.
- The PLAYER slot represents the player and their current HP.
- The BLOCK slot holds the active BLOCK card.
- The CORNER slot holds a PUNCH, BLOCK, or HEALTH card for future use.

### Rounds

Each round consists of four new cards drawn from the deck that must be addressed by the player.

CHAMP cards must be defended against, while BLOCK, HEALTH, and PUNCH cards must be either used or stored in an appropriate slot for later.

When the four slots in the upper row are empty, the next round begins with four new cards.

### Victory

If the player reaches the end of the 12th round with 1 or more HP, they win the game. But as soon as the player's HP reaches 0, the game is over with a loss.

## Interface

The original _Deck 'Em!_ is played by dragging cards from slot to slot using the touchscreen. As _Deck 'Em! Text_ is only command-line based, it's interface is less intuitive, but still functional. The following is an example of the game in play:

    ROUND 2		DECK 44/52		RECORD 0 - 0
    A        	  B        	  C        	  D
    ┌─────────┐	┌─────────┐	┌─────────┐	┌─────────┐
    │ CHAMP   |	│ CHAMP   |	│ EMPTY   |	│ EMPTY   |
    │         │	│         │	│         │	│         │
    │   😈    │	│   😈    │	│         │	│         │
    │         │	│         │	│         │	│         │
    |       2 |	|       4 |	|         |	|         |
    └─────────┘	└─────────┘	└─────────┘	└─────────┘

    ┌─────────┐	┌─────────┐	┌─────────┐	┌─────────┐
    │ LUCKY   |	│ PLAYER  |	│ BLOCK   |	│ LUCKY   |
    │         │	│         │	│         │	│         │
    │   🥊    │	│   🙁    │	│   🙅    │	│   🥊    │
    │         │	│         │	│         │	│         │
    |       3 |	|      17 |	| 10 \ 13 |	|       3 |
    └─────────┘	└─────────┘	└─────────┘	└─────────┘
    PUNCH      	PLAYER     	BLOCK      	CORNER

    BLOCK succeeded! PLAYER took 3 damage from CHAMP 13 😈! (20 -> 17)

    (0) [A -> BLOCK]:  DEFEND against CHAMP 2 😈 with BLOCK 10 \ 13 🙅
    (1) [A -> PLAYER]:  DEFEND against CHAMP 2 😈 with PLAYER 17 🙁
    (2) [B -> BLOCK]:  DEFEND against CHAMP 4 😈 with BLOCK 10 \ 13 🙅
    (3) [B -> PLAYER]:  DEFEND against CHAMP 4 😈 with PLAYER 17 🙁
    (4) [PUNCH -> CORNER]:  MOVE LUCKY 3 🥊 to [CORNER] (LUCKY 3 🥊)
    (5) [PUNCH -> A]:  PUNCH CHAMP 2 😈 with LUCKY 3 🥊
    (6) [PUNCH -> B]:  PUNCH CHAMP 4 😈 with LUCKY 3 🥊
    (7) [BLOCK -> CORNER]:  MOVE BLOCK 10 \ 13 🙅 to [CORNER] (LUCKY 3 🥊)
    (8) [CORNER -> PUNCH]:  MOVE LUCKY 3 🥊 to [PUNCH] (LUCKY 3 🥊)
    (u) UNDO
    (q) QUIT

Every action a player can take is enumerated, and to make a move, the player enters the corresponding number into the prompt. You can also choose to quit and to undo any action made in the current round.

## Usage

To play the game, clone this repo and run it with:

     python -m deck_em
