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
        f"<h1> Available Routes for Hawaii Data Analysis</h1><br/>"
        f"<h2> Available Static Information Routes: </h2><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<h2> Available Dynamic Information Routes: </h2><br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
        f"<h2> Important Notes </h2><br/>"
        f"Dates must be input in the following format: yyyy-mm-dd<br/>"
        f"Date ranges must be input in the following format: yyyy-mm-dd_yyyy-mm-dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and date data"""
  
    precip_results = session.query(meas.date, meas.prcp).filter(meas.date > "2016-08-23").order_by(meas.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precip data
    precip_data = []
    for date, prcp in precip_results:
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
  
    station_results = session.query(stat.station, stat.name).order_by(stat.station).all()

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

@app.route("/api/v1.0/<start>")
def input_start(start):
    end = "2017-08-23"
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, max temp given a start date"""

    start_results = session.query(func.min(meas.tobs), func.max(meas.tobs), func.avg(meas.tobs)).filter(meas.date >= start).filter(meas.date <=end).all()

    session.close()

    start_data = []
    for min, max, avg in start_results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max 
        start_dict["avg"] = avg
        start_data.append(start_dict)

    return jsonify(start_data)
    
@app.route("/api/v1.0/<start>_<end>")
def input_startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, max temp given a start date"""

    startend_results = session.query(func.min(meas.tobs), func.max(meas.tobs), func.avg(meas.tobs)).filter(meas.date >= start).filter(meas.date <=end).all()

    session.close()

    startend_data = []
    for min, max, avg in startend_results:
        startend_dict = {}
        startend_dict["min"] = min
        startend_dict["max"] = max 
        startend_dict["avg"] = avg
        startend_data.append(startend_dict)

    return jsonify(startend_data)

if __name__ == '__main__':
    app.run(debug=True)