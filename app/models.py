from flask_sqlalchemy import SQLAlchemy
from app.database import db
from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType
import geocoder

class Geometry(UserDefinedType):
    def get_col_spec(self):
        return "GEOMETRY"

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsGeoJson(col, type_=self)


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

  latitude = db.Column(db.Float,
                        unique=True, 
                        nullable=True)

  longitude = db.Column(db.Float,
                        unique=True, 
                        nullable=True)

  website = db.Column(db.Text,  
                      unique=False,
                      nullable=True)

  programs = relationship("Program", 
                      backref="organizations")

  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )

  def to_dict(self):

    return {
    'id': self.id,
    'name': self.name,
    'address': self.address,
    'description': self.description,
    'city': self.city,
    'state': self.state,
    'zipcode': self.zipcode,
    'phone': self.phone,
    'website': self.website,
    'last_updated': self.last_updated
    }

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

  program_type = relationship(
        "ProgramType",
        secondary='program_types',
        backref="programs")

  age_groups = relationship(
        "AgeGroups",
        secondary='program_ages',
        backref="programs")

  regions = relationship(
        "Regions",
        secondary='neighborhood_programs',
        backref="programs")


  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )

  def to_dict(self):
    return {
    'name': self.name,
    'regions': [region.to_dict() for region in self.regions],
    }

  def __repr__(self):
    return f"Program('{self.name}', '{self.description}', '{self.volunteers_needed}', '{self.open_public_school_enrollement}') , '{self.website}', , '{self.phone}', '{self.org_id}', '{self.organizations}', '{self.program_type}','{self.age_groups}','{self.regions}','{self.last_updated}')"


# location tables

class Neighborhoods(db.Model):

  __tablename__ = 'neighborhoods'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                  unique=False,
                  nullable=False)

  region_id = db.Column(db.Integer,
                    db.ForeignKey('regions.id'),
                    unique=False, 
                    nullable=False)

  SHAPE = db.Column(Geometry, nullable=False)
  
  zip_codes = relationship(
        "ZipCodes",
        secondary='neighborhood_zips',
        backref="neighborhoods")

  schools = relationship(
        "Schools",
        secondary='neighborhood_schools',
        backref="neighborhoods")

  def to_dict(self):
    geo = eval(self.SHAPE)

    return {
    'type': "Feature",
    "properties":
      {'id': self.id,
      'name': self.name,
      'region_id': self.region_id},
    'geometry': geo
    }

  def __repr__(self):
    return f"Neighborhood({self.name}','{self.regions}', '{self.SHAPE}')"

  # ???

class Regions(db.Model):

  __tablename__ = "regions"

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=True,
                    nullable=False)

  neighborhoods = relationship("Neighborhoods", 
                      backref="regions")

  def to_dict(self):
    return {
    'id': self.id,
    'name': self.name
    }

  def __repr__(self):
    return f"Region({self.name}"

class ZipCodes(db.Model):

  __tablename__ = "zip_codes"

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.Integer,
                    unique=True,
                    nullable=False)

  schools = relationship(
        "Schools",
        secondary='school_zips',
        backref="zip_codes")

  def __repr__(self):
    return f"ZipCode('{self.name}')"

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

  def __repr__(self):
    return f"School('{self.name}')"

  # ??

    # program join tables
neighborhood_programs = db.Table('neighborhood_programs',
                    db.Column('region_id', db.Integer, db.ForeignKey('regions.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
                    )

# zipcode_programs: db.Table('zipcode_programs',
#                     db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True),
#                     db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
#                     )

# schoool_programs: db.Table('schoool_programs',
#                     db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True),
#                     db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
#                     )


# join tables for locations

neighborhood_zips = db.Table('neighborhood_zips',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhoods.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True)
                    )

school_zips = db.Table('school_zips',
                    db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip_codes.id'), primary_key=True)
                    )

neighborhood_schools = db.Table('neighborhood_schools',
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

  def __repr__(self):
    return f"ProgramType('{self.name}'"

class AgeGroups(db.Model):
  __tablename__ = 'age_groups'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=False,
                    nullable=False)

  def __repr__(self):
    return f"ProgramAge('{self.name}')"



program_types = db.Table('program_types',
                    db.Column('program_iid', db.Integer, db.ForeignKey('programs.id'), primary_key=True),
                    db.Column('program_type_id', db.Integer, db.ForeignKey('program_type.id'), primary_key=True)
                    )

program_ages = db.Table('program_ages',
                    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True),
                    db.Column('program_age_id', db.Integer, db.ForeignKey('age_groups.id'), primary_key=True)
                    )
