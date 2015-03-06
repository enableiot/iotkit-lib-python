"""@package Data
Methods for IoT Analytics user invites
"""
import globals
from utils import *
import requests
import uuid
import json
import urllib


class Invites:
    client = None
    acct = None

    def __init__(self, acct=None, client=None):

        if acct:
            self.client = acct.client
            self.account = acct
        elif client:
            self.client = client
        else:
            raise ValueError(
                "Either account or connection object is required.")

    def get_account_invites(self):
        url = "{0}/accounts/{1}/invites".format(
            self.client.base_url, self.account.id)
        resp = requests.get(url, headers=get_auth_headers(
            self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

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

    def add_invite(self, email):
        if email:
            url = "{0}/accounts/{1}/invites".format(
                self.client.base_url, self.account.id)
            payload = {
                "email": email
            }
            data = json.dumps(payload)
            resp = requests.post(url, data=data, headers=get_auth_headers(
                self.client.user_token), proxies=self.client.proxies, verify=globals.g_verify)
            check(resp, 201)
            js = resp.json()
        else:
            raise ValueError("No email provided.")

    def delete_invites(self, email):
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
