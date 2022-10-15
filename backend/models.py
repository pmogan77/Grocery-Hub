from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

accounts = Table(
   'accounts', meta, 
   Column('id', Integer, primary_key = True), 
)