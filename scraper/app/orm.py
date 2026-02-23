import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, BigInteger, Text, Numeric, Integer, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path)


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://scraper_agent:D7Apd9MCSf3C@localhost:5432/carstest"


Base = declarative_base()

class Car(Base):
    __tablename__ = 'cars'

    id = Column(BigInteger, primary_key=True)
    url = Column(Text, nullable=False, unique=True)
    title = Column(Text)
    price_usd = Column(Numeric(12,2))
    odometer = Column(BigInteger)
    username = Column(Text)
    phone_number = Column(BigInteger)
    image_url = Column(Text)
    images_count = Column(Integer)
    car_number = Column(Text)
    car_vin = Column(Text)
    datetime_found = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_url', 'url'),
        Index('idx_cars_title', 'title'),
        Index('idx_cars_vin', 'car_vin'),
        Index('idx_phone', 'phone_number'),
    )

class ORM:
    def __init__(self, db_url=DB_URL):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, url: str):
        session = self.Session()
        car = Car(url=url)
        session.add(car)
        try:
            session.commit()
            session.refresh(car)
            print(f"Inserted car: id={car.id}, url={car.url}")
            return car
        except Exception as e:
            session.rollback()
            print(f"Insert failed: {e}")
            return None
        finally:
            session.close()


    def get_pending_listings(self, batch_size = 100):
        session = self.Session()

        records = (
            session.query(Car)
            .filter(Car.title == None)
            .order_by(Car.id)
            .limit(batch_size)
            .all()
        )
        session.close()
        return records

    def find(self, **conditions):
        session = self.Session()
        query = session.query(Car)
        for attr, vallue in conditions.items(): 
            query = query.filter(getattr(Car, attr) == vallue)
        results = query.all()
        session.close()
        return results
    
    def delete(self, **conditions):
        session = self.Session()
        query = session.query(Car)
        for attr, vallue in conditions.items(): 
            query = query.filter(getattr(Car, attr) == vallue)
        deleted_count = query.delete(synchronize_session=False)
        session.commit()
        session.close()
        return deleted_count
    
    def update(self, url:str, data:dict):
        session = self.Session()
        try:
            updated = (
                session.query(Car)
                .filter(Car.url == url)
                .update(data, synchronize_session=False)
            )
            session.commit()
            return updated
        except Exception as e:
            session.rollback()
            print(f"Update error: {e}")
            return 0
        finally:
            session.close()

