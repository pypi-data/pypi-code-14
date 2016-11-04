import urlparse, requests, json

class Bbug():
    def __init__(self, settings):

        bbug_ids = settings['Item']['bbug_company_id'].split('__')
        self.company_id=bbug_ids[1]
        settings=settings['Item']['bbug_app']

        url = settings['admin_endpoint'] +  '/login/admin'
        self.url = settings['admin_endpoint'] +  '/admin/'+ self.company_id


        payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n" +  settings['email'] + "\r\n-----011000010111000001101001\r\n Content-Disposition: form-data; name=\"password\"\r\n\r\n" + settings['password'] + "\r\n-----011000010111000001101001--"

        headers = {
                   'content-type': "multipart/form-data; boundary=---011000010111000001101001",
                    'App-Id': settings['app_id'],
                    'cache-control': "no-cache"
                    }

        self.response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(self.response.text)
        headers['auth-token']= data['auth_token']
        self.headers = headers

    def get_client(self, accountid):
        self.headers['content-type']='application/json; charset=utf-8'
        self.response = requests.request("GET",self.url +
                                         '/client/find_by_ref/' + accountid, headers=self.headers )
        if self.response.status_code ==200:
            data= json.loads(self.response.text)
        else:
            data= {}
        return data

    def save_client(self,account):

        client = {
            'last_name': account["name"],
            'email': account["emailaddress1"],
            'mobile': account["telephone1"],
            'address1': self.address1(account),
            'postcode': account["address1_postalcode"],
            'join_date': account["opendeals_date"],
            'country': account["address1_country"]
            }

        data = self.get_client(account['accountid'])

        if self.response.status_code == 200:
            self.update_client(client,data['id'])
            message = 'updated client: '
        elif self.response.status_code == 404:
            self.create_client(client,account['accountid'])
            message = 'created client: '
        else:
            raise RuntimeError("error to update account " +
                               account['accountid'])
        return [message + account['name']]

    def create_client(self, client,accountid):
        client['reference']=accountid
        client['member_type']= 2
        client['send_email']="false"
        client['member_level_id']= 0
        url = self.url + '/client'
        self.bbug_response = requests.request("POST", url, data=json.dumps(client),
                                         headers=self.headers)

    def update_client(self, client,clientid):
        url = self.url + '/client/' + `clientid`
        self.bbug_response = requests.request("PUT", url, data=json.dumps(client),
                                         headers=self.headers)

    def address1(self,account):
        address = account['address1_line1']
        if isinstance(account['address1_city'], basestring) :
            address+= ", " + account['address1_city']

        if 'address1_stateprovince' in account.keys() :
            address+= ", " + account['address1_stateprovince']
        return address



