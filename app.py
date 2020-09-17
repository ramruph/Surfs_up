#Importing Dependencies for the app
import datetime as dt
import numpy as np
import pandas as pd

#import SQLite Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Flask dependencies
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save Refrences 
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# Setting up Flask

app = Flask(__name__)
#All routes go after app = Flask(__name__) for the code to run properly

@app.route('/')

def welcome():
    return (
    ''' 
    Welcome to the Climate Analysis API! <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end <br>
    ''')

#Creating precipitation routine
@app.route('/api/v1.0/precipitation')

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


#creating station routine
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))          #unravels the data into a 1 dimensional array
    return jsonify(stations = stations)


#creating temperature observation route
@app.route('/api/v1.0/tobs')
def temp_monthly():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps=temps)