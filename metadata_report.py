# ---------------------------------------------------------------------------------
# scans all items in an ArcGIS Online organisation or an ArcGIS Enterprise Portal,
# and writes a csv with item title, item type, item id, summary and description
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

    # get output file path as text, and optionally an item owner as text
    output_file_path = arcpy.GetParameterAsText(0)
    item_owner = arcpy.GetParameterAsText(1)

    arcpy.AddMessage('Scanning items')
    # create list of either all items in the active portal, or all of the items owned by one user in the active portal
    if len(item_owner) > 0:
        items = gis.content.search(query="owner: {}".format(item_owner), max_items=10000)
    else:
        items = gis.content.search(query="".format(item_owner), max_items=10000)

    # initialise empty dictionary to store user data
    item_metadata = {}

    # iterate over items in item list and populate info into item_metadata dictionary
    for item in items:
        # filter out item types that aren't useful to report on
        if item.type not in ('Code Attachment', 'Mobile Map Package', 'Layer Template', 'Mobile Application'):
            item_metadata[item.id] = {'title': item.title,
                                     'type': item.type,
                                     'id': item.id,
                                     'summary': "",
                                     'description': ""}
            # accesses item summary
            if item['snippet'] is not None:
                item_metadata[item.id]['summary'] = item['snippet']
            # access item description
            if item['description'] is not None:
                item_metadata[item.id]['description'] = item['description']

    arcpy.AddMessage('Writing csv')
    # writes a csv using the csv module and the information gathered iterating over portal items
    with open(output_file_path, mode='w', newline="", encoding="utf-8") as item_report:
        field_names = ['title', 'type', 'id', 'summary', 'description']
        report_writer = csv.DictWriter(item_report, fieldnames=field_names)
        report_writer.writeheader()
        for k in item_metadata.keys():
            report_writer.writerow(item_metadata[k])
    # opens file upon completion
    os.startfile(output_file_path)

if __name__ == "__main__":
    main()
