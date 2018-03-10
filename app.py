# Dependencies
import numpy as np

from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///static/data/belly_button_biodiversity.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Metadata = Base.classes.samples_metadata
Samples = Base.classes.samples
Otu = Base.classes.otu

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

bb_db = Flask(__name__)


#################################################
# Flask Routes
#################################################

@bb_db.route('/')
def index():
    """Return the dashboard homepage."""

    return render_template('index.html')


# List of sample names
@bb_db.route('/names')
def names():

    mapper = inspect(Samples)

    nameList = []
    for row in mapper.columns:
        nameList.append(row.name)
    del nameList[0]

    return jsonify(nameList)


# List of OTU descriptions
@bb_db.route('/otu')
def otu():

    results = session.query(Otu.lowest_taxonomic_unit_found).all()

    descriptions = list(np.ravel(results))

    return jsonify(descriptions)


# MetaData for a given sample
@bb_db.route('/metadata/<sample>')
def metadata(sample):

    sampleId = sample.split('_')

    results = session.query(Metadata).\
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
@bb_db.route('/wfreq/<sample>')
def washingFrequency(sample):

    sampleId = sample.split('_')

    results = session.query(Metadata).\
        filter(Metadata.SAMPLEID == sampleId[1]).first()

    wfeq = results.WFREQ

    return jsonify(wfeq)


@bb_db.route('/samples/<sample>')
def samples(sample):

    sel = [
            Samples.otu_id,
            getattr(Samples, sample),
            Otu.lowest_taxonomic_unit_found
          ]

    results = session.query(*sel).\
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
        'otu_ids': ids,
        'sample_values': values,
        'descriptions': descriptions
    }

    return jsonify(sampleDetails)


if __name__ == '__main__':
    bb_db.run(debug=True)
