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

"""@package Device
Methods for IoT Analytics device management and data submission
"""
import globals
from utils import check, get_auth_headers
import requests
import json
import os.path
import time
import component


class Device(object):
    device_id = None
    client = None
    account = None
    device_token = None
    info = None
    account_id = None

    def __init__(self, id=None, account=None, client=None):
        if account:
            self.client = account.client
            self.account = account
            self.account_id = self.account.id
            if id:
                self.device_id = id
                try:
                    js = self.get_device()
                except Exception, err:
                    raise ValueError("Device ID not found: %s" % str(err))
        elif client:
            self.client = client
        else:
            raise ValueError("Account or connection object required.")

    def create_device(self, device_info, activate=False):
        if device_info:
            url = "{0}/accounts/{1}/devices".format(
                self.client.base_url, self.account_id)
            data = json.dumps(device_info)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            self.device_id = js["deviceId"]
            self.info = js
            if activate:
                activation_code = self.account.renew_activation_code()
                self.activate_new_device(activation_code)
            return js
        else:
            raise ValueError("No account name given.")

    def load_config(self, configFile):
        if os.path.isfile(configFile):
            js = open(configFile)
            data = json.load(js)
            self.info = data
            self.device_id = self.info["deviceId"]
            self.device_token = self.info["device_token"]
            self.account_id = self.info["account_id"]
            js.close()
            return data
        else:
            raise ValueError("Config file not found: ", configFile)

    def save_config(self, configFile, overWrite=False):
        if self.device_id:
            data = self.get_device()
            data["device_token"] = self.device_token
            data["account_id"] = self.account_id
        else:
            raise ValueError("Unknown device - no configuration to save.")

        try:
            if os.path.isfile(configFile) and not overWrite:
                raise RuntimeError(
                    "Cannot overwrite existing token file:", configFile)
            else:
                with open(configFile, 'w') as configFile:
                    json.dump(
                        data, configFile, sort_keys=True, indent=4, separators=(',', ': '))
        except:
            raise RuntimeError("Error writing token:", configFile)

    def get_device(self, device_id=None):
        if not device_id:
            device_id = self.device_id
        url = "{0}/accounts/{1}/devices/{2}".format(
            self.client.base_url, self.account_id, device_id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_id = js["deviceId"]
        self.info = js
        return js

    def update_device(self, device_info, device_id=None):
        if not device_id:
            device_id = self.device_id
        url = "{0}/accounts/{1}/devices/{2}".format(
            self.client.base_url, self.account_id, device_id)
        data = json.dumps(device_info)
        resp = requests.put(url, data=data, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.info = js
        return js

    def activate_new_device(self, activation_code):
        url = "{0}/accounts/{1}/devices/{2}/activation".format(
            self.client.base_url, self.account_id, self.device_id)
        activation = {
            "activationCode": activation_code
        }
        data = json.dumps(activation)
        resp = requests.put(url, data=data, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.device_token = js["deviceToken"]
        return self.device_token

    def delete_device(self, device_id=None):
        if not device_id:
            device_id = self.device_id
        if device_id:
            url = "{0}/accounts/{1}/devices/{2}".format(
                self.client.base_url, self.account_id, device_id)
            resp = requests.delete(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 204)
            self.device_id = None
            self.info = None
        else:
            raise ValueError("No active device selected.")

    def get_devices(self):
        """ List all users associated with this account

            Returns:
            A list of device-attribute JSON messages
            Example,
                [
                    {
                        "attributes": {
                            "agent_version": "1.5.1",
                            "hardware_vendor": "Genuine Intel(R) CPU   4000  @  500MHz",
                            "hardware_model": "linux",
                            "Model Name": "ia32",
                            "Firmware Version": "3.10.17-poky-edison+"
                        },
                        "created": 1424713173378,
                        "components": [
                            {
                                "name": "temp",
                                "type": "temperature.v1.0",
                                "cid": "f4f942c1-7d6f-4771-bbd4-9cfa9717ba5a"
                            }
                        ],
                        "deviceId": "jumbo-edison",
                        "gatewayId": "jumbo-edison",
                        "name": "jumbo-edison-NAME",
                        "status": "active"
                    }
                ]

        """
        url = "{0}/accounts/{1}/devices".format(
            self.client.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def get_tags(self):
        url = "{0}/accounts/{1}/devices/tags".format(
            self.client.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def get_attributes(self):
        url = "{0}/accounts/{1}/devices".format(
            self.client.base_url, self.account_id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def send_data(self, dataSeries):
        url = "{0}/data/{1}".format(self.client.base_url, self.device_id)
        payload = {
            "on": time.time(),
            "accountId": self.account_id,
            "data": dataSeries
        }
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.device_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 201)
        return resp.text

    def package_data_series(self, dataSeries, cid, loc=None):
        packagedSeries = []
        for timestamp, value in dataSeries:
            js = {
                "componentId": cid,
                "on": timestamp,
                "value": str(value)
            }
            if loc:
                js["loc"] = loc

            packagedSeries.append(js)
        return packagedSeries

    def component(self):
        __component = component.Component(device=self)
        return __component
