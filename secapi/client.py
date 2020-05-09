import requests
import json
import pkg_resources


"""Main module."""
class SecApi:
    class __Company:
        def __init__(self, parent):
            self.parent = parent

        def companyDetail(self, companyId):
            return self.parent.make_get_request('companies',[companyId])

        def find(self, companyId=None, sic=None, cik=None, ticker=None, name=None):
            return self.parent.make_post_request('companies',['find'], {'id':companyId,'sic':self.parent.Noneint(sic), 'cik':self.parent.Noneint(cik),'ticker':ticker, 'name':name})


    class __Filing:
        def __init__(self, parent):
            self.parent = parent

        def filingDetail(self, filingId):
            return self.parent.make_get_request('filings',[filingId])

        def filingCompleteTextFile(self, filingId):
            return self.parent.make_get_request('filings',[filingId,'completeTextFile'])

        def filingGetFileBySequenceId(self, filingId, sequenceId):
            return self.parent.make_get_request('filings',[filingId,'file',str(sequenceId)])

        def filingGetFileByName(self, filingId, name):
            return self.parent.make_get_request('filings',[filingId,'file',name])

        def filingGetAsText(self, filingId):
            return self.parent.make_get_request('filings',[filingId,'text'])

        def find(self, filingId=None, companyId=None, companyCik=None, filinType=None, accessionNo=None, sort_field='FilingDate', direction='Asc', start=0, limit=1000):
            return self.parent.make_post_request('filings',[f'find?start={start}&limit={limit}'],
             {'query': {'id':filingId,'companyId':companyId, 'companyCik':self.parent.Noneint(companyCik),'filinType':filinType, 'accessionNo':self.parent.Noneint(accessionNo)},'sort':{'field': sort_field, 'direction':direction}})



    class __Sector:
        def __init__(self, parent):
            self.parent = parent

        def sicCodes(self):
            return self.parent.make_get_request('sicCodes')


    class __Ticker:
        def __init__(self, parent):
            self.parent = parent

        def tickers(self):
            return self.parent.make_get_request('tickers')


    def __init__(self, apiKey=''):
        self.verify_ssl = True
        self.host = "https://sec-api.com"
        self.base_url = "/api/v2/"
        self.user_agent = 'secApi/%s/python' % pkg_resources.require("SecApi")[0].version


        self.session = requests.Session()
        self.session.headers.update({'user-agent': self.user_agent})
        self.set_api_key(apiKey)




        self.Ticker = self.__Ticker(self)
        self.Company = self.__Company(self)
        self.Filing = self.__Filing(self)
        self.Sector = self.__Sector(self)

    def Noneint(self, num):
        if num is None:
            return None
        return int(num)

    def set_api_key(self, apiKey):
        if not apiKey or apiKey== '':
            raise Exception('ApiKey is required, register for a free key at: https://sec-api.com')
        self.api_key = apiKey
        self.session.headers.update({'Authorization': f"Bearer {self.api_key}"})

    def make_get_request(self, method, args=[]):
        url = f"{self.host}{self.base_url}{method}/{'/'.join(args)}"
        # print (url)
        ret = self.session.get(url).content
        try:
            return json.loads(ret)
        except Exception as e:
            raise Exception(b'Error, returned:' + ret)


    def make_post_request(self, method, args, kwargs):
        url = f"{self.host}{self.base_url}{method}/{'/'.join(args)}"
        json_args = {k: v for k, v in kwargs.items() if v is not None}
        ret = self.session.post(url, json=json_args).content
        try:
            return json.loads(ret)
        except Exception as e:
            raise Exception(b'Error, returned:' + ret)



