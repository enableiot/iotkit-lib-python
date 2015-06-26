#!/usr/bin/env python
# Copyright (c) 2015, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of Intel Corporation nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""@package Data
Methods for IoT Analytics data transfer
"""
from globals import *
from utils import *
import requests
import time


class Data(object):

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
