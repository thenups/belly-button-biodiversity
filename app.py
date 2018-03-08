# Dependencies
from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# engine = create_engine("sqlite:///static/data/belly_button_biodiversity.sqlite", echo=False)
#
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)
#
# # Save reference to the table
# Metadata = Base.classes.samples_metadata
# Samples = Base.classes.samples
# Otu = Base.classes.otu
#
# # Create our session (link) from Python to the DB
# session = Session(engine)


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

@bb_db.route('/names')
def names():
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]

    """



@bb_db.route('/otu')
def otu():
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
@bb_db.route('/metadata/<sample>')
def metadata():
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """



@bb_db.route('/wfreq/<sample>')
def washingFrequency():
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """


@bb_db.route('/samples/<sample>')
def samples():
    """OTU IDs and Sample Values for a given sample.

    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]
    """

if __name__ == '__main__':
    bb_db.run(debug=True)
