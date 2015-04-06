"""@package Data
Methods for IoT Analytics component type catalog
"""
from globals import *
from utils import *
import globals
import requests
import json


class ComponentCatalog:
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
