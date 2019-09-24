from . import db
import enum
from datetime import date

class Organization(db.Model):

  __tablename__ = 'organizations'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80)
                    unique=True, 
                    nullable=False)

  description = db.Column(db.Text,
                    unique=False, 
                    nullable=False)

  address = db.Column(db.String(120),
                      unique=False,
                      nullable=True)

  phone = db.Column(db.String(80)
                    unique=False,
                    nullable=True)

  website = db.Column(db.Text,  
                      unique=False,
                      nullable=True)

  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )


class ProgramAge(enum.Enum):
  prek_0_3 = 1
  prek_3_5 = 2
  grades_K_8 = 3
  grades_9_12 = 4
  adult = 5


class ProgramType(db.Model):
  __tablename__ = 'program_types'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                    unique=False,
                    nullable=False)

  ages = db.Column(db.Enum(ProgramAge),
                    unique=False,
                    nullable=False)

  open_public_school_enrollement =  db.Column(db.Boolean,
                                                unique=False,
                                                nullable=False)
  
  last_updated = db.Column(db.DateTime,
                            nullable=False,
                            default=date.today(),
                            )


class Program(db.Model):

  __tablename__ = 'programs'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80)
                    unique=True, 
                    nullable=False)

  description = db.Column(db.text(120),
                      unique=False,
                      nullable=True)

  volunteers_needed = db.Column(db.Boolean,
                    unique=False,
                    nullable=False)

  website = db.column(db.Text,  
                      unique=False,
                      nullable=True)

  phone = db.Column(db.String(80)
                    unique=False,
                    nullable=True)

  type_id = db.Column(db.Integer,
                    db.ForeignKey('program_type.id'),
                    unique=True, 
                    nullable=False)

  org_id = db.Column(db.Integer,
                    db.ForeignKey('organization.id'),
                    unique=True, 
                    nullable=False)

  # program join tables
neighborhood_programs: db.Table('neighborhood_programs',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhood.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('program.id'), primary_key=True)
                    )

zipcode_programs: db.Table('zipcode_programs',
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('program.id'), primary_key=True)
                    )

schoool_programs: db.Table('schoool_programs',
                    db.Column('school_id', db.Integer, db.ForeignKey('school.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey('program.id'), primary_key=True)
                    )


# location tables

class Neighborhoods(db.Model):

  __tablename__ = 'neighborhoods'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(80),
                  unique=False,
                  nullable=False)

  # ???

class ZipCodes(db.Model):

  __tablename__ = "zip_codes"

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.Integer,
                    unique=True,
                    nullable=False)

  # ??

class Schools(db.Model):

  __tablename__ = 'schools'

  id = db.Column(db.Integer,
                  primary_key=True)

  name = db.Column(db.String(200),
                    unique=True,
                    nullable=False)

  # ??

# join tables for locations

neighborhood_zips: db.Table('neighborhood_zips',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhood.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip.id'), primary_key=True)
                    )

school_zips: db.Table('school_zips',
                    db.Column('school_id', db.Integer, db.ForeignKey('school.id'), primary_key=True),
                    db.Column('zip_id', db.Integer, db.ForeignKey('zip.id'), primary_key=True)
                    )

neighborhood_schools: db.Table('neighborhood_schools',
                    db.Column('neighborhood_id', db.Integer, db.ForeignKey('neighborhood.id'), primary_key=True),
                    db.Column('school_id', db.Integer, db.ForeignKey('school.id'), primary_key=True)
                    )


