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


class Alert:

    def __init__(self, acct):
        self.client = acct.client
        self.account = acct

    # Get alerts for an account
    def get_alerts(self):
        url = "{0}/accounts/{1}/alerts".format(
            self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    # Get alert information - for a specific alert
    def get_alert(self, alert_id):
        if alert_id is not None:
            url = "{0}/accounts/{1}/alerts/{2}".format(
                self.client.base_url, self.account.id, alert_id)
            resp = requests.get(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            return js
        else:
            raise ValueError("alert-ID required.")

    # Reset alert
    def reset_alert(self, alert_id):
        if alert_id is not None:
            url = "{0}/accounts/{1}/alerts/{2}/reset".format(
                self.client.base_url, self.account.id, alert_id)
            resp = requests.put(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("alert-ID required.")

    # Update alert status
    def update_alert_status(self, alert_id, alert_status):
        if alert_id is not None and alert_status is not None:
            url = "{0}/accounts/{1}/alerts/{2}/status/{3}".format(
                self.client.base_url, self.account.id, alert_id, alert_status)
            resp = requests.put(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("alert-ID and status are required.")

    # Add comments to an alert
    def add_alert_comment(self, alert_id, alert_comment):
        if alert_id is not None and alert_comment is not None:
            url = "{0}/accounts/{1}/alerts/{2}/comments".format(
                self.client.base_url, self.account.id, alert_id, alert_status)
            data = json.sumps(alert_comment)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
        else:
            raise ValueError("alert-ID and comment are required.")
