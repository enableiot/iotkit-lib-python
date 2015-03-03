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

"""@package User
Methods for IoT Analytics user management
"""
import globals
from utils import *
import requests
import json


class User:
    id = None
    client = None

    def __init__(self, client):
        self.client = client
        js = client.get_user_tokeninfo()
        if js["payload"]["sub"]:
            self.id = js["payload"]["sub"]

    def add_user(self, email, password, toc=True):
        if email and password:
            # given a user_id, get the user's info
            # if toc:
                # toc = "true"
            # else:
                # toc = "false"
            payload = {
                "email": email,
                "password": password,
                "termsAndConditions": toc
            }
            url = "{0}/users".format(globals.base_url)
            data = json.dumps(payload)
            # prettyprint(data)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            self.id = js["id"]
            return js
        else:
            raise ValueError("Invalid username or password.")
        return None

    def get_user_info(self):
        # Get the user's info
        url = "{0}/users/{1}".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def delete_user(self, user_id):
        # Get the user's info
        url = "{0}/users/{1}".format(globals.base_url, user_id)
        resp = requests.delete(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 204)

    def update_user(self, user_info):
        if user_info:
            # given a user_id, get the user's info
            url = "{0}/users/{1}".format(globals.base_url, self.id)
            data = json.dumps(user_info)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("No user info given.")
        return None

    def change_password(self, username, oldpassword, newpassword):
        if username and oldpassword and newpassword:
            # given a user_id, get the user's info
            url = "{0}/users/{1}/change_password".format(
                globals.base_url, username)
            payload = {
                "currentpwd": oldpassword,
                "password": newpassword
            }
            data = json.dumps(payload)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("No username, old or new password given.")
        return None

    def find_accounts(self, account_name, firstAccountOnly=True):
        accounts = []
        if account_name:
            js = self.get_info()
            if js["accounts"]:
                for account, value in js["accounts"].items():
                    if value["name"] == account_name:
                        accounts.append(account)
        else:
            raise ValueError("No account_name given.")

        if firstAccountOnly:
            return accounts[0]
        return accounts
        
    def change_password(self):
        pass
        
    def update_user_role(self):
        pass
        
    def reset_password(self):
        pass
        
    def request_password_reset(self):
        pass
