# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#home route
@app.route('/')
def home():
    return """
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/&lt;start_date&gt;<br>
    /api/v1.0/&lt;start_date&gt/&lt;end_date&gt;
    """

#route that returns precipitation data for last year
@app.route('/api/v1.0/precipitation')
def precipitation():
    #get most recent date from data
    mostRecentDate = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()[0]
        
    #set the query date to 365 days before the mostRecentDate
    queryDate = dt.datetime.strptime(mostRecentDate, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #get all the precipitation data in the last year
    precipitationData = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= queryDate).all()
    
    #convert into a dictionary for JSON
    precipitationDict = {date: prcp for date, prcp in precipitationData}
    
    #return the JSON
    return jsonify(precipitationDict)

#route that returns all stations
@app.route('/api/v1.0/stations')
def stations():
    #get all the stations
    stations = session.query(Station.station).all()
    
    #convert into a list with Numpy
    stationList = list(np.ravel(stations))
    
    #return JSON
    return jsonify(stationList)

#route that returns tobs data for most active station
@app.route('/api/v1.0/tobs')
def tobs():
    #set fields for selection
    fields = [Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    #find the most active station by count of observations
    mostActiveStation = session.query(*fields).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
        
    #store the station ID in a variable
    stationId = mostActiveStation[0]
    
    #get the most recent date in the data
    mostRecentDate = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()[0]
        
    #set the query date to 365 - highest date available
    queryDate = dt.datetime.strptime(mostRecentDate, '%Y-%m-%d') - dt.timedelta(days=365)
    
    #query the data for the tobs for mostActiveStation
    data = session.query(Measurement.tobs).\
        filter(Measurement.station == stationId).\
        filter(Measurement.date >= queryDate).all()
        
    #convert into list with Numpy
    tobsList = list(np.ravel(data))
    
    #return JSON
    return jsonify(tobsList)

@app.route('/api/v1.0/<start_date>')
def dynamicTobs(start_date):
    """_summary_
        This function will take in a start_date and return the Min, Avg, and Max tobs data for the most active station in that time period.

    Args:
        start_date (date): Date to start pulling in data after

    Returns:
        jsonify(tobsData): JSON data of Station, Min, Avg, and Max tobs
    """
    #set fields for selection
    fields = [Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    #find the most active station by count of observations
    mostActiveStation = session.query(*fields).\
        group_by(Measurement.station).\
        filter(Measurement.date >= start_date).\
        order_by(func.count(Measurement.station).desc()).first()
        
    #store the station ID in a variable
    stationId = mostActiveStation[0]
    
    #query data for Min, Avg, and Max tobs for most active station to date using <start_date> param
    query = session.query(Measurement.station,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.station == stationId).all()
    
    
    #create a dictionary:
    tobsData = []
    for station, min, avg, max in query:
        #insert values in dictionary
        tempDict = {
            "station":station,
            "min_temp":min,
            "avg_temp":avg,
            "max_temp":max
        }
        #append dictionary to list
        tobsData.append(tempDict)
    
    #return JSON
    return jsonify(tobsData)

@app.route('/api/v1.0/<start_date>/<end_date>')
def dynamicTobsTwoDates(start_date, end_date):
    """_summary_
        This function takes in 2 dates. start_date and end_date. It will return the Min, Avg, and Max temp for the most active station during that time period.

    Args:
        start_date (date): Start date for data return
        end_date (date): End date for data return

    Returns:
        jsonify(tobsData): Returns in JSON format the Station, Min Temp, Avg Temp, and Max Temp
    """
      #set fields for selection
    fields = [Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    #find the most active station by count of observations
    mostActiveStation = session.query(*fields).\
        group_by(Measurement.station).\
        filter(Measurement.date >= start_date).\
        order_by(func.count(Measurement.station).desc()).first()
        
    #store the station ID in a variable
    stationId = mostActiveStation[0]
    
    #query the data
    query = session.query(Measurement.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date, Measurement.station == stationId).\
        all()
    
    tobsData = []
    for station, min, avg, max in query:
        tempDict = {
            "station":station,
            "min_temp":min,
            "avg_temp":avg,
            "max_temp":max
        }
        tobsData.append(tempDict)
    return jsonify(tobsData)
    
#################################################
# Run Flask App
#################################################
if __name__ == '__main__':
    app.run(debug=True)