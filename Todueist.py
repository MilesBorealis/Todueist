# Todueist
# Author: MilesBorealis; Date: 02/15/2020
# Based off of u/DinoPunch's reddit post: https://www.reddit.com/r/todoist/comments/fdlb6l/i_use_labels_to_set_deadlines_so_i_can_move_the/

#Imports
import datetime
import todoist
from dateutil.relativedelta import *

#Todoist API initiation
api = todoist.TodoistAPI('')

#Establish today's date
today = datetime.date.today()

"""
Check for due date labels. If labels are not present, they will be created.
"""

#Create Array for Label Objects
labels1 = api.state['labels']

current_year = date.today().year
first_of_the_year = datetime.datetime(current_year, 1, 1)

#Create "Due" labels
due_found = False
for i in labels1:
    if i.data['name'] == "Due":
        print("Found: " + i.data['name'])

        #change due_found to true as "Due" label already exists
        due_found = True

if due_found == False:
    print("Did not find: Due. Adding label.")

    #Create label with color sky blue - 39
    api.labels.add(name = "Due", color = 39, item_order = 0)


#Create month labels
for i in range(12):
    #Set up condition to identify if month label is found
    month_found = False

    #iterate through all labels
    for j in labels1:

        #If label name already exists
        if j.data['name'] == first_of_the_year.strftime("%B"):
            print("Found: " + j.data['name'])

            #Change month_found to true as month label already exists
            month_found = True

    #If month label was not found, create label
    if month_found == False:
        print("Did not find: " + first_of_the_year.strftime("%B") + ". Adding label.")

        #Create label with month name and color sky blue - 39
        api.labels.add(name = first_of_the_year.strftime("%B"), color = 39, item_order = 1)

    #increment month
    first_of_the_year = first_of_the_year + relativedelta(months=+1)

#Create day labels
for i in range(1,32):
    #Set up condition to identify if day label is found
    day_found = False

    if i < 10:
        x = "0" + str(i)
    else:
        x = str(i)

    #iterate through all labels
    for j in labels1:

        #If label name already exists
        if j.data['name'] == x:
            print("Found: " + j.data['name'])

            #Change day_found to true as day label already exists
            day_found = True

    #If day label was not found, create label
    if day_found == False:
        print("Did not find: " + x + ". Adding label.")

        #Create label with day name and color sky blue - 39
        api.labels.add(name = x, color = 39, item_order = 2)


#Variable for how many years ahead, in addition to the current year, should be added as labels
years_ahead = 1

#Variable should not be changed.
year_label = current_year


#Create year lables
for i in range(years_ahead + 1):

    #Set up condition to identify if year label is found
    year_found = False

    #iterate through all labels
    for j in labels1:

        #If label name already exists

        data = j.data
        if data['name'] == str(year_label):
            print("Found: " + data['name'])

            #label already exists, change year_found to true to prevent label creation
            year_found = True

    #if year_label was not found, create the label
    if year_found == False:
        print("Did not find: " + str(year_label) + ". Adding label.")

        #create label with year name and color sky blue - 39
        api.labels.add(name = str(year_label), color = 39, item_order = 3)

    #increment year_label
    year_label += 1


#commit changes
api.commit()

"""
Check for Upcoming Due Tasks Filter. If filter is not present, it will be created.
"""

#Create Array for Filter Objects
filters1 = api.state['filters']

#Search for existence of "Upcoming Due Tasks"
taskExists = False

for x in filters1:
    y = x.data
    if str(y['name']) == "Upcoming Due Tasks":
        print("Filter '" + str(y['name']) + "' found, id: " + str(y['id']))
        filterid = y['id']
        taskExists = True

#If filter is not present, create Filter "Upcoming Due Tasks"
if taskExists == False:
    print("Filter is not present. Creating Filter 'Upcoming Due Tasks'")
    filter = api.filters.add(name = "Upcoming Due Tasks", query = "@Due", color = 42, is_favorite = 1)
    filterid = filter.temp_id
    print(filter.temp_id)

#Update Filter

#Days must be greater than 0
days = 7

#Create string for query
query = ""

for x in range(days):
    #Define date
    date = today + datetime.timedelta(days=x)

    #For queries longer than 1 item, add 'or' bar --> "|"
    if x > 0:
        query = query + "| "

    #Concat with new query
    query = query + date.strftime("@Due & @%B & @%d & @%Y ")

#Find filter 'Upcoming Due Tasks'
filter2 = api.filters.get_by_id(filterid)

#Update Filter Query
filter2.update(query = query)

#Commit changes
api.commit()
