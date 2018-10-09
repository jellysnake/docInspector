# DocInspector

A program made to provide statistical information about google documents and their revisions


### Prerequisites

- Python 3.7 or later 
- Google account with access to google document


### Installing

Clone DocInspector from https://git.infotech.monash.edu/FIT2101-S2-2018-Scrumbags/docInspector.git

```
$ git clone https://git.infotech.monash.edu/FIT2101-S2-2018-Scrumbags/docInspector.git
$ cd DocInspector
```

Run DocInspector.py from command line 


## Built With

* [Python 3.7](https://www.python.org/downloads/release/python-370/) - Version used  
* [Google API V2](https://developers.google.com/drive/api/v2/reference/) - API used
* ADD LIBRARIES HERE 


| Flag name | Description | 
| --- | --- |
| fileId | A valid google document ID from which revision data will be retrieved |
| -d | The start and end date range from which statistics will be extracted in the format "dd-mm-yyyy/dd-mm-yyyy". Ensure that start and end date are within the range of the documents lifespan |
| -t | Time increment in which changes will be displayed in the format 'd:h:m'. Only increments that contain recognised changes will be displayed |
| -u | Unsafe API which will gather a larger amount of date from the same date range. Use this to gather more data for each increment of time |
| -f | Whether a finer level of detail will be used with the unsafe API|



## Authors

* **Quinn Roberts**
* **Simon Schippl**
* **Darcy Trenfield**
* **Ganesh Ukwatta**

 
## Acknowledgments

* Robyn McNamara for being a great client

