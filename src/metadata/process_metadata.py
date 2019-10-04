#entity extraction
#need to update test and error cases

#package dependency
import numpy as np

class Metadata:
    "extract content metadata from input json file"
    def __init__(self, content):

        self.content = content
        self.metadata = content['data']['item']
        self.id = self.metadata['altids']['itemid']
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

    #need to revisit this function
    #for now ignore the hierachy in tags
    def get_subjects(self):
        "retrieve article tags"
        subjects = self.metadata['subject']
        #cache list to parse the subjects dictionary
        tags = list()
        tag_relations = list()
        for info in subjects:
            tags.append(info['name'])
            try:
                tag_relation = info['rels']
                #if there are more than 1 item
                #in tag_relation,
                #combine as string
                if len(tag_relation) > 1:
                    tag_relation = '_'.join(tag_relation)
                else:
                    #return item, not list
                    tag_relation = tag_relation[0]
                tag_relations.append(tag_relation)
            except:
                tag_relations.append(np.nan)
        return tags, tag_relations

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

    def get_place(self):
        "get a dictionary of associated locations"
        return self.metadata['place']

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
