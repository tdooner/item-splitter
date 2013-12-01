from sqlalchemy import *
from migrate import *

meta = MetaData()

auction = Table('auction', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('total_bid', String(255))
)

bid = Table('bid', meta,
    Column('id', Integer, primary_key=True),
    Column('amount', Integer),
    Column('item_id', Integer),
    Column('participant_id', Integer))

item = Table('item', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('auction_id', Integer))

participant = Table('participant', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('auction_id', Integer))

fks = [
    ForeignKeyConstraint([bid.c.item_id], [item.c.id]),
    ForeignKeyConstraint([bid.c.participant_id], [participant.c.id]),
    ForeignKeyConstraint([item.c.auction_id], [auction.c.id]),
    ForeignKeyConstraint([participant.c.auction_id], [auction.c.id]),
]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    auction.create()
    bid.create()
    item.create()
    participant.create()
    for fk in fks:
        fk.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    auction.drop()
    bid.drop()
    item.drop()
    participant.drop()
    for fk in fks:
        fk.drop()
