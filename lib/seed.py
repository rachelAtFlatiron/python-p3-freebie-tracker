#!/usr/bin/env python3
from faker import Faker 
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from models import Dev, Company, Freebie 
import random 

fake = Faker()

#parameter x: takes in integer for number of companies to create
#returns array of company instances created as well as their ids
def create_companies(x):
    companies = [] 
    for i in range(x):
        company = Company(name=fake.company(), founding_year=fake.year())
        session.add(company) #add individually to get back id
        session.commit()
        companies.append(company)
    return companies

#parameter x: takes in integer for number of devs to create
#returns array of dev instances created as well as their ids
def create_devs(x):
    devs = [] 
    for i in range(x):
        dev = Dev(name=fake.name())
        session.add(dev) #add individually to get back id
        session.commit() 
        devs.append(dev)
    return devs

#x: number of freebies to make, 
#companies: list of created companies WITH id,
#devs: list of created companies WITH id
def create_freebies(x, companies, devs):
    freebies = [] 
    for i in range(x):
        freebie = Freebie(item_name=fake.word(), value=random.randint(30, 100), company_id=random.choice(companies).id, dev_id=random.choice(devs).id)
        freebies.append(freebie)
    session.bulk_save_objects(freebies) #can use bulk save because we don't need IDs (yet)
    session.commit()
    return freebies #will not include IDs

if __name__ == "__main__":
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session() 

    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete() 

    companies = create_companies(5)
    devs = create_devs(10)
    freebies = create_freebies(20, companies, devs)

    #note: all session commits happen in create_model functions





