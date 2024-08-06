# Import the dependencies.

import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
meas = Base.classes.measurement
stat = Base.classes.station


# Create our session (link) from Python to the DB

# session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1> Available Routes for Hawaii Data Analysis:</h1><br/>"
        f"<h2> Available Information Routes: </h2><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and date data"""
  
    precip_results = session.query(meas.prcp, meas.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip data
    precip_data = []
    for prcp, date in precip_results:
        precip_dict = {}
        precip_dict["precipitation"] = prcp
        precip_dict["date"] = date
        
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data"""
  
    station_results = session.query(stat.station, stat.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip data
    station_data = []
    for station, name in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs data for most active, last year"""
    most_active = session.query(meas.station,func.count(meas.station)).order_by(func.count(meas.station).desc()).group_by(meas.station).all()
    mas = most_active[0][0]

    # mas_start = "2016-08-18"

    tobs_results = session.query(meas.date, meas.tobs).filter(meas.station == mas).filter(meas.date > "2016-08-18").group_by(meas.date).order_by(meas.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip data
    tobs_data = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

if __name__ == '__main__':
    app.run(debug=True)