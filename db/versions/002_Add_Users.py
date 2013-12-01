from sqlalchemy import *
from migrate import *

meta = MetaData()
user = Table('user', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('oauth_access_token', String(255)),
    Column('oauth_secret', String(255))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    participant = Table('participant', meta, autoload=True)
    # Create User table
    user.create()

    # Add user_id to participant
    c_user_id = Column('user_id', Integer)
    c_user_id.create(participant)

    # Remove name from participant
    participant.c.name.drop()

    # Add participant.user_id FK constraint
    fk = ForeignKeyConstraint([participant.c.user_id], [user.c.id])
    fk.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    participant = Table('participant', meta, autoload=True)
    user.drop()
    participant.c.user_id.drop()
    c_name = Column('name', String(255))
    c_name.create(participant)
    fk = ForeignKeyConstraint([participant.c.user_id], [user.c.id])
    fk.drop()
