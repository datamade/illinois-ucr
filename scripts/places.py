import csv
import sys

from census import Census

from secrets import API_KEY

c = Census(API_KEY)

places = set()

for place in c.acs5.state_place(('NAME',), '17', '*'):

    if 'CDP' not in place['NAME']:
        for county in c.acs5.get(('NAME',),
                                 {'for' : 'county:*',
                                  'in' : 'state:{} place:{}'.format('17', place['place'])}):
            if county['NAME'].startswith(('Cook County', 'Lake County', 'DuPage County', 'Kane County', 'Will County', 'McHenry County')):
                places.add((place['NAME'], place['place']))

writer = csv.writer(sys.stdout)
writer.writerow(['Place', 'FIPS'])
for place in sorted(places):
    writer.writerow(place)
