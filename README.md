# LibertyGlobalProject1
This project consists of two tasks:

## MetaWeatherAPI
This task implements a service that receives weather data from https://www.metaweather.com/ for St. Petersburg over the past month

### Prerequisites
All the necessary libraries are in the requirements.txt file.

### Getting Started
To use this service (instructions for Ubuntu 18.04), in the project folder, enter the following:
```
$ sudo docker-compose up -d
$ python3 app.py
```
### Usage
```
http://127.0.0.1:5000/weather/2019-01-02  # returns data for the specified date
```

## TestClassPerson
This task tests the Person class with pytest, finding bugs in it.
