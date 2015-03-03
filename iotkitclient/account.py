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

"""@package Account
Methods for IoT Analytics account management
"""
import globals
from utils import check, get_auth_headers, update_properties
import requests
import json


class Account:
    """ Create IoT Account instance

        Args:
        client (obj): IoT client connection instance containing
        authorization token

    """
    id = None
    client = None
    info = None

    def __init__(self, client):
        self.client = client

    def create_account(self, account_name):
        """ Create a new account.

            Args:
            account_name (str): alias/name for account

            Returns:
            JSON message containing account attributes.
            Example:
                {
                    "name":"AccountName",
                    "healthTimePeriod":86400,
                    "created":1406919627586,
                    "updated":1406919627586,
                    "exec_interval":300,
                    "base_line_exec_interval":86400,
                    "cd_model_frequency":604800,
                    "cd_execution_frequency":600,
                    "data_retention":0,
                    "id":"321ef007-8449-477f-9ea0-d702d77e64b9"
                }

        """

        if account_name:
            url = "{0}/accounts".format(globals.base_url)
            payload = {"name": account_name}
            data = json.dumps(payload)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
            self.id = js["id"]
            #update_properties(self, js)  # save account properties
            self.info = js
            return js
        else:
            raise ValueError("No account name given.")

    def get_account(self, account_name, account_id=None):
        """ Look up account attributes for a given account and load instance
            attributes with returned values

            Args:
            account_name (str): alias/name of account to lookup (first match will be returned)
            account_id (str): use account ID (GUID) of account to help match

            Returns:
            account ID (str): Account ID (GUID) or matching account

        """

        if account_name:
            # given a user_id, get the account_id of the associated account with account_name
            # if there are multiple accounts with the same name, return one of
            # them
            url = "{0}/users/{1}".format(globals.base_url, self.client.user_id)
            resp = requests.get(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            if 'accounts' in js:
                accounts = js["accounts"]
                for key, value in accounts.iteritems():
                    if 'name' in value and value["name"] == account_name:
                        # if account_id is given, verify its value also
                        if account_id and account_id == key or not account_id:
                            self.id = key
                            return self.id
            msg = "Account name {0} not found.".format(account_name)
            msg = msg + "Available accounts are: {0}".format(
                [value["name"] for key, value in accounts.iteritems()])
            raise ValueError(msg)
        else:
            raise ValueError("No account name given.")

    def get_info(self):
        """ Return account attributes for a given account.

            Args:
            account_name (str): alias/name of account to lookup (first match will be returned)
            account_id (str): use account ID (GUID) of account to help match

            Returns:
            JSON message containing account information.
            Example:
                {
                    "name": "AccountName",
                    "healthTimePeriod": 86400,
                    "created": 1404415261310,
                    "updated": 1404415261310,
                    "exec_interval": 120,
                    "base_line_exec_interval": 86400,
                    "cd_model_frequency": 604800,
                    "cd_execution_frequency": 600,
                    "data_retention": 0,
                    "attributes":{
                        "phone":"123456789",
                        "another_attribute":"another_value"
                    },
                    "id": "321ef007-8449-477f-9ea0-d702d77e64b9"
                }

        """

        url = "{0}/accounts/{1}".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        #update_properties(self, js)  # save account properties
        self.info = js
        return js

    def update_account(self, acct_info):
        """ Update account attributes for current account instance

            Args:
            account_info (dict): A dict containing updated account attributes

            Returns:
            JSON message containing account attributes

        """
        data = json.dumps(acct_info)
        if acct_info:
            url = "{0}/accounts/{1}".format(globals.base_url, self.id)
            resp = requests.put(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            #update_properties(self, js)  # save account properties
            self.info = js
            return js
        else:
            raise ValueError("Invalid account info given.")

    def get_activation_code(self):
        """ Return previous activation code if it is still valid

        Returns:
        JSON message containing activation code and expiration time.
        Values will be "None" if the code has expired.
        Example,
            {
                "activationCode": "5nLyMJrh",
                "timeLeft": 1424731140
            }

        """
        url = "{0}/accounts/{1}/activationcode".format(
            globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"]

    def renew_activation_code(self):
        """ Return new activation code

        Returns:
        JSON message containing activation code and expiration time.
        Example,
            {
                "activationCode": "5nLyMJrh",
                "timeLeft": 1424731140
            }

        """
        url = "{0}/accounts/{1}/activationcode/refresh".format(
            globals.base_url, self.id)
        resp = requests.put(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js["activationCode"]

    def delete_account(self, account_id):
        """ Delete account with given account ID

            Args:
            account_id (str): account ID of account to delete

            Returns:
            No value is returned. A ValueError will be thrown if the device ID is invalid

        """
        if account_id:
            url = "{0}/accounts/{1}".format(globals.base_url, account_id)
            resp = requests.delete(url, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 204)
        else:
            raise ValueError("Invalid account ID.")

    def list_account_users(self):
        """ List all users associated with this account

            Returns:
            A list of user-attribute JSON messages
            Example,
                [
                    {
                        "id": "54e7cf2399fe4c41202e5b2f",
                        "accounts": {
                            "88f741fe-4087-42ef-a042-93c021e0148e": "admin"
                        },
                        "created": 1424477987329,
                        "email": "joetest@mycorp.com",
                        "termsAndConditions": true,
                        "updated": 1424478023196,
                        "verified": true
                    }
                ]

        """
        url = "{0}/accounts/{1}/users".format(globals.base_url, self.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def load_cert(self, infile):
        """

        """
        token = None
        json_data = open(infile).read()
        data = json.loads(json_data)
        if data["accountId"] == self.id:
            token = data["deviceToken"]
        return token

    def search_data(self, time0, time1, devices, components, csv=None):
        """ Retrieve data for a list of devices and components in a
            given time period.

            Args:
            time0 (int): beginning time
            time1 (int): ending time (None = current timestamp)
            devices (list of strings): list of devices IDs to return data for
            components (list of strings): list of component IDs to return data for
            csv (bool): return results in JSON or CSV format

            Returns:
            JSON or CSV message
                {
                    "from": 1234567890,
                    "to": 1234567890,
                    "maxPoints": 100,
                    "series": [
                        {
                            "deviceId": "D1",
                            "deviceName": "D1",
                            "componentId": "e3a48caa-e4c5-46bb-951e-8f9d0a4be516",
                            "componentName": "temp",
                            "componentType": "temperature.v1.0",
                            "points": [
                                {"ts":9874569871, "value":25},
                                {"ts":9874569899, "value":24}
                            ]
                        },
                        {
                            "deviceId": "D2",
                            "deviceName": "D2",
                            "componentId": "76a95112-2159-4ee6-8e91-6a69b9c51edc",
                            "componentName": "Humidity 1",
                            "componentType": "humidity.v1.0",
                            "points": [
                                {"ts":9874569871,"value":"55"},
                                {"ts":9874569899,"value":"65"}
                            ]
                        }
                    ]
                }

        """

        url = "{0}/accounts/{1}/data/search".format(globals.base_url, self.id)
        if csv:
            url = url + "?output=csv"
        payload = {
            "from": time0,
            "targetFilter": {
                "deviceList": devices
            },
            "metrics": []
        }
        if time1:
            payload["to"] = time1
        for c in components:
            payload["metrics"].append({"id": c, "op": "none"})
        payload["targetFilter"]["deviceList"] = devices
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        if csv:
            return resp.text
        else:
            js = resp.json()
            return js["series"]

    def advanced_data_query(self, payload):
        """ Advanced data query supports multiple filters and sorting options
        
            Args:
            payload (dict): dict containing iotkit REST API advanced-search
            parameters.

            Returns:
            JSON message containing returned data set
            
            See the Advanced Data Inquiry page on the iotkit REST API wiki for
            request and response message formats
            https://github.com/enableiot/iotkit-api/wiki/Advanced-Data-Inquiry
            
        """     
        url = "{0}/accounts/{1}/data/search/advanced".format(
            globals.base_url, self.id)

        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    def aggregated_report(self, payload):
        """ Return aggregated data report
        
            Args:
            payload (dict): dict containing iotkit REST API advanced-search
            parameters.

            Returns:
            JSON message containing returned data set
            
            See the Aggregated Report interface page on the iotkit REST API
            wiki for request and response message formats.
            https://github.com/enableiot/iotkit-api/wiki/Aggregated-Report-Interface
            
        """
        url = "{0}/accounts/{1}/data/report".format(globals.base_url, self.id)

        data = json.dumps(payload)
        # print url, data
        resp = requests.post(url, data=data, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    