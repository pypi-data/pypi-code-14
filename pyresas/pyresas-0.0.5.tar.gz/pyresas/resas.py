import requests,json
import logging

API_ENDPOINT = 'https://opendata.resas-portal.go.jp'

class RESASAPIException(Exception):
  def __init__(self, obj):
    self.status_code = obj['statusCode']
    self.message = obj['message']
  def __str__(self):
    return 'statusCode:"{:s}" message:"{:s}"'.format(self.status_code, self.message)

class RESASAPI() :
  def __init__(self, api_key, api_endpoint=API_ENDPOINT) :
    self.api_key = api_key
    self.api_endpoint = api_endpoint

  def getPrefectures(self) :
    return self.request('api/v1-rc.1/prefectures')

  def getCities(self, prefCode) :
    return self.request('api/v1-rc.1/cities', {'prefCode':prefCode})

  def getOldCities(self, prefCode, cityCode) :
    return self.request('api/v1-rc.1/oldCities', {'prefCode':prefCode, 'cityCode':cityCode})

  def getIndustriesBroad(self) :
    return self.request('api/v1-rc.1/industries/broad')

  def getIndustriesMiddle(self, sicCode) :
    return self.request('api/v1-rc.1/industries/middle', {'sicCode':sicCode})

  def getIndustriesNarrow(self, simcCode) :
    return self.request('api/v1-rc.1/industries/narrow', {'simcCode':simcCode})

  def getJobsBroad(self) :
    return self.request('api/v1-rc.1/jobs/broad')

  def getJobsMiddle(self, iscoCode) :
    return self.request('api/v1-rc.1/jobs/middle', {'iscoCode':iscoCode})

  def getPatentsBroad(self) :
    return self.request('api/v1-rc.1/patents/broad')

  def getPatentsMiddle(self, tecCode) :
    return self.request('api/v1-rc.1/patents/middle', {'tecCode':tecCode})

  def getCustoms(self, prefCode) :
    return self.request('api/v1-rc.1/customs', {'prefCode':prefCode})

  def getRegionsBroad(self) :
    return self.request('api/v1-rc.1/regions/broad')

  def getRegionsMiddle(self, regionCode) :
    return self.request('api/v1-rc.1/regions/middle', {'regionCode':regionCode})

  def getRegionsAgricultureDepartments(self) :
    return self.request('api/v1-rc.1/regions/agricultureDepartments')

  def getPatentsLocations(self, prefCode, cityCode) :
    return self.request('api/v1-rc.1/patents/locations', {'prefCode':prefCode, 'cityCode':cityCode})

  def getTradeInfoItemTypesBroad(self) :
    return self.request('api/v1-rc.1/tradeInfoItemTypes/broad')

  def getTradeInfoItemTypesMiddle(self, itemCode1) :
    return self.request('api/v1-rc.1/tradeInfoItemTypes/middle', {'itemCode1':itemCode1})

  def getTradeInfoItemTypesNarrow(self, itemCode1, itemCode2) :
    return self.request('api/v1-rc.1/tradeInfoItemTypes/narrow', {'itemCode1':itemCode1, 'itemCode2':itemCode2})

  def request(self, path, params = None) :
    res = requests.get(
      '{:s}/{:s}'.format(self.api_endpoint, path),
      headers={'X-API-KEY':self.api_key},
      params=params
      )
    obj = json.loads(res.text)

    if ('statusCode' in obj.keys()) and obj['statusCode'] != u'200' :
      logging.error("invalid api statuscode: {:s} ({:s})".format(
        obj['statusCode'], obj['message']))
      raise RESASAPIException(obj)
    return obj['result']

if __name__ == '__main__':
  from pprint import pprint as pp
  logging.basicConfig(level=logging.NOTSET)
  api_key = "..."

  resas_api = RESASAPI(api_key)
  res = resas_api.getPrefectures()
  pp(res)
  #res = resas_api.getCities(res[0]['prefCode'])

  #res = resas_api.getIndustriesBroad()
  #res = resas_api.getIndustriesMiddle(res[0]['sicCode'])
  #res = resas_api.getIndustriesNarrow(res[0]['simcCode'])

  #res = resas_api.getJobsBroad()
  #res = resas_api.getJobsMiddle(res[0]['iscoCode'])

  #res = resas_api.getPatentsBroad()
  #res = resas_api.getPatentsMiddle(res[1]['tecCode'])

  #res = resas_api.getPrefectures()
  #res = resas_api.getCustoms(res[0]['prefCode'])

  #res = resas_api.getRegionsAgricultureDepartments()

  #res = resas_api.getTradeInfoItemTypesBroad()
  #res = resas_api.getTradeInfoItemTypesMiddle(res[0]['itemCode1'])
