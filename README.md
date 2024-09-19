# SQLAlchemy Challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to conduct a climate analysis of the area. The following sections outline the steps needed to accomplish this task.

<hr>

## Instructions


You can clone this project to your local machine to try it yourself!


`git clone https://github.com/jroelofsz/sqlalchemy-challenge.git`


Once cloned, you may need to install some dependencies:

1. SQLAlchemy: `pip install SQLAlchemy`
2. Flask: `pip install Flask`
3. Matplotlib: `pip install matplotlib`
4. Pandas: `pip install pandas`


To view the analysis, run the `climate_analysis.ipynb`. If you would like to test the API in your environment, run the `app.py` file from the command line in your environment with the dependencies installed.

<hr>

## API Usage

This project provides five available API routes:

- **Home Page: `/`**
    - Returns available routes throughout the API.

- **Precipitation: `/api/v1.0/precipitation`**
    - Returns the last year of available precipitation data.

    Return Example:

    ```
    {
        "2016-08-24": 1.45
    }
    ```

- **Stations: `/api/v1.0/stations`**
    - Returns all station data.

    Return Example:

    ```
    [
        "USC00519397"
    ]
    ```

- **TOBS (Temperature): `/api/v1.0/tobs`**
    - Returns temperature data for the most active station (the station with the most observations) from the last 12 months.

    Return Example:
    ```
    [
        77.0
    ]   
    ```

- **Temperature Data After Start Date: `/api/v1.0/<start_date>`**
    - Returns temperature data for the most active station after the specified start date.

    Example:
    ```
    /api/v1.0/2015
    ```
    This will return the temperature data for the most active station from 2015 until the most recent date available.

    Return Example:
    ```
    [
        {
        "avg_temp": 74.90833333333333,
        "max_temp": 87.0,
        "min_temp": 58.0,
        "station": "USC00519397"
        }
    ]
    ```

- **Temperature Data Between Start Date and End Date: `/api/v1.0/<start_date>/<end_date>`**
    - Returns temperature data for the most active station between the two provided dates.

    Example:
    ```
    /api/v1.0/2015/2016
    ```
    This will return the temperature data for the most active station from 2015 to 2016.

    Return Example:
    ```
    [
        {
        "avg_temp": 75.31043956043956,
        "max_temp": 84.0,
        "min_temp": 58.0,
        "station": "USC00519397"
        }
    ]   
    ```

<hr>

## Documentation

- [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)

## References

Certain functionality was inspired by Richard Wallace. You can reference his project [here](https://github.com/Cenbull70/sqlalchemy-challenge).
