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
Methods for IoT Analytics user invites
"""
import globals
from utils import check, get_auth_headers
import requests
import json
import urllib


class Invites(object):
    client = None
    acct = None

    def __init__(self, account=None, client=None):

        if account:
            self.client = account.client
            self.account = account
        elif client:
            self.client = client
        else:
            raise ValueError(
                "Either account or connection object is required.")

    def get_account_invites(self):
        if self.account:
            url = "{0}/accounts/{1}/invites".format(
                self.client.base_url, self.account.id)
            resp = requests.get(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            return js
        else:
            raise ValueError("No account provided.")

    def get_user_invites(self, email):
        if email:
            url = "{0}/invites/{1}".format(
                self.client.base_url, urllib.quote(email))
            resp = requests.get(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            return js
        else:
            raise ValueError("No email provided.")

    def delete_invites(self, email):
        if self.account:
            if email:
                url = "{0}/accounts/{1}/invites/{2}".format(
                    self.client.base_url, self.account.id, urllib.quote(email))
                resp = requests.delete(url, headers=get_auth_headers(
                    self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
                check(resp, 200)
                js = resp.json()
                return js
            else:
                raise ValueError("No email provided.")
        else:
            raise ValueError("No account provided.")

    def accept_invite(self, email):
        if email:
            url = "{0}/invites/{1}/status".format(
                self.client.base_url, email)
            payload = {
                "accept": True
            }
            data = json.dumps(dict(payload))
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            return js
        else:
            raise ValueError("No email provided.")
