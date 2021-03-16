#import dependencies
import pandas as pd
import numpy as np
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#setup flask
app = Flask(__name__)

#Home page and List all routes that are available.
@app.route("/")

def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start"
        f"/api/v1.0/temp/start/end")

#NO.1 Precipitation Route

@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of all Precipitation Data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").all()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitations = {date: prcp for date, prcp in results}

    # Return the JSON representation of your dictionary.
    return jsonify(precipitations)

#NO.2 Stations Route

@app.route("/api/v1.0/stations")

def stations():
    #query station data
    results = session.query(Station.station).all()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))

    # Return a JSON list of stations from the dataset.
    return jsonify(stations = stations)



#NO.3 Temperature Obervations Route

@app.route("/api/v1.0/tobs")

def temp_obs():

    # Query all stations of temperature obvervations last year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= "2016-08-24").all()

    # Unravel results into a 1D array and convert to a list
    all_tobs = list(np.ravel(results))

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(all_tobs = all_tobs)

#NO.4 start temperature Route
#NO.5 start/end temperature Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#start format yyyy-mm-dd; <start>/<end> formats when query in broswer yyyy-mm-dd/yyyy-mm-dd

def star_end(start = None, end = None):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return TMIN,TAVG,TMAX"""
    # Query all tobs
    #in case of end date is not given
    if not end: 
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    #incase of both start and end date are provided
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#run app
if __name__ == '__main__':
    app.run()
