# DocInspector
A program made to provide statistical information about google documents and their revisions

## Table of contents 
* [About DocInspector](#about-docinspector)
* [Prerequisites](#prerequisites)
* [Usage](#Usage)
* [Built With](#built-with)
* [Flags](#flags)
* [Credits](#Credits)
* [Acknowledgments](#acknowledgments)

## About DocInspector 
The DocInspector is a program created to obtain statistical data on changes to google documents and convert it into a form that is easy to read and understand. This can be related to user input to the google document including characters added and removed and also gives information as to which user created each edit of the document. This would be useful in an educational setting where teachers and markers need to see the contribution of each student to a google doc to ensure that the workload has been distributed evenly. Similarly, it could be used in a business setting where managers can see the productivity of each employee through the metrics provided by DocInspector.

## Prerequisites 
- Python 3.7 or later 
- Google account with access to google document

## Usage
Unfortunately due to changes on google's end, until this app is verified it should only be used by people who are intending on developing it.

See the [Dev Setup](#dev-setup) section below on what to do in order to set this up in a dev environment.

1. Clone this repository.
2. Install the pip package.
3. Simply use `DocInspector` on the terminal and pass in the flags as desired.
4. Profit!

```bash
$ git clone https://github.com/jellysnake/docInspector.git docInspector
$ cd docInspector
$ pip install .
```

## Dev Setup
The dev setup consists of two main parts.
1. Creating the credentials and authorizing the application
2. Downloading the code and setting up the dev environment

If you have any difficulties with the dev setup then feel free to open an issue or email me on my gmail address `iamajellysnake`


### Obtaining Credentials
In order to develop with this application, you will need to obtain your own credentials from the google cloud console. This is because this project is not verified by google currently (process is ongoing) and hence will error when used with some flags that require more permissive scopes

Firstly, create an new project in the [Google Cloud Console](https://cloud.google.com/resource-manager/docs/creating-managing-projects). Then you need to [setup the project to work with oAuth 2](https://developers.google.com/identity/protocols/OAuth2UserAgent).  
This new project should enable the [Google Drive API](https://console.developers.google.com/apis/library/drive.googleapis.com?id=e44a1596-da14-427c-9b36-5eb6acce3775) and request the `https://www.googleapis.com/auth/drive` and `https://www.googleapis.com/auth/drive.metadata.readonly` scopes.  

You will see a warning about the app being unverified. This is fine to ignore because you are only developing the application.  
It does mean that you can only make requests to documents you have access to _on the same account you made the project under_.

### Dev Environment
This step is actually very easy and hardly worth it's own section.  
Because of how python works, all you need to do is add the `-e` flag to the pip install step of the usage section.
```bash
$ pip install . -e
```

## Flags 
DocInspector uses a number of flags to which stats to retrieve and how to retrieve them 

| Flag command |   Flag name   | Description | 
| --- | --- | --- |
| -d | --dates | The start and end date range from which statistics will be extracted in the format "dd-mm-yyyy/dd-mm-yyyy". Value will default to lifespan of the document if left blank or value entered is outside of document lifespan |
| -t | --time | Time increment in which changes will be displayed in the format 'd:h:m'. Only increments that contain recognised changes will be displayed |
| -u | --unsafe | Unsafe API which will gather a larger amount of date from the same date range. Use this to gather more data for each increment of time |
| -f | --fine | Whether a finer level of detail will be used with the unsafe API. May take a while to process as large amounts of data are being retrieved |
| -c | --cache | Caches login details to prevent re-authentication. Use this to store credentials so that authentication is only prompted once |

## Built With 
* [Python 3.7](https://www.python.org/downloads/release/python-370/) - Version used  
* [Google API V2](https://developers.google.com/drive/api/v2/reference/) - API used
* [google-api-python-client](https://developers.google.com/api-client-library/python/) - Google API library
* [oauth2client](https://developers.google.com/api-client-library/python/guide/aaa_oauth) - Google authentication library
* [httplib2](https://pypi.org/project/httplib2/) - HTTP library 

## Credits
**Current Maintainer**
* *Quinn Roberts*

**Initial Version**
* *Quinn Roberts*
* *Simon Schippl*
* *Darcy Trenfield*
* *Ganesh Ukwatta*
 
## Acknowledgments 
* Robyn McNamara of Monash Univeristy, the initial  client

