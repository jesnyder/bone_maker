#!/usr/bin/env python3
"""
Script to scrape clinicaltrials.gov website and return information
on studies. In particular, we're interested in converting an nctid
(national clinical study identifier?) to a tuple of (country, zip).
"""
import json
import requests
import logging
import os
import sys
import time

from c0001_retrieve_meta import retrieve_path


logging.getLogger().setLevel(logging.INFO)


# Took some experimentation. See API docs here:
#
#   https://clinicaltrials.gov/api/gui/ref/api_urls#expr
#
# Given a specific study such as:
#
#   https://clinicaltrials.gov/ct2/show/NCT04276987
#
# we can extract the trial id and substitute that as a URL parameter.
# We'll use JSON to make extracting the subfields easy.

# BASE_URL = "https://clinicaltrials.gov/api/query/full_studies?expr=NCT04276987&fmt=json"
BASE_URL = "https://clinicaltrials.gov/api/query/full_studies?expr={}&fmt=json"


class ClinicalTrial():
    """
    Data structure for handling information about a given Clinical Study.
    Requires an NCTID to create (so it can be looked up via API).
    Attributes include:

      title (BriefTitle)
      location (country, zip)

    """

    def __init__(self, nctid):
        self.nctid = nctid
        self.api_url = BASE_URL.format(self.nctid)
        print(f"Study url: {self.api_url}")

        path = retrieve_path('json_clinical')
        file = os.path.join(path, nctid  + '.json')
        print('json file: ')
        print(file)

        #raw_json = r.json()
        # raw_json = json.loads(file)

        with open(file, 'r') as myfile:
            #data = myfile.read()
            raw_json = json.load(myfile)

        self.raw_json = raw_json

        """
        if len(raw_json["FullStudiesResponse"]["FullStudies"]) != 1:
            logging.error(f"Could not find study for nctid {self.nctid}")

        self.raw_json = raw_json["FullStudiesResponse"]["FullStudies"][0]["Study"]
        """

    # walk the dict and retrieve country, zip.
    # path to desired struct:
    #
    #  ["FullStudiesResponse"]["FullStudies"][0]["Study"]["ProtocolSection"]["ContactsLocationsModule"]["LocationList"]["Location"]
    #
    # Yowza.

    @property
    def location(self):

        try:
            locations = self.raw_json["ProtocolSection"]["ContactsLocationsModule"]["LocationList"]["Location"]
            if len(locations) < 1:
                logging.warning("No location found for study")
                raise ValueError
            elif len(locations) > 1:
                logging.warning("Multiple locations found for study, ignoring all but first")

            location = locations[0]
            city = location["LocationCity"]
            facility = location["LocationFacility"]
            zipcode = location["LocationZip"]
            country = location["LocationCountry"]

        except:
            country, zipcode, city, facility = None, None, None, None

        return (facility, zipcode, city, country)

    @property
    def title(self):
        return self.raw_json["ProtocolSection"]["IdentificationModule"]["BriefTitle"]


    @property
    def contacts(self):

        try:
            contacts = self.raw_json["ProtocolSection"]["ContactsLocationsModule"]["OverallOfficialList"]["OverallOfficial"]
            if len(contacts) < 1:
                logging.warning("No contacts found for study")
                raise ValueError
            elif len(contacts) > 1:
                logging.warning("Multiple contacts found for study, ignoring all but first")

            contacts = contacts[0]
            name = contacts["OverallOfficialName"]
            affiliation = contacts["OverallOfficialAffiliation"]
            role = contacts["OverallOfficialRole"]

        except:
            name, affiliation, role = None, None, None

        return (name, affiliation, role)

    @property
    def condition(self):

        try:
            condition = self.raw_json["ProtocolSection"]["ConditionsModule"]["ConditionList"]["Condition"]
            if len(condition) < 1:
                logging.warning("No contacts found for study")
                raise ValueError
            elif len(condition) > 1:
                logging.warning("Multiple contacts found for study, ignoring all but first")

            condition = condition[0]
            #meshTerm = condition["ConditionMeshTerm"]


        except:
            condition = None

        return (condition)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        logging.error("Usage: provide nctids on command line")
        sys.exit(1)

    for nctid in sys.argv[1:]:
        s = ClinicalTrial(nctid)
        logging.info(f"Study found in {s.location}: {s.title}")
