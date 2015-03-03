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

import globals
from utils import *
import requests
import uuid
import json

class Component:

    def __init__(self, device):
        self.client = device.client
        self.account = device.account
        self.device = device
        self.id = None

    def get_component(self, component_name, cid=None):
        info = self.device.get_device()
        if 'components' in info:
            components = info["components"]
            for c in components:
                # return first matching component
                if c['name'] == component_name:
                    if cid and cid != c['cid']:
                        continue
                    self.id = c['cid']
                    self.name = c['name']
                    return c
        return None

    def add_component(self, name, type):
        cid = str(uuid.uuid4())
        payload = {
            "cid": cid,
            "name": name,
            "type": type
        }
        url = "{0}/accounts/{1}/devices/{2}/components".format(
            globals.base_url, self.account.id, self.device.device_id)
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.device.device_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 201)
        js = resp.json()
        self.id = cid
        self.name = name
        self.type = type
        return js

    def delete_component(self, cid):
        url = "{0}/accounts/{1}/devices/{2}/components/{3}".format(
            globals.base_url, self.account.id, self.device.device_id, cid)
        resp = requests.delete(url, headers=get_auth_headers(
            self.device.device_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 204)
