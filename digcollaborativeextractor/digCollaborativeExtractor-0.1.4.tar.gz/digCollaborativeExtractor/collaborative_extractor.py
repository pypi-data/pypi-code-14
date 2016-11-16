__author__ = 'majid'
import json
from copy import copy
from digExtractor.extractor import Extractor

class collaborative_extractor(Extractor):
    def __init__(self, prior_dict):
        self.renamed_input_fields = 'phone'
        self.metadata = {'extractor': 'city'}
        self.prior_dict = prior_dict
        # self.init_prior_dictionaries(email_prior_path, phone_prior_path)

    def set_extraction_field(self, extraction_field):
        self.extraction_field = extraction_field
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields

    def get_metadata(self):
        return copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    # def init_prior_dictionaries(self, email_prior_path, phone_prior_path):
    #     phone_prior_info = []
    #     email_prior_info = []
    #     if phone_prior_path is not None:
    #         phone_prior_info = [eval(x) for x in open(phone_prior_path).readlines()]
    #     if email_prior_path is not None:
    #         email_prior_info = [eval(x) for x in open(email_prior_path).readlines()]
    #     self.phone2country = {}
    #     self.email2country = {}
    #     for x in phone_prior_info:
    #         self.phone2country[x[0]] = dict(x[1])
    #     for x in email_prior_info:
    #         self.email2country[x[0]] = dict(x[1])

    def extract_city(self, info, image2country=None, uri2imageurl=None):
        # prediction_res = open('prediction_res.json', 'w')
        # emails = all_gt[ID]['emails']
        # try using phone
        aggregated = {}
        for x in info:
            if x in self.prior_dict:
                for c, num in self.prior_dict[x].items():
                    if c in aggregated:
                        aggregated[c] += num
                    else:
                        aggregated[c] = num

        # x['phones'] = phones
        sum_count = float(sum([xx[1] for xx in aggregated.items()]))
        # res = {'prediction': sorted([{'name': xx[0], 'probability': float(xx[1])/sum_count} for xx in all_countries.items()],
        #                                 key=lambda x: x['probability'], reverse=True)}
        # standard_error = max([sqrt(xx['probability']*(1.0 - xx['probability'])/float(sum_count)) for xx in x['predicted_country']] + [0.0])
        # standard_error = sqrt(0.25 / float(sum_count+1))
        # res['standard_error'] = standard_error
        # res['confidence'] = 2.0*norm(0,1).pdf(standard_error) - 1.0
        res = sorted([{'name': xx[0], 'probability': float(xx[1])/sum_count} for xx in aggregated.items()],
                                        key=lambda x: x['probability'], reverse=True)
        res = [x['name'] for x in res]
        # print(res)
        return res

    def extract(self, doc):
        # print doc
        if self.renamed_input_fields in doc:
            if self.extraction_field == 'city':
                if type(doc[self.renamed_input_fields]) is list:
                    return self.extract_city(doc[self.renamed_input_fields])
                else:
                    return self.extract_city([doc[self.renamed_input_fields]])
            else:
                return None
        else:
            return None



class voting_country_predictor(Extractor):
    def __init__(self, city2country_dict):
        self.city2country = city2country_dict
        self.metadata = {'extractor': 'country'}
        self.renamed_input_fields = 'country'

    def get_renamed_input_fields(self):
        return self.renamed_input_fields

    def set_renamed_input_fields(self, x):
        self.renamed_input_fields = x
        return self

    def get_metadata(self):
        return copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def pred_country(self, info):
        # try using phone
        all_countries = {}
        for city in info:
            if city in self.city2country:
                countries = self.city2country[city]
                for country in countries:
                    if country in all_countries:
                        all_countries[country] += 1
                    else:
                        all_countries[country] = 1

        res = sorted(all_countries.items(), key=lambda x: x[1], reverse=True)
        if len(res) == 0:
            return None
        # return {'name': res[0][0],
        #         'probability': (float(res[0][1]) / float(sum(all_countries.values()))),
        #         'cities': info,
        #         'count': res[0][1]
        #         }
        return res[0][0]

    def extract(self, doc):
        # print 'doc is: ' + str(doc)
        if type(self.renamed_input_fields) is list:
            input_fields = self.renamed_input_fields
        else:
            input_fields = [self.renamed_input_fields]
        if any([(x in doc) for x in input_fields]):
            input_arr = []
            for f in input_fields:
                if f in doc:
                    if type(doc[f]) is str:
                        input_arr.append(doc[f])
                    else:
                        for xx in doc[f]:
                            input_arr.append(xx)
            # print(input_arr)
            return self.pred_country(input_arr)
        else:
            return None


# if __name__ == '__main__':
    # sample_gt = [json.loads(x) for x in open('sample_country_gt_test.json')]
    # all_gt = dict([(json.loads(line)['_id'].strip(), json.loads(line)) for line in open('/Users/majid/DIG/dig-groundtruth-data/memex-2016-summer-eval/all_extractions_july_2016.jl')])
    # alldata = dict([(json.loads(x)['_id'], json.loads(x)) for x in open('//Users/majid/DIG/dig-groundtruth-data/memex-2016-summer-eval/cdr_input_ads.jl')])
    # input = []
    # for x in sample_gt:
    #     print x
    #     uri = x['uri']
    #     all_gt[uri]['annotated_country'] = x['country']
    #     input.append(all_gt[uri])
    #
    # phone2city = []
    # email2city = []
    #
    # city_collaborative_email = ExtractorProcessor() \
    #     .set_output_field('city') \
    #     .set_extractor_processor_inputs(email_high_recall) \
    #     .set_extractor(collaborative_filtering_extractor([], email2city).set_extraction_field('city')) \
    #     .set_name('collaborative_filtering_email2city')
    #
    # city_collaborative_phone = ExtractorProcessor() \
    #     .set_output_field('city') \
    #     .set_extractor_processor_inputs(phone_high_recall) \
    #     .set_extractor(collaborative_filtering_extractor(phone2city, []).set_extraction_field('city')) \
    #     .set_name('collaborative_filtering_phone2city')