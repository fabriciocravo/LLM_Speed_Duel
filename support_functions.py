import random as rd
import json
import secrets

def load_deck_list(deck_info):
    return deck_info["main_deck"]

def load_extra_deck(deck_info):
    return deck_info["extra_deck"]

def shuffle(deck):
    rd.shuffle(deck)

def draw(deck):
    return deck.pop(-1)

def draw_multiple(deck, number_of_cards):
    cards_draw = []
    for _ in range(number_of_cards):
        cards_draw.append(draw(deck))
    return cards_draw


def encode_for_llm(data):
    """Scatter real data throughout random hex with instruction"""

    # Add instruction at the start (in hex)
    instruction = "YUGIOH_GAME_STATE: Extract data between || delimiters"
    instruction_hex = instruction.encode().hex()

    # Split data into chunks
    hand_hex = json.dumps(data['hand']).encode().hex()
    deck_hex = json.dumps(data['deck']).encode().hex()
    field_hex = json.dumps({
        'monster_field': data['monster_field'],
        'magic_field': data['magic_field'],
        'lp': data['lp']
    }).encode().hex()
    graveyard_hex = json.dumps(data['graveyard']).encode().hex()
    banished_hex = json.dumps(data['banished']).encode().hex()
    extra_hex = json.dumps(data['extra_deck']).encode().hex()

    # Generate random padding between each chunk
    pad1 = secrets.token_hex(rd.randint(50, 150))
    pad2 = secrets.token_hex(rd.randint(50, 150))
    pad3 = secrets.token_hex(rd.randint(50, 150))
    pad4 = secrets.token_hex(rd.randint(50, 150))
    pad5 = secrets.token_hex(rd.randint(50, 150))
    pad6 = secrets.token_hex(rd.randint(50, 150))
    pad7 = secrets.token_hex(rd.randint(50, 150))

    # Mix everything together with instruction at start
    return (f"{instruction_hex}||{pad1}||{hand_hex}||{pad2}||{deck_hex}||{pad3}||{field_hex}||{pad4}||{graveyard_hex}"
            f"||{pad5}||{banished_hex}||{pad6}||{extra_hex}||{pad7}")

class LLMGameState:

    def __init__(self, deck_name):
        self.lp = 4000

        base_monster_field = {'card': None, 'face_up': None, 'position': None} # or 'defense'
        self.monster_field = {'L': base_monster_field, 'M':base_monster_field, 'R':base_monster_field}
        base_magic_field = {'card': None, 'face_up': None}
        self.magic_field = {'L': base_magic_field, 'M':base_magic_field, 'R':base_magic_field}

        self.graveyard = []
        self.banished = []

        with open(deck_name, 'r') as f:
            self.deck_info = json.load(f)
        self.deck = load_deck_list(self.deck_info)
        self.extra_deck = load_extra_deck(self.deck_info)
        shuffle(self.deck)

        self.hand = draw_multiple(self.deck, 4)

    def get_llm_state(self):
        """Returns state with random padding"""
        state = {
            'lp': self.lp,
            'hand': self.hand,
            'deck': self.deck,
            'extra_deck': self.extra_deck,
            'monster_field': self.monster_field,
            'magic_field': self.magic_field,
            'graveyard': self.graveyard,
            'banished': self.banished
        }
        return encode_for_llm(state)

    def draw_from_deck(self):
        if self.deck:
            self.hand = self.hand + draw(self.deck)
            return True
        else:
            return False

    def shuffle_deck(self):
        shuffle(self.deck)
        return True

    def to_graveyard(self, card_name):
        self.graveyard = self.graveyard + [card_name]
        return True

    def to_banish(self, card_name):
        self.banished = self.banished + [card_name]
        return True

    def gain_lp(self, lp_gain):
        return self.lp_change(lp_gain)

    def remove_lp(self, lp_loss):
        return self.lp_change(lp_loss)

    def lp_change(self, lp):
        self.lp = self.lp + lp
        if self.lp > 0:
            return True
        else:
            return False