from sqlalchemy import create_engine
class Location(Base):
     __tablename__ = 'Locations'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     latitude = Column(Integer)
     longitude = Column(Integer)

