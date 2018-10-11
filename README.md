# DocInspector

A program made to provide statistical information about google documents and their revisions

## Table of contents 
* [About DocInspector](#about)
* [Prerequisites](#prereq)
* [Installing](#install)
* [Built With](#built)
* [Flags](#flags)
* [Authors](#authors)
* [Acknowledgments](#acknowledgements)
<a name="about"></a>

## About DocInspector 

The DocInspector is a program created to obtain statistical data on changes to google documents and convert it into a form that is easy to read and understand. This can be related to user input to the google document including characters added and removed and also gives information as to which user created each edit of the document. This would be useful in an educational setting where teachers and markers need to see the contribution of each student to a google doc to ensure that the workload has been distributed evenly. Similarly, it could be used in a business setting where managers can see the productivity of each employee through the metrics provided by DocInspector.
<a name="prereq"></a>

## Prerequisites 

- Python 3.7 or later 
- Google account with access to google document
<a name="install"></a>

## Installing 

Clone DocInspector from https://git.infotech.monash.edu/FIT2101-S2-2018-Scrumbags/docInspector.git

```
$ git clone https://git.infotech.monash.edu/FIT2101-S2-2018-Scrumbags/docInspector.git
$ cd DocInspector
```

Run DocInspector.py from command line 
<a name="built"></a>

## Built With 

* [Python 3.7](https://www.python.org/downloads/release/python-370/) - Version used  
* [Google API V2](https://developers.google.com/drive/api/v2/reference/) - API used
* [google-api-python-client] (https://developers.google.com/api-client-library/python/) - Google API library
* [oauth2client] (https://developers.google.com/api-client-library/python/guide/aaa_oauth) - Google authentication library
* [httplib2] (https://pypi.org/project/httplib2/) - HTTP library 
<a name="flags"></a>

## Flags 

DocInspector uses a number of flags to which stats to retrieve and how to retrieve them 

| Flag command |   Flag name   | Description | 
| --- | --- | --- |
| -d | --dates | The start and end date range from which statistics will be extracted in the format "dd-mm-yyyy/dd-mm-yyyy". Value will default to lifespan of the document if left blank or value entered is outside of document lifespan |
| -t | --time | Time increment in which changes will be displayed in the format 'd:h:m'. Only increments that contain recognised changes will be displayed |
| -u | --unsafe | Unsafe API which will gather a larger amount of date from the same date range. Use this to gather more data for each increment of time |
| -f | --fine | Whether a finer level of detail will be used with the unsafe API. May take a while to process as large amounts of data are being retrieved |
| -c | --cache | Caches login details to prevent re-authentication. Use this to store credentials so that authentication is only prompted once |
<a name="authors"></a>

## Authors <a name="authors"></a>

* **Quinn Roberts**
* **Simon Schippl**
* **Darcy Trenfield**
* **Ganesh Ukwatta**
<a name="acknowledgements"></a>
 
## Acknowledgments 

* Robyn McNamara for being a great client

