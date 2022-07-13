from main import Base, Session

from sqlalchemy import ForeignKey, Table, Column, String, Integer
from sqlalchemy.orm import relationship

deck_card_association = Table(
    'deck_card_association',
    Base.metadata,
    Column('card_id', ForeignKey('card.id'), primary_key=True),
    Column('deck_id', ForeignKey('deck.id'), primary_key=True)
)

class Deck(Base):
    __tablename__ = 'deck'
    
    id = Column(Integer, primary_key=True)
    theme = Column(String)
    type = Column(String)
    card_list = relationship('Card', back_populates='deck_list', secondary=deck_card_association)

    def __repr__(self) -> str:
        return f"<Deck {self.name}>"

class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    effect = Column(String)
    limit = Column(Integer, default=3)
    deck_list = relationship('Deck', back_populates='card_list', secondary=deck_card_association)

    def __repr__(self) -> str:
        return f"<Card {self.name}>"

Base.metadata.create_all()

shaddoll = Deck(theme='Shaddoll', type='Combo')
exodia = Deck(theme='Exodia', type='OTK')

shekhinaga = Card(name='El Shaddoll Shekhinaga', type='Monster', effect='Deny a special summon')
construct = Card(name='El Shaddoll Construct', type='Monster', effect='Destroy special summoned monster in battle')
falco = Card(name='El Shaddoll Falco', type='Monster', effect='Flip: special summon a shaddoll from your graveyard')
dragon = Card(name='El Shaddoll Dragon', type='Monster', effect="Return an opponents card to its owner's hand")

the_forbidden_one = Card(name='Exodia the forbidden one', type='Monster', effect='autowin if you have the other 4 parts in your hand', limit=1)
left_arm = Card(name='Left arm of the forbidden one', type='Monster', limit=1)
right_arm = Card(name='Right arm of the forbidden one', type='Monster', limit=1)
left_leg = Card(name='Left leg of the forbidden one', type='Monster', limit=1)
right_leg = Card(name='Right lef of the forbidden one', type='Monster', limit=1)

shaddoll.card_list.extend([
    shekhinaga, construct, falco, dragon
])
exodia.card_list.extend([
    the_forbidden_one, left_arm, right_arm, right_leg, left_leg
])

session = Session()
session.add_all([shaddoll, exodia])
session.commit()

deck_association_subquery = session.query(
    Deck.theme, deck_card_association.c.card_id
    ).join(deck_card_association, Deck.id == deck_card_association.c.deck_id).subquery()

cards_in_decks_view = session.query(
    Card.name, deck_association_subquery.c.theme
).join(deck_association_subquery, Card.id == deck_association_subquery.c.card_id).order_by(deck_association_subquery.c.theme)

for card, deck in cards_in_decks_view:
    print(f"{card} in {deck}")