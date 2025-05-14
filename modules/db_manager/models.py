from sqlalchemy import Table, Column, String, Boolean, DateTime, MetaData, ForeignKey

metadata = MetaData()

vehicles = Table('vehicles', metadata,
    Column('plate', String, primary_key=True),
)
blacklist = Table('blacklist', metadata,
    Column('plate', String, ForeignKey('vehicles.plate')),
)
access_rules = Table('access_rules', metadata,
    Column('plate', String, ForeignKey('vehicles.plate')),
    Column('allowed', Boolean),
)
recognition_events = Table('recognition_events', metadata,
    Column('id', String, primary_key=True),
    Column('plate', String, ForeignKey('vehicles.plate')),
    Column('ts', DateTime),
    Column('status', String),
)