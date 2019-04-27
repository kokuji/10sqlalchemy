# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index (home) route
@app.route("/")
def home():
    return (
        f"Welcome to the Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end")


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Get the date and corresponding precipitation level or a 404 if not."""
    # Query all dates
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.prcp]
    last_twelve_months = session.query(*sel).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list
    all_prcp = []
    for date, prcp in last_twelve_months:
        dates_dict = {}
        dates_dict["Date"] = date
        dates_dict["Prcp"] = prcp
        all_prcp.append(dates_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    results_station = session.query(Station.station).all()

    all_stations = []
    # for station in results_station:
    #     station_dict = {}
    #     all_stations.append(station_dict)

    return jsonify(results_station)

# Find most recent date in data set

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all dates
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.tobs]
    highest_tobs = session.query(*sel).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date > query_date).all()

    # Create a dictionary from the row data and append to a list
    all_temps = []
    for date, tobs in highest_tobs:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Temp"] = tobs
        all_temps.append(temps_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def calc_temps(start = None, end = None):
    if not end:
        results_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        
    else:
        results_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        

    # Create a dictionary from the row data and append to a list
    temps = list(np.ravel(results_temp))

    return jsonify(temps)


if __name__ == "__main__":
    app.run()
