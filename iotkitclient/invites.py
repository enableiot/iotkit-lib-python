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
