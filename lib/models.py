#!/usr/bin/env python3

from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

#Questions for Company.give_freebie() and Company.oldest_company().
    #should we be passing in session?


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    #create relationshp to freebie's foreign key column
    freebies = relationship('Freebie', backref='company')
    #create relationship to devs through freebies
    devs = association_proxy('freebies', 'dev', 
                        creator=lambda dv: Freebie(dev=dv))

    ###
    def give_freebie(self, dev, item_name, value, session):
        freebie = Freebie(dev_id=dev.id, company_id=self.id, item_name=item_name, value=value)
        session.add(freebie)
        session.commit()
        return freebie #TODO: are we supposed to be saving this to the database?, is it ok freebie.id == None?

    @classmethod
    def oldest_company(self, session):
        return session.query(Company).order_by(Company.founding_year.asc()).first()
    
    def __repr__(self):
        return f'<Company id={self.id} name={self.name} founding_year={self.founding_year}>'

class Dev(Base):
    __tablename__ = 'devs'
    id = Column(Integer(), primary_key=True)
    name= Column(String())

    #create relationship to freebie's foreign key column
     #NOTE USAGE OF backref and not back populates
     #if we were to use back populates we would have to include it in Freebie()
    freebies = relationship('Freebie', backref='dev')

    #create relationship to companies through freebies
    companies = association_proxy('freebies', 'company', 
                                  creator=lambda cmpy: Freebie(company=cmpy))


    ###
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True 
        return False
    
    def give_away(self, dev, freebie):
        pass 

    def __repr__(self):
        return f'<Dev id={self.id} name={self.name}>'


#association table (the through table)
class Freebie(Base):
    __tablename__ = 'freebies'
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    #create foreign key columns 
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    ###
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'

    def __repr__(self):
        return f'<Freebie id={self.id} item_name={self.item_name}, value={self.value} dev_id={self.dev_id}, company_id={self.company_id}>'
