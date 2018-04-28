import pywikibot



class People(object):

    def __init__(self):
        self.names = None
        self.birth_lists = None
        self.job_lists = None

        self.site = pywikibot.Site("en", "wikipedia")
        # Make site object to get the data from.

    def find_people(self):
        pass

    def get_person_info(self, name):
        """Get information for a specific person."""

        page = pywikibot.Page(self.site, name)
        item = pywikibot.ItemPage.fromPage(page)
        item_dict = item.get()
        clm_dict = item_dict["claims"]
        # Get things from all the boxes on the page.

        birth_date = clm_dict["P569"]
        # Get things from the box on date of birth.
        for binfo in birth_date:
            b = binfo.getTarget()
            # Get info from target.
            year_birth = b.year
            month_birth = b.month
            day_birth = b.day
            hour_birth = b.hour
            minute_birth = b.minute
            second_birth = b.second
            birth_date = [second_birth, minute_birth, hour_birth, day_birth,
                          month_birth, year_birth]
            # Get birth date information (up from second to year).

        birth_location = clm_dict["P19"]
        # Get things from the box on location of birth.
        for binfo in birth_location:
            print(len(birth_location))
            b = binfo.getTarget()
            bp_id = b.id
            # Get ID of birth location (for use in coordinate location).
            location = self.get_location_info(bp_id)


    def get_location_info(self, identify):
        """Get location coordinates for astrology"""
        repo = self.site.data_repository()
        item = pywikibot.ItemPage(repo, identify)

        item_dict = item.get()
        clm_dict = item_dict["claims"]
        # Get things from all the boxes on the page.

        coords = clm_dict["P625"]
        # Get things from the box on date of birth.
        for c in coords:
            c_data = c.getTarget()
            lat = c_data.lat
            long = c_data.lon
            alt = c_data.alt
            location_info = [lat, long, alt]

c = People()

c.get_person_info('Albert Einstein')