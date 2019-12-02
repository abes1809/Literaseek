from flask import Flask, cli
import click
from app.database import db
from app.models import Organization

import geocoder

@click.command('update_lat_lon')
@cli.with_appcontext
def update_lat_lon():

	all_organizations = Organization.query.all()

	for organization in all_organizations: 

		full_address = organization.address + ", " + organization.city + ", " + organization.state + ", " + organization.zipcode

		latlong = geocoder.osm(full_address).json

		print(latlong)

		latitude = latlong['lat']

		longitude = latlong['lng']

		organization.latitude = latitude

		organization.longitude = longitude

		print(organization.name)
		print(organization.latitude)
		print(organization.longitude)

		db.session.commit()

	return all_organizations