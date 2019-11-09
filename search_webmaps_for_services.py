# ---------------------------------------------------------------------------------
# scans Web Maps and Web Mapping Applications in an ArcGIS Online organisation
# or an ArcGIS Enterprise Portal for an input service or services. Currently only scans Web
# Mapping Applications for if they have a search configured against the input service.
# returns the name of the Web Map and the Web Mapping Application as well the layer url (matching
# with the input service(s), and for Web Mapping Applications the field the search is configured against
#
# runs over the currently active portal in ArcGIS Pro
#
# (C) 2019 Joshua Sharp-Heward, Whangarei, New Zealand
# released under GNU Lesser Public License v3.0 (GPLv3)
# email jsh726@uowmail.edu.au
# linkedin https://www.linkedin.com/in/joshua-sharp-heward-89b129131/
# ---------------------------------------------------------------------------------

from arcgis.gis import GIS
from arcgis.mapping import WebMap
import arcpy

# sign into the active portal of the ArcGIS Pro Project this script is run from
gis = GIS('pro')

def main():
    # signs into the active portal of the ArcGIS Pro Project this script is run from

    arcpy.AddMessage("Logged into {} as {}".format(arcpy.GetActivePortalURL(), gis.properties['user']['username']))

    # creates variable for user input services
    services = arcpy.GetParameter(0)

    # inputs services to web map search function
    wm_search(services)

    # inputs services to app search function
    app_search(services)

# returns Web Map title and url where the input service matches a layer
def wm_search(services):
    arcpy.AddMessage('Searching' + ' webmaps in ' + arcpy.GetActivePortalURL())
    web_maps = gis.content.search(query="", item_type="Web Map", max_items=10000)
    for item in web_maps:
        web_map = WebMap(item)
        layers = web_map.layers
        for layer in layers:
            # loops through all input services
            for service in services:
                try:
                    if layer['layerType'] == "VectorTileLayer":
                        if service.lower() in layer.styleUrl.lower():
                            arcpy.AddMessage(f"{item.title} | {layer.styleUrl}")
                    elif service.lower() in layer.url.lower():
                        arcpy.AddMessage(f"{item.title} | {layer.url}")
                except:
                    continue
    arcpy.AddMessage('Search Complete')

# returns Web Mapping Application title, url and configured search fields where the input service matches
def app_search(services):
    arcpy.AddMessage('Searching webapp configured searches in ' + arcpy.GetActivePortalURL())
    web_apps = gis.content.search(query='', item_type='Web Mapping Application', max_items=10000)
    for app in web_apps:
        for service in services:
            try:
                for widget in app.get_data()['widgetOnScreen']['widgets']:
                    if 'uri' in widget.keys() and widget['uri'] == 'widgets/Search/Widget':
                        for source in widget['config']['sources']:
                            if service.lower() in source['url'].lower() and 'searchFields' in source.keys():
                                arcpy.AddMessage("{} | {} | Searching on: {}".format(app.title, source['url'], ", ".join(source['searchFields'])))
                for widget in app.get_data()['widgetPool']['widgets']:
                    if 'uri' in widget.keys() and widget['uri'] == 'widgets/Search/Widget':
                        for source in widget['config']['sources']:
                            if service.lower() in source['url'].lower() and 'searchFields' in source.keys():
                                arcpy.AddMessage("{} | {} | Searching on: {}".format(app.title, source['url'], ", ".join(source['searchFields'])))
            except:
                continue

if __name__ == '__main__':
    main()
