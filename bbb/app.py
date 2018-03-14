#################################################
# Dependencies
#################################################
import numpy as np

from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect

import os
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Assign databse URL to app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///static/data/belly_button_biodiversity.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create our session (link) from Python to the DB
engine = create_engine('sqlite:///static/data/belly_button_biodiversity.sqlite')

# Create SQLAlchemy object
db = SQLAlchemy(app)

#################################################
# Database Setup
#################################################
# Reflect tables
db.reflect()

class Metadata(db.Model):
    __tablename__ = 'samples_metadata'

class Samples(db.Model):
    __tablename__ = 'samples'

class Otu(db.Model):
    __tablename__ = 'otu'


#################################################
# Flask Routes
#################################################
# Full dashboard
@app.route('/')
def index():
    """Return the dashboard homepage."""

    return render_template('index.html')


# List of sample names
@app.route('/names')
def names():

    mapper = inspect(Samples)

    nameList = []
    for row in mapper.columns:
        nameList.append(row.name)
    del nameList[0]

    return jsonify(nameList)


# List of OTU descriptions
@app.route('/otu')
def otu():

    results = db.session.query(Otu.lowest_taxonomic_unit_found).all()

    descriptions = list(np.ravel(results))

    return jsonify(descriptions)


# MetaData for a given sample
@app.route('/metadata/<sample>')
def metadata(sample):

    sampleId = sample.split('_')

    results = db.session.query(Metadata).\
        filter(Metadata.SAMPLEID == sampleId[1]).first()

    filteredResults = {
        'AGE': results.AGE,
        'BBTYPE': results.BBTYPE,
        'ETHNICITY': results.ETHNICITY,
        'GENDER': results.GENDER,
        'LOCATION': results.LOCATION,
        'SAMPLEID': results.SAMPLEID
        }

    return jsonify(filteredResults)


# Weekly Washing Frequency as a number
@app.route('/wfreq/<sample>')
def washingFrequency(sample):

    sampleId = sample.split('_')

    results = db.session.query(Metadata).\
        filter(Metadata.SAMPLEID == sampleId[1]).first()

    wfeq = results.WFREQ

    return jsonify(wfeq)


@app.route('/samples/<sample>')
def samples(sample):

    sel = [
            Samples.otu_id,
            getattr(Samples, sample),
            Otu.lowest_taxonomic_unit_found
          ]

    results = db.session.query(*sel).\
        join(Otu, Samples.otu_id==Otu.otu_id).\
        order_by(getattr(Samples, sample).desc()).all()

    ids = []
    values = []
    descriptions = []
    i=0
    while i<len(results):
        ids.append(results[i][0])
        values.append(results[i][1])
        descriptions.append(results[i][2])
        i += 1

    sampleDetails = {
        'id': sample,
        'otu_ids': ids,
        'sample_values': values,
        'descriptions': descriptions
    }

    return jsonify(sampleDetails)


if __name__ == '__main__':
    app.run(debug=True)
