from itertools import count
from main import Base, Session

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

deck_card_association = Table(
    'deck_card_association',
    Base.metadata,
    Column('deck_id', ForeignKey('deck.id')),
    Column('card_id', ForeignKey('card.id'))
)

class Deck(Base):
    __tablename__ = 'deck'

    id = Column(Integer, primary_key=True)
    theme = Column(String)
    card_list = relationship('Card', back_populates='deck_list', secondary=deck_card_association)

    def __repr__(self) -> str:
        return f"<Deck {self.theme}>"

class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    deck_list = relationship('Deck', back_populates='card_list', secondary=deck_card_association)

    def __repr__(self) -> str:
        return f"<Card {self.name}>"

Base.metadata.create_all()

mystical_typhoon = Card(name='Mystical Typhoon',type='Spell')
sakuretsu_armor = Card(name='Sakuretsu Armor',type='Trap')
dark_magician = Card(name='Dark Magician',type='Monster')
des_wombat = Card(name='Des Wombat', type='Monster')
rainbow_dragon = Card(name='Rainbow Dragon', type='Monster')

crystal_beasts = Deck(theme='Crystal Beasts')
yami_yugi = Deck(theme='Yami Yugi')
tyranno_hassleberry = Deck(theme='Tyranno Hassleberry')

crystal_beasts.card_list.extend([mystical_typhoon, des_wombat])
yami_yugi.card_list.extend([mystical_typhoon, sakuretsu_armor, dark_magician])
tyranno_hassleberry.card_list.extend([mystical_typhoon, sakuretsu_armor, des_wombat])

session = Session()

session.add_all([crystal_beasts, yami_yugi, tyranno_hassleberry])
session.commit()

decks = session.query(Deck)

for deck in decks:
    print(f"{deck} has {deck.card_list}")

    for card in deck.card_list:
        print(f"{card} is found in {card.deck_list}")

cards = session.query(Card)

for card in cards:
    print(f"{card} is found in {card.deck_list}")