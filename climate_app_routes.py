# 1. import Flask
from flask import Flask, jsonify



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


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Get the date and corresponding precipitation level or a 404 if not."""
    # Query all dates
    results_prcp = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_dates = []
    for date, prcp in results_prcp:
        dates_dict = {}
        dates_dict["Date"] = date
        dates_dict["Prcp"] = prcp
        all_dates.append(dates_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def station():
    

# Find most recent date in data set
session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date a year from the last data point for date in the database
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print("Query Date: ", query_date)

@app.route("/api/v1.0/tobs")
def tobs():
    """Get the date and corresponding precipitation level or a 404 if not."""
    # Query all dates
    results_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > query_date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_temps = []
    for date, prcp in results_prcp:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Temp"] = tobs
        all_temps.append(dates_dict)

    return jsonify(all_dates)

@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)


if __name__ == "__main__":
    app.run(debug=True)
