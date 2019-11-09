# ---------------------------------------------------------------------------------
# scans all users in an ArcGIS Online organisation or an ArcGIS Enterprise Portal,
# then writes a csv with each user's username, first name (if specified), last name
# (if specified), email, level, role, groups and last login date
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
import time
import csv
import os

def main():
    # sign into the active portal of the ArcGIS Pro Project this script is run from
    gis = GIS('pro')

    arcpy.AddMessage("Logged into {} as {}".format(arcpy.GetActivePortalURL(), gis.properties['user']['username']))

    # get output file path as text
    output_file_path = arcpy.GetParameterAsText(0)

    arcpy.AddMessage('Scanning users in  {}'.format(arcpy.GetActivePortalURL()))

    # create list of all users in the active portal
    users = gis.users.search(query="", max_users=10000)

    # initialise empty dictionary to store user data
    user_info = {}

    arcpy.AddMessage("Accessing user properties")

    # iterate over users in user list and populate info into user_info dictionary
    for user in users:
        user_groups = []
        for grp in user.groups:
            # this try and except handles when users are in external secured groups, which returns an error when you try to find the group's title
            try:
                user_groups.append(grp.title)
            except:
                user_groups.append('External private group')
        user_info[user.username] = {'username': user.username,
                                    'first name': "",
                                    'last name': "",
                                    'email': user.email,
                                    'level': user.level,
                                    'role': user.role,
                                    'groups': ", ".join(user_groups),
                                    'last login': ""}
        if hasattr(user, 'firstName'):
            user_info[user.username]['first name'] = user.firstName
        if hasattr(user, 'lastName'):
            user_info[user.username]['last name'] = user.lastName
        if user.lastLogin > 0:
            user_info[user.username]['last login'] = time.strftime("%d/%m/%Y", time.localtime(user.lastLogin / 1000))

    arcpy.AddMessage('Writing csv with user information')
    # writes a csv using the csv module and the information gathered iterating over portal users
    with open(output_file_path, mode='w', newline="") as user_report:
        field_names = ['username', 'first name', 'last name', 'email', 'level', 'role', 'groups', 'last login']
        user_writer = csv.DictWriter(user_report, fieldnames=field_names)
        user_writer.writeheader()
        for k in user_info.keys():
            user_writer.writerow(user_info[k])
    # opens file upon completion
    os.startfile(output_file_path)

if __name__ == "__main__":
    main()
