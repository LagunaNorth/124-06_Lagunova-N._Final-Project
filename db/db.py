import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, relationship, joinedload

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Market(Base):
    __tablename__ = 'markets'
    market_id = Column(Integer, primary_key=True)
    market_name = Column(String)
    companies_m = relationship('Company', back_populates='markets_c', 
                               primaryjoin="Market.market_id == Company.market")
class Business_Cat(Base):
    __tablename__ = 'business'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    companies_b = relationship('Company', back_populates='business_c',
                               primaryjoin="Business_Cat.category_id == Company.business")
class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(String, primary_key=True)
    tel = Column(String)
    email = Column(String)
    registered_as = Column(Integer)
    market = Column(Integer, ForeignKey('markets.market_id'))
    business = Column(Integer, ForeignKey('business.category_id'))
    provide_service = Column(Integer)
    customer = Column(Integer)
    markets_c = relationship('Market', back_populates='companies_m')
    business_c = relationship('Business_Cat', back_populates='companies_b')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
results = session.query(Company).select_from(Company).join(Business_Cat, 
                                                           Company.business == Business_Cat.category_id, 
                                                           isouter=True).join(Market, 
                                                                              Company.market == Market.market_id, 
                                                                              isouter=True).all()
df = pd.DataFrame([(line.company_id, line.tel, line.email, line.registered_as, line.markets_c.market_name, 
                    line.business_c.category_name, line.provide_service, line.customer) for line in results], 
                    columns=['id компании', 'телефон', 'e-mail', 'кол-во AS', 'сегмент рынка',
                    'категория бизнеса', 'предоставляет услугу','является клиентом'])

df['предоставляет услугу'] = df['предоставляет услугу'].astype(str)
df['предоставляет услугу'] = df['предоставляет услугу'].replace({'1': 'предоставляет услугу', '0': 'не предоставляет услугу'})
df['является клиентом'] = df['является клиентом'].astype(str)
df['является клиентом'] = df['является клиентом'].replace({'1':'клиент', '0':'не клиент'})

session.close()