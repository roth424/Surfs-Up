
# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
#import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool


engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread':False},
   poolclass=StaticPool)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our connection object
session = Session(engine)

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
        "Available Routes:<br/>" +
        "/api/v1.0/precipitation<br/>"+
        "api/v1.0/stations<br/>"+
        "/api/v1.0/tobs<br/>"+
        "/api/v1.0/<start><br/>"+
        "/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def date():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value."""
    # Query precipitation
    results = session.query(Measurement.prcp).all()

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Measurement.stations).group_by(Measurement.stations).all()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def temp():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    engine.execute('SELECT date, tobs FROM Measurement ORDER BY date DESC').fetchall()

    date = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= date).all()
    results

    return jsonify(results)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def times():
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    

if __name__ == '__main__':
    app.run(debug=True)
