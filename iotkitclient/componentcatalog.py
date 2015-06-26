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
Methods for IoT Analytics component type catalog
"""
from globals import *
from utils import check, get_auth_headers
import globals
import requests
import json


class ComponentCatalog(object):
    account = None

    def __init__(self, account=None):
        self.account = account
        self.client = account.client

    def add_comp_type(self, component_info=None):
        if component_info:
            url = "{0}/accounts/{1}/cmpcatalog".format(self.client.base_url,
                                                       self.account.id)
            data = json.dumps(component_info)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            return js
        else:
            raise ValueError("No component info given.")

    def get_comp_types(self, full=False):
        url = "{0}/accounts/{1}/cmpcatalog".format(self.client.base_url,
                                                   self.account.id)
        if full == True:
            url += "?full=true"
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def get_comp_type(self, component_id):
        if component_id:
            url = "{0}/accounts/{1}/cmpcatalog/{2}".format(self.client.base_url,
                                                           self.account.id,
                                                           component_id)
            resp = requests.get(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            #check(resp, 200)
            if resp.status_code == 404:
                return None
            js = resp.json()
            return js
        else:
            raise ValueError("No component ID given.")

    def update_comp_type(self, component_id=None, component_info=None):
        if component_id:
            if component_info:
                url = "{0}/accounts/{1}/cmpcatalog/{2}".format(self.client.base_url,
                                                               self.account.id,
                                                               component_id)
                data = json.dumps(component_info)
                resp = requests.put(url, data=data, headers=get_auth_headers(
                    self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
                check(resp, 201)
                js = resp.json()
                return js
            else:
                raise ValueError("No component info given.")
        else:
            raise ValueError("No component_id given.")
