from flask_sqlalchemy import SQLAlchemy
from app.database import db
from datetime import date
from sqlalchemy.orm import relationship

class Organization(db.Model):

  __tablename__ = 'organizations'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=True, 
                    nullable=False)

  description = db.Column(db.Text,
                    unique=False, 
                    nullable=False)

  address = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  city = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  state = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  zipcode = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  phone = db.Column(db.String(80),
                    unique=False,
                    nullable=True)

  website = db.Column(db.Text,  
                      unique=False,
                      nullable=True)

  programs = relationship("Program", 
                      back_populates="organizations")

  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )
  def __repr__(self):
    return f"Organization('{self.name}', '{self.description}', '{self.address}', '{self.website}', '{self.phone}', '{self.programs}', '{self.last_updated}')"



class Program(db.Model):

  __tablename__ = 'programs'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=True, 
                    nullable=False)

  description = db.Column(db.Text,
                      unique=False,
                      nullable=True)

  volunteers_needed = db.Column(db.Boolean,
                    unique=False,
                    nullable=False)

  open_public_school_enrollement =  db.Column(db.Boolean,
                                              unique=False,
                                              nullable=False)

  website = db.Column(db.Text,  
                      unique=False,
                      nullable=True)

  phone = db.Column(db.String(80),
                    unique=False,
                    nullable=True)

  org_id = db.Column(db.Integer,
                    db.ForeignKey('organizations.id'),
                    unique=False, 
                    nullable=False)

  organizations = relationship("Organization", 
                      back_populates="programs")

  program_type = relationship(
        "ProgramType",
        secondary='program_types',
        back_populates="programs")

  age_groups = relationship(
        "AgeGroups",
        secondary='program_ages',
        back_populates="programs")

  neighborhoods = relationship(
        "Neighborhoods",
        secondary='neighborhood_programs',
        back_populates="programs")

  zip_codes = relationship(
        "ZipCodes",
        secondary='zipcode_programs',
        back_populates="programs")

  schools = relationship(
        "Schools",
        secondary='schoool_programs',
        back_populates="programs")

  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )

  def __repr__(self):
    return f"Program('{self.name}', '{self.description}', '{self.volunteers_needed}', '{self.open_public_school_enrollement}') , '{self.website}', , '{self.phone}', '{self.org_id}', '{self.organizations}', '{self.program_type}','{self.age_groups}','{self.neighborhoods}','{self.zip_codes}','{self.schools}','{self.last_updated}'"


# location tables

class Neighborhoods(db.Model):

  __tablename__ = 'neighborhoods'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                  unique=False,
                  nullable=False)

  programs = relationship(
        "Program",
        secondary='neighborhood_programs',
        back_populates="neighborhoods")

  zip_codes = relationship(
        "ZipCodes",
        secondary='neighborhood_zips',
        back_populates="neighborhoods")

  schools = relationship(
        "Schools",
        secondary='neighborhood_schools',
        back_populates="neighborhoods")

  def __repr__(self):
    return f"Neighborhood({self.name}','{self.programs}','{self.zip_codes}','{self.schools}')"

  # ???

class ZipCodes(db.Model):

  __tablename__ = "zip_codes"

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.Integer,
                    unique=True,
                    nullable=False)

  programs = relationship(
        "Program",
        secondary='zipcode_programs',
        back_populates="zip_codes")

  neighborhoods = relationship(
        "Neighborhoods",
        secondary='neighborhood_zips',
        back_populates="zip_codes")

  schools = relationship(
        "Schools",
        secondary='school_zips',
        back_populates="zip_codes")

  def __repr__(self):
    return f"ZipCode('{self.name}','{self.programs}','{self.neighborhoods}','{self.schools}'"

  # ??

class Schools(db.Model):

  __tablename__ = 'schools'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(200),
                    unique=True,
                    nullable=False)

  grade = db.Column(db.String(80),
                    unique=False,
                    nullable=False)

  address = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  type = db.Column(db.String(80),
                    unique=False,
                    nullable=False)

  programs = relationship(
        "Program",
        secondary='schoool_programs',
        back_populates="schools")

  neighborhoods = relationship(
        "Neighborhoods",
        secondary='neighborhood_schools',
        back_populates="schools")

  zip_codes = relationship(
        "ZipCodes",
        secondary='school_zips',
        back_populates="schools")

  def __repr__(self):
    return f"School('{self.name}','{self.programs}','{self.neighborhoods}','{self.zip_codes}'"

  # ??

    # program join tables
neighborhood_programs: db.Table('neighborhood_programs',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhoods.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
                    )

zipcode_programs: db.Table('zipcode_programs',
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
                    )

schoool_programs: db.Table('schoool_programs',
                    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
                    )


# join tables for locations

neighborhood_zips: db.Table('neighborhood_zips',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhoods.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True)
                    )

school_zips: db.Table('school_zips',
                    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True)
                    )

neighborhood_schools: db.Table('neighborhood_schools',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhoods.id'), primary_key=True),
                    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True)
                    )

# program type and age tables


class ProgramType(db.Model):
  __tablename__ = 'program_type'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=False,
                    nullable=False)
  programs = relationship(
        "Program",
        secondary='program_types',
        back_populates="program_type")

  def __repr__(self):
    return f"ProgramType('{self.name}','{self.programs}'"

class AgeGroups(db.Model):
  __tablename__ = 'age_groups'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=False,
                    nullable=False)

  programs = relationship(
        "Program",
        secondary='program_ages',
        back_populates="age_groups")

  def __repr__(self):
    return f"ProgramAge('{self.name}','{self.programs}'"



program_types = db.Table('program_types',
                    db.Column('program_iid', db.Integer, db.ForeignKey('programs.id'), primary_key=True),
                    db.Column('program_type_id', db.Integer, db.ForeignKey('program_type.id'), primary_key=True)
                    )

program_ages = db.Table('program_ages',
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True),
                    db.Column('program_age_id', db.Integer, db.ForeignKey('age_groups.id'), primary_key=True)
                    )
