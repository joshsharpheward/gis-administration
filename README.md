# gis-administration
### My homemade administrative tools for ArcGIS Online and Portal. 

## Description

Early this year I realised it was kind of difficult to manage a Portal/AGOL organisation with the tools available via the GUI. What if I wanted to change the schema of a service, but have no idea which webmaps it was consumed in and therefore what required updating? How do I easily answer questions like "which accounts in my organisation haven't been used in the last 6 months", or "where am I missing metadata on my services, webmaps and web applications". As such I went digging into the ArcGIS API for Python and have developed a number of scripts to answer these sorts of questions.

As not everyone has the time or inclination to learn Python, I also wanted these tools to be able to simple enough to be able to be run by someone with little or no experience.

### Overview of different tools
1. Find Unused Services: Searches the active portal for services (map image, feature, vector tile, and image services included) which aren't being used in any webmaps within the active portal and returns the item title and url of the item to the geoprocessing results window.
1. Metadata Report: Searches the active portal for items (excluding Code Attachments, Mobile Map Packages, Layer Templates and Mobile Applications as I didn't think these were necessary), fetches key information for the item (title, type of item, id, summary, description) and writes a csv with this information for each item. Optionally restricts the items searched to a single item owner - this is handy in situations where you just want to audit your authoritative content if it is all managed under a single admin account.
1. Search Webmaps for Service(s): Takes a service url or part of a service url as an input, then searches the active portal for webmaps and configured searches in web applications which are using that service, then returns the webmap title(s) and layer rest url(s) (tells you whether whole service used, or just individual layers) and web application title(s), layer rest url(s) and which fields the search is configured on - all to the geoprocessing results window.
1. Service Report: Searches the active portal for service items (map image, feature, vector tile, and image services included), fetches key information for the service (title, type, layers, url, access, groups shared with) then writes a csv with this information for each service item.
1. User Report: Searches the active portal for users, fetches key information for the user (username, first name, last name, email, level, role, groups, last login) where it exists and writes a csv with this information for each user.

Disclaimer: I have no background in programming and am entirely self-taught (been playing around with python for ~ 1 year). As such there may be more efficient or more pythonic ways of writing these tools.

## Installation
Python and all required packages come installed with ArcGIS Pro. As long as you run these tools from within ArcGIS Pro as they are intended to be used, there should be no additional configuration required.

While I have included all of the individual Python (.py) files, instead of creating your own script tools and having to configure their parameters you can simply download the .tbx file which has these embedded and pre-configured. 

If you would like to run these scripts from an environment other than an ArcGIS Pro script tool, you can make the following changes to do so:
1. Replace the "gis = GIS('pro')" line with another authentication method from the list here https://developers.arcgis.com/python/guide/working-with-different-authentication-schemes/
The most common and safest method being using code like this:
from getpass import getpass
portal_url = 'https://fakeurl.maps.arcgis.com/home/'
username = 'your_username'
password = getpass() # this prompts the user to input a password without echoing, better than hard-coding and storing in the python file
gis = GIS(portal_url, username, password)

2. Replace all instances of "arcpy.AddMessage()" with "print()", replacing the function but keeping the text

3. Replace all instances of "arcpy.GetParameter(x)" and "arcpy.GetParameterAsText(x)" with an appropriate input. For example, for any of the report scripts that require an output filepath as input, simply replace "output_file_path = arcpy.GetParameterAsText(0)" with "output_file_path = r'myfolder\myfile.csv'"

4. Remove "import arcpy" as there shouldn't be any other references to the package once the above changes have been made

## Usage
All of these tools have been designed to run in ArcGIS Pro, and use the active portal in Pro to log in to the "GIS" object from the ArcGIS Api for Python, which supplies the required url and credentials. These will either fail or yield partial results depending on the user type of the account logged in - ideally they should be run from an account with a "User Type" of "Administrator" as this will have full access to the contents of the portal.

The main benefit of writing these tools to run in this way is that they can be run over different organisations very easily and without requiring any changes to the python file (whereas otherwise you would have to update url, username, pw each time you wanted to run it over a different organisation). 

Inputs and outputs for each script detailed below

### Find Unused Services

input: none

example output: 

Running script Find Unused Services...

Logged into https://fakeurl.maps.arcgis.com/ as test_user

Searching webmaps in https://fakeurl.maps.arcgis.com/

The following services are not used in any webmaps in https://fakeurl.maps.arcgis.com/

test hfs not used in map | https://fakeurl.maps.arcgis.com/home/item.html?id= ~~redacted~~

Form 1 | https://fakeurl.maps.arcgis.com/home/item.html?id= ~~redacted~~

There are a total of 2 unused services in your portal

Completed script Find Unused Services...

### Metadata Report

### Search Webmaps for Service(s)
input: one or more url strings to search for - can be entire service url or slice. note: search not case sensitive

example input:

1. test

2. https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer/0

example output:

Running script Search Web Maps For Services...

Logged into https://fakeurl.maps.arcgis.com/ as test_user

Searching webmaps in https://fakeurl.maps.arcgis.com/

test webmap | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer/0

test webmap | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer/1

Search Complete
Searching webapp configured searches in https://fakeurl.maps.arcgis.com/

test webapp | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer/1 | Searching on: name, sst, ssta, hs

test webapp | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer/0 | Searching on: name, date, hs, ts_fig

Completed script Search Web Maps For Services...

### Service Report
input: output file path

example input: 

\myfolder\myfile.csv

example output: 

service name  |  service type  |  service layers  |  service url  |  sharing  |  shared groups
--- | --- | --- | --- | --- | ---
test hfs not used in map | Feature Service | test layer, test layer 2 | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_not_used_in_map/FeatureServer | private | Not shared to groups
test hfs used in map | Feature Service | test layer 3, test layer 4 | https://services9.arcgis.com/~~redacted~~/arcgis/rest/services/test_hfs_used_in_map/FeatureServer | shared | my_group 1, my_group 2



### User Report

## License
All scripts released under GNU Lesser Public License v3.0 (GPLv3)

Full details accessible here https://www.gnu.org/licenses/lgpl-3.0.en.html
