import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Setup Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#table references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Engine
session = Session(engine)

app = Flask(__name__)

# Home route
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return Dates and Precipitation from the last year."""
    #query precipitation data from last year
    session = session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    measurements_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()
    
    #save list and jsonify it
    prcp_list = [measurements_year]
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""    
    session = Session(engine)
    
    #query stations data
    stations = session.query(Station)
    
    #loop to create dictionary
    station_dictionary = []
    for station in stations:
        stations = {}
        stations["Station"] = station.station
        stations["Name"] = station.name
        station_dictionary.append(station_dict)
        
    return jsonify(station_dictionary)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query for tobs for most active station for one year"""
    session = Session(engine)
    
    measurements_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()
    
    top_tobs = []
    for measurements in measurements_year:
        temp_dictionary = {}
        temp_dictionary["date"] = measurements_year[1]
        temp_dictionary["tobs"] = measurements_year[2]
        top_tobs.append(temp_dictionary)
        
    return jsonify(top_tobs)


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    