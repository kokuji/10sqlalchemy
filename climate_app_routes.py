# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


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
        f"/api/v1.0/tobs<br/>")


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
        all_dates.append(dates_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    results_station = session.query(Station.station).all()

    all_stations = []
    for station in results_station:
        station_dict = {}
        all_stations.append(station_dict)

# Find most recent date in data set
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date a year from the last data point for date in the database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all dates
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    sel = [Measurement.date, Measurement.tobs]
    results_temp = session.query(*sel).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list
    all_temps = []
    for date, tobs in results_temp:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Temp"] = tobs
        all_temps.append(temps_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps():
    if not end:
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        TMIN, TAVG, TMAX = calc_temps('2017-07-01', '2017-07-08')[0]
    else:
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        TMIN, TAVG, TMAX = calc_temps('2017-07-01', '2017-07-08')[0]

    # Create a dictionary from the row data and append to a list
    all_calcs = []
    for TMIN, TAVG, TMAX in calc_temps:
        temps_dict = {}
        temps_dict["TMIN"] = TMIN
        temps_dict["TAVG"] = TAVG
        temps_dict["TMAX"] = TMAX
        all_temps.append(temps_dict)

    return jsonify(all_calcs)


if __name__ == "__main__":
    app.run()
