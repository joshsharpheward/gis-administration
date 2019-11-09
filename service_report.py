# ---------------------------------------------------------------------------------
# scans all map, feature, vector tile and image services in an ArcGIS Online organisation
# or an ArcGIS Enterprise Portal, then writes a csv with the service title, type, layers
# (if any), sharing and groups shared with (if any)
#
# runs over the currently active portal in ArcGIS Pro
#
# (C) 2019 Joshua Sharp-Heward, Whangarei, New Zealand
# released under GNU Lesser Public License v3.0 (GPLv3)
# email jsh726@uowmail.edu.au
# linkedin https://www.linkedin.com/in/joshua-sharp-heward-89b129131/
# ---------------------------------------------------------------------------------

from arcgis.gis import GIS
import arcpy
import csv
import os

def main():
    # sign into the active portal of the ArcGIS Pro Project this script is run from
    gis = GIS('pro')

    arcpy.AddMessage("Logged into {} as {}".format(arcpy.GetActivePortalURL(), gis.properties['user']['username']))

    # get output file path as text
    output_file_path = arcpy.GetParameterAsText(0)

    arcpy.AddMessage("Scanning services in {}".format(arcpy.GetActivePortalURL()))

    # creates list of all service items in active portal
    services = (gis.content.search(query="", item_type="Map Service", max_items=10000) +
                gis.content.search(query="", item_type="Feature Service", max_items=10000) +
                gis.content.search(query="", item_type="Vector Tile Service", max_items=10000) +
                gis.content.search(query="", item_type="Image Service", max_items=10000))

    # initialise empty dictionary to store service information
    service_info = {}

    arcpy.AddMessage("Accessing service properties")

    # iterate over services in service list and populate info into service_info dictionary
    for service in services:
        layers = []
        try:
            for layer in service.layers:
                if layer.properties['type'] != 'Group Layer':
                    layers.append(layer.properties['name'])
        except:
            layers.append("No layers")
        groups = []
        if len(service.shared_with['groups']) != 0:
            for group in service.shared_with['groups']:
                groups.append(group.title)
        else:
            groups.append("Not shared to groups")
        service_info[service.id] = {'service name': service.title,
                                   'service type': service.type,
                                   'service layers': ", ".join(layers),
                                   'service url': service.url,
                                   'sharing': service.access,
                                   'shared groups': ", ".join(groups)}

    arcpy.AddMessage("Writing csv with service information")
    # writes a csv using the csv module and the information gathered iterating over portal services
    with open(output_file_path, mode='w', newline="") as serviceReport:
        fieldnames = ['service name', 'service type', 'service layers', 'service url', 'sharing', 'shared groups']
        reportwriter = csv.DictWriter(serviceReport, fieldnames=fieldnames)
        reportwriter.writeheader()
        for k in service_info.keys():
            reportwriter.writerow(service_info[k])
    # opens file upon completion
    os.startfile(output_file_path)

if __name__ == "__main__":
    main()
