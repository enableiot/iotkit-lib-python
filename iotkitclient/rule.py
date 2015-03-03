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

class Rule:
    rule_id = None

    def __init__(self, acct):
        self.client = acct.client
        self.account = acct

    def get_rules(self):
        """ Get list of rules for this account """
        url = "{0}/accounts/{1}/rules".format(
            self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js
        
    def find_rule(self, rule_name):
        """ Create a rule as a draft """
        js = self.list_rules()
        for row in js:
            print row["name"]
            if row["name"] == rule_name:
                prettyprint(row)
                return row["externalId"]
        
    def add_draft_rule(self, rule_info):
        """ Create a rule as a draft """
        if rule_info:
            url = "{0}/accounts/{1}/rules/draft".format(
                self.client.base_url, self.account.id)
            data = json.dumps(rule_info)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
        else:
            raise ValueError("No rule information provided.")
    def delete_draft_rule(self, rule_id):
        """ Delete a draft rule """
    def get_rule(self, rule_id):
        """ Get single rule """
    def add_rule(self, rule_info):
        """ Create a rule """
        if rule_info:
            url = "{0}/accounts/{1}/rules".format(
                self.client.base_url, self.account.id)
            data = json.dumps(rule_info)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
        else:
            raise ValueError("No rule information provided.")
            
    def update_rule(self, rule_info):
        """ Update a rule """
        if rule_info:
            url = "{0}/accounts/{1}/rules/{2}".format(
                self.client.base_url, self.account.id, self.rule_id)
            data = json.dumps(rule_info)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
        else:
            raise ValueError("No rule information provided.")
            
    def update_rule_status(self, rule_status):
        """ Update a rule status """
        if rule_status:
            url = "{0}/accounts/{1}/rules/{2}/status".format(
                self.client.base_url, self.account.id, self.rule_id)
            payload = { "status": rule_status }
            data = json.dumps(payload)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
        else:
            raise ValueError("No rule information provided.")


