from arcgis.gis import GIS
from arcgis.mapping import WebMap
import arcpy

def finding_unused_services():
    gis = GIS('pro')

    arcpy.AddMessage("Logged into {} as {}".format(arcpy.GetActivePortalURL(), gis.properties['user']['username']))
    services = (gis.content.search(query="", item_type="Map Service", max_items=10000) +
                gis.content.search(query="", item_type="Feature Service", max_items=10000) +
                gis.content.search(query="", item_type="Vector Tile Service", max_items=10000) +
                gis.content.search(query="", item_type="Image Service", max_items=10000))
    arcpy.AddMessage('Searching webmaps in {}'.format(arcpy.GetActivePortalURL()))
    web_maps = gis.content.search(query="", item_type="web map", max_items = 10000)
    for item in web_maps:
        web_map = WebMap(item)
        layers = web_map.layers
        for layer in layers:
            # loops through all input services
            for service in services:
                try:
                    if layer['layerType'] == "VectorTileLayer":
                        if service.url.lower() in layer.styleUrl.lower():
                            services.remove(service)
                    elif service.url.lower() in layer.url.lower():
                            services.remove(service)
                except:
                    continue
    arcpy.AddMessage('The following services are not used in any webmaps in {}'.format(arcpy.GetActivePortalURL()))
    for service in services:
        arcpy.AddMessage('title:{} | url:{}'.format(service.title, (arcpy.GetActivePortalURL() + r'home/item.html?id=' + service.id)))

def main():
    finding_unused_services()

if __name__ == "__main__":
    main()