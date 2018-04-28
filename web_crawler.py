import pywikibot
from pywikibot import pagegenerators as pg
import numpy as np
import pandas as pd


class People(object):

    def __init__(self):
        self.names = None
        self.birth_lists = None
        self.job_lists = None
        self.site = pywikibot.Site("en", "wikipedia")
        # Make site object to get the data from.
        self.repo = self.site.data_repository()

    def get_people(self):
        """Load in csv for web query data"""
        df = pd.read_csv('query.csv')
        # Load in dataframe of query data from wikidata.
        addresses = df['item']
        # Wiki-data addresses of people to use.
        query_right = [a.replace('http://www.wikidata.org/entity/', '') for a in addresses]
        # Get query in form that can be passed to 'get_person_info'

        #, numpy_long, numpy_alt = np.empty((len(query_right),)), \
        #                                   np.empty((len(query_right),)), \
         #                                  np.empty((len(query_right),))
        # Empty numpy arrays to fill with location data.

        frames = []

        for i,q in enumerate(query_right[:100]):
            n, b, l, o, g = self.get_person_info(q)
            #intodf = [n, b[0], b[1], b[2], b[3], b[4], b[5], b[6], l[0], l[1], l[2], o, g]
            d = {'serial':q, 'lat':l[0], 'long':l[1], 'second':b[0], 'minute':b[1], 'hour':b[2],
                 'day':b[3], 'month':b[4], 'year':b[5], 'timezone':b[6], 'occupation':o,
                     'gender':g}
            new_data = pd.DataFrame(data=d, index=[i])
            frames.append(new_data)

        result = pd.concat(frames)
        # Concatenate all the dataframes into one.

        with open('dump2.csv', 'w') as f:
            result.to_csv(f, header=True)
             #Save data.


    def get_person_info(self, name):
        """Get information for a specific person."""
        #page = pywikibot.Page(self.site, name)
        #item = pywikibot.ItemPage.fromPage(page)
        item = pywikibot.ItemPage(self.repo, name)
        item_dict = item.get()
        clm_dict = item_dict["claims"]
        # Get things from all the boxes on the page.

        if 'en' in item.labels:
            name =  item.labels['en']

        birth_date = clm_dict["P569"]
        # Get things from the box on date of birth.
        for binfo in birth_date:
            b = binfo.getTarget()
            #print(b.__dict__.keys())
            # Get info from target.
            year_birth = b.year
            month_birth = b.month
            day_birth = b.day
            hour_birth = b.hour
            minute_birth = b.minute
            second_birth = b.second
            timezone_birth = b.timezone
            bdate = [second_birth, minute_birth, hour_birth, day_birth,
                          month_birth, year_birth, timezone_birth]
            # Get birth date information (up from second to year).

        birth_location = clm_dict["P19"]
        # Get things from the box on location of birth.
        for binfo in birth_location:
            b = binfo.getTarget()
            bp_id = b.id
            # Get ID of birth location (for use in coordinate location).
            location = self.get_location_info(bp_id)

        gender = clm_dict["P21"]
        # Get things for box on gender.
        for g in gender:
            b = g.getTarget()
            mf_id = b.id
            # Get id of gender.
            if b.id == 'Q6581097':
                mf = 'Male'
            elif b.id == 'Q6581072':
                mf = 'Female'

        occupation = clm_dict["P106"]
        occu = []
        for op in occupation:
            o = op.getTarget()
            o_id = o.id
            occu.append(self.get_occupation_info(o_id))

        occu = ','.join(occu)

        return name, bdate, location, occu, mf



    def get_location_info(self, identify):
        """Get location coordinates for astrology"""
        item = pywikibot.ItemPage(self.repo, identify)

        item_dict = item.get()
        clm_dict = item_dict["claims"]
        # Get things from all the boxes on the page.

        try:
            coords = clm_dict["P625"]
            # Get things from the box on coordinates.
            for c in coords:
                c_data = c.getTarget()
                lat = c_data.lat
                long = c_data.lon
                alt = c_data.alt
                location_info = [lat, long, alt]

        except KeyError:
            location_info = 'None'

        return location_info


    def get_occupation_info(self, identify):
        """Get occupation for astrology"""
        item = pywikibot.ItemPage(self.repo, identify)
        item.get()

        if 'en' in item.labels:
            profession_name =  item.labels['en']
            # Get profession name.
        #print(profession_name)

        return profession_name


c = People()
c.get_people()

#c.get_person_info('http://www.wikidata.org/entity/Q7791722')
