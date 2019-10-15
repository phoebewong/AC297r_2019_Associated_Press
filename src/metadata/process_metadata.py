#entity extraction
#need to update test and error cases

#package dependency
import numpy as np

class Metadata:
    "extract content metadata from input json file"
    def __init__(self, content):

        #get parent id for images
        #articles do not have this entity
        try:
            self.ai = content['params']['ai']
        except:
            self.ai = None
        self.content = content
        self.metadata = content['data']['item']
        self.id = self.metadata['altids']['itemid']
        self.version = self.metadata['version']
        self.versioncreated = self.metadata['versioncreated']
        self.uri = self.metadata['uri']
        self.type = self.metadata['type']
        self.language = self.metadata['language']

    ###retrieve content information
    def get_profile(self):
        "get item editorial content type"
        return self.metadata['profile']

    def get_title(self):
        "get title of content"
        try:
            return self.metadata['title']
        except:
            return np.nan

    def get_headline(self):
        "get content headline"
        try:
            return self.metadata['headline']
        except:
            return np.nan

    def get_headline_extended(self):
        "get extended headline"
        try:
            return self.metadata['headline_extended']
        except:
            return np.nan

    def get_summary(self):
        "get content descriptive summary"
        try:
            return self.metadata['description_summary']
        except:
            try:
                return self.metadata['description_caption']
            except:
                return np.nan

    def get_keywords(self):
        "get content keywords generated for search"
        try:
            return self.metadata['keywords']
        except:
            return [np.nan]

    def get_AP_category(self):
        "retrieve AP category code from subject tags"
        categories = list()
        category_codes = list()
        category_relations = list()
        try:
            subjects = self.metadata['subject']
            for info in subjects:
                if list(info.keys())[0] == 'rels':
                    categories.append(info['name'])
                    if len(info['rels']) > 1:
                        category_relations.append('_'.join(info['rels']))
                    else:
                        category_relations.append(info['rels'][0])
                    category_codes.append(info['code'])
            return categories, category_relations, category_codes
        except:
            return [np.nan], [np.nan], [np.nan]

    def get_subjects(self):
        "retrieve subject tags"
        #cache list to parse the subjects dictionary
        tags = list()
        tag_relations = list()
        tag_codes = list()
        try:
            subjects = self.metadata['subject']
            for info in subjects:
                #skip ap category code
                if list(info.keys())[0] != 'rels':
                    tags.append(info['name'])
                    tag_codes.append(info['code'])
                    try:
                        tag_relation = info['rels']
                        #if there are more than 1 item
                        #in tag_relation
                        #combine as string
                        if len(tag_relation) > 1:
                            tag_relation = '_'.join(tag_relation)
                        else:
                            #return item, not list
                            tag_relation = tag_relation[0]
                        tag_relations.append(tag_relation)
                    except:
                        tag_relations.append(np.nan)
            return tags, tag_relations, tag_codes
        except:
            return [np.nan], [np.nan], [np.nan]

    ###retrieve person tags
    def get_person_tags(self):
        "retrieve content person tags"
        persons = list()
        persons_code = list()
        person_relations = list()
        try:
            person_list = self.metadata['person']
            for p in person_list:
                name = p['name']
                rels = p['rels']
                code = p['code']
                persons.append(name)
                persons_code.append(code)
                if len(rels) > 1:
                    rels = '_'.join(rels)
                else:
                    rels = rels[0]
                person_relations.append(rels)
            return persons, person_relations, persons_code
        except:
            return [np.nan], [np.nan], [np.nan]

    def get_person_types(self):
        "retrieve content person type in tags"
        names = list()
        types = list()
        codes = list()
        try:
            person_list = self.metadata['person']
            for p in person_list:
                try:
                    for t in p['types']:
                        names.append(p['name'])
                        codes.append(p['code'])
                        types.append(t)
                except:
                    continue
            return names, codes, types
        except:
            return [np.nan], [np.nan], [np.nan]

    def get_person_team(self):
        "retrieve team of tagged person"
        names = list()
        codes = list()
        teams = list()
        team_codes = list()
        try:
            person_list = self.metadata['person']
            for p in person_list:
                try:
                    team = p['teams']
                    for t in team:
                        names.append(p['name'])
                        codes.append(p['code'])
                        teams.append(t['name'])
                        team_codes.append(t['code'])
                except:
                    continue
            return names, codes, teams, team_codes
        except:
            return [np.nan], [np.nan], [np.nan], [np.nan]

    ###retrieve organisation tags
    def get_organisation(self):
        "retrieve organisation tags"
        org_names = list()
        org_relations = list()
        org_codes = list()
        try:
            org_list = self.metadata['organisation']
            for org in org_list:
                org_names.append(org['name'])
                if len(org['rels']) > 1:
                    org_relations.append('_'.join(org['rels']))
                else:
                    org_relations.append(org['rels'][0])
                org_codes.append(org['code'])
            return org_names, org_relations, org_codes
        except:
            return [np.nan], [np.nan], [np.nan]

    def get_organisation_industry(self):
        "retrieve organisation industry tags"
        org_names = list()
        org_codes = list()
        org_industries_names = list()
        org_industries_codes = list()
        try:
            org_list = self.metadata['organisation']
            for org in org_list:
                org_names.append(org['name'])
                org_codes.append(org['code'])
                try:
                    industries = org['industries']
                    for ind in industries:
                        org_industries_names.append(ind['name'])
                        org_industries_codes.append(ind['code'])
                except:
                    org_industries_names.append(np.nan)
                    org_industries_codes.append(np.nan)
            return org_names, org_codes, org_industries_names, org_industries_codes
        except:
            return [np.nan], [np.nan], [np.nan], [np.nan]

    ###retrieve place tags
    def get_place(self):
        "get locations associated with content"
        place_names = list()
        place_codes = list()
        place_relations = list()
        try:
            places = self.metadata['place']
            for p in places:
                place_names.append(p['name'])
                place_codes.append(p['code'])
                if len(p['rels']) > 1:
                    place_relations.append('_'.join(p['rels']))
                else:
                    place_relations.append(p['rels'][0])
            return place_names, place_relations, place_codes
        except:
            return [np.nan],[np.nan],[np.nan]

    ###retrieve event tags
    def get_event_tags(self):
        "retrieve event names"
        event_names = list()
        event_codes = list()
        try:
            events = self.metadata['event']
            for e in events:
                event_names.append(e['name'])
                try:
                    event_codes.append(e['code'])
                except:
                    event_codes.append(np.nan)
            return event_names, event_codes
        except:
            return [np.nan], [np.nan]

    ###retrieve geographical information
    def get_city(self):
        try:
            return self.metadata['datelinelocation']['city']
        except:
            return np.nan

    def get_country_areacode(self):
        try:
            return self.metadata['datelinelocation']['countryareacode']
        except:
            return np.nan

    def get_country_areaname(self):
        try:
            return self.metadata['datelinelocation']['countryareaname']
        except:
            return np.nan

    def get_country_code(self):
        try:
            return self.metadata['datelinelocation']['countrycode']
        except:
            return np.nan

    def get_country_name(self):
        try:
            return self.metadata['datelinelocation']['countryname']
        except:
            return np.nan

    def get_long_lat(self):
        try:
            long_lat = self.metadata['datelinelocation']['geometry_geojson']
            return long_lat['coordinates']
        except:
            return np.nan


    ###retrieve publishing logistic information
    def get_altids(self):
        "return alternative ids as a dictionary"
        return self.metadata['altids']

    def get_pubstatus(self):
        "get item publishing status"
        return self.metadata['pubstats']

    def get_editorialrole(self):
        "get editorial role of content"
        return self.metadata['editorialrole']

    def get_signals(self):
        "get content item processing status"
        return self.metadata['signals']

    def get_copyrightnotice(self):
        "get copyright notice"
        return self.metadata['copyrightnotice']

    def get_usageterms(self):
        "get content usage limitation"
        return self.metadata['usageterms']
