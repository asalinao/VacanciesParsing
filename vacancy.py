from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(String)
    field = Column(String)
    name = Column(String)
    has_test = Column(Boolean)
    address_city = Column(String)
    alternate_url = Column(String)
    salary_from = Column(Float)
    salary_to = Column(Float)
    salary_currency = Column(String)
    published_at = Column(DateTime)
    employer_name = Column(String)
    schedule = Column(String)
    pos_level = Column(String)