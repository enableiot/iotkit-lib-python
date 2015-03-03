"""@package Data
Methods for IoT Analytics data transfer
"""
from globals import *
from utils import *
import requests
import time


class Data:

    def __init__(self, account):
        self.client = account.client
        self.account = account

    # def get_data(self, time0, time1, devices, components, output=None):
        # url = "{0}/accounts/{1}/data/search".format(self.client.base_url, self.account.id)
        # if output:
        # url += "?output=" + output
        # payload = {
        # "from": time0,
        # #"to": time1,
        # "targetFilter": {
        # "deviceList": None
        # },
        # "metrics": [
        # # {
        # # "id": "<component_id>",
        # # "op": "none" // currently it's the only value supported
        # # }
        # ]
        # }
        # if time1:
        # payload["to"] = time1
        # for c in components:
        # payload["metrics"].append({"id": c, "op": "none"})
        # payload["targetFilter"]["deviceList"] = devices
        # data = json.dumps(payload)
        # #print url, data
        # resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        # check(resp, 200)
        # if output:
        # return resp.text
        # else:
        # js = resp.json()
        # return js

    # def send(self, device, time, series):
        # url = "{0}/data/{1}".format(self.client.base_url, device.device_id)
        # if time == None:
        # time = time.now()
        # payload = {
        # "on": time,
        # "accountId": self.account.id,
        # "data": series
        # }
        # data = json.dumps(payload)
        # print url, data
        # resp = requests.post(url, data=data, headers=get_auth_headers(device.device_token), proxies=self.client.proxies, verify=g_verify)
        # check(resp, 201)
        # return resp.text

    # def advancedQuery(self, payload):
        # url = "{0}/accounts/{1}/data/search/advanced".format(self.client.base_url, self.account.id)

        # data = json.dumps(payload)
        # #print url, data
        # resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        # check(resp, 200)
        # js = resp.json()
        # return js

    # def report(self, payload, output=None):
        # url = "{0}/accounts/{1}/data/report".format(self.client.base_url, self.account.id)

        # data = json.dumps(payload)
        # #print url, data
        # resp = requests.post(url, data=data, headers=get_auth_headers(self.client.user_token), proxies=self.client.proxies, verify=g_verify)
        # check(resp, 200)
        # js = resp.json()
        # return js

    # def packageDataSeries(self, dataSeries, loc, cid):
        # packagedSeries = []
        # for time, value in dataSeries:
        # js = {
        # "componentId": cid,
        # "on":          time,
        # "value":       str(value)
        # }
        # if loc:
        # js["loc"] = loc

        # packagedSeries.append(js)
        # return packagedSeries
