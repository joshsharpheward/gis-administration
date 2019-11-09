# ---------------------------------------------------------------------------------
# scans all map, feature, vector tile and image services in an ArcGIS Online organisation
# or an ArcGIS Enterprise Portal, then returns the items of the services which are not used
# within any web maps within that organisation
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


def main():
    # logs into active portal in ArcGIS Pro
    gis = GIS('pro')

    arcpy.AddMessage("Logged into {} as {}".format(arcpy.GetActivePortalURL(), gis.properties['user']['username']))

    # creates list of items of all map image, feature, vector tile and image services (up to 10000 of each) in active portal
    services = (gis.content.search(query="", item_type="Map Service", max_items=10000) +
                gis.content.search(query="", item_type="Feature Service", max_items=10000) +
                gis.content.search(query="", item_type="Vector Tile Service", max_items=10000) +
                gis.content.search(query="", item_type="Image Service", max_items=10000))

    arcpy.AddMessage('Searching webmaps in {}'.format(arcpy.GetActivePortalURL()))

    # creates list of items of all webmaps in active portal
    web_maps = gis.content.search(query="", item_type="Web Map", max_items = 10000)
    # loops through list of webmap items
    for item in web_maps:
        # creates a WebMap object from input webmap item
        web_map = WebMap(item)
        # accesses basemap layer(s) in WebMap object
        basemaps = web_map.basemap['baseMapLayers']
        # accesses layers in WebMap object
        layers = web_map.layers
        # loops through basemap layers
        for bm in basemaps:
            # tests whether the bm layer has a styleUrl(VTS) or url (everything else)
            if 'styleUrl'in bm.keys():
                for service in services:
                    if service.url in bm['styleUrl']:
                        services.remove(service)
            elif 'url' in bm.keys():
                for service in services:
                    if service.url in bm['url']:
                        services.remove(service)
        # loops through layers
        for layer in layers:
            # tests whether the layer has a styleUrl(VTS) or url (everything else)
             if hasattr(layer, 'styleUrl'):
                 for service in services:
                    if service.url in layer.styleUrl:
                        services.remove(service)
             elif hasattr(layer, 'url'):
                 for service in services:
                    if service.url in layer.url:
                        services.remove(service)

    arcpy.AddMessage('The following services are not used in any webmaps in {}'.format(arcpy.GetActivePortalURL()))
    # as we have removed all services being used in active portal, print list of remaining unused services
    for service in services:
        arcpy.AddMessage("{} | {}".format(service.title ,arcpy.GetActivePortalURL() + r'home/item.html?id=' + service.id))
    arcpy.AddMessage("There are a total of {} unused services in your portal".format(str(len(services))))

if __name__ == "__main__":
    main()
