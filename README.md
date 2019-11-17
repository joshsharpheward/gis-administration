# gis-administration
## Description
My low-budget homemade administrative tools for ArcGIS Online and Portal. 

## Installation
Python and all required packages come installed with ArcGIS Pro. As long as you run these tools from within ArcGIS Pro as they are intended to be used, there should be no additional configuration required.

While I have included all of the individual Python (.py) files, instead of creating your own script tools and having to configure their parameters you can simply download the .tbx file which has these embedded and pre-configured. 

If you would like to use these scripts from an environment other than an ArcGIS Pro script tool, you can make the following changes to do so:
1. replace the 

## Usage
All of these tools have been designed to run in ArcGIS Pro, and use the active portal in Pro to log in to the "GIS" object from the ArcGIS Api for Python, which supplies the required url and credentials. These will either fail or yield partial results depending on the user type of the account logged in - ideally they should be run from an account with 

## License
