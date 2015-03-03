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

"""@package Client
Methods for IoT Analytics Cloud connections

"""
from utils import check, prettyprint, get_auth_headers
import globals
import json
import requests

class Connect:

    """ IoT Analytics Cloud connection class

    Attributes:
      proxies (str): proxy server used for connection
      user_token (str): access token from IoT Analytics site connection
      user_id (str): user ID for authenticated user
    """
    proxies = None
    user_token = ''
    user_id = ''
    base_url = globals.base_url
    
    def __init__(self, host=None, proxies=None):
        """ Creates IoT Analytics user session and sets up connection
        information (host, proxy connections)

        Args:
        ----------
        host (str, optional): IoT Analytics server address
        proxies (str, optional): list of proxy server addresses
          (e.g., {"https": "http://proxy-us.mycorp.com:8080"}

        """
        if host:
            self.base_url = "https://{0}{1}".format(host, globals.api_root)
            
        if proxies:
            self.proxies = proxies
        # test the connection
        try:
            js = self.get_version()
        except Exception, err:
            raise RuntimeError("Connection to %s failed: %s" % (self.base_url, str(err)))
        
    def login(self, username, password):
        """ Submit IoT Analytics user credentials to obtain the access token

        Args:
        ----------
        username (str): username for IoT Analytics site
        password (str): password for IoT Analytics site

        Returns:
        Sets user_id and user_token attributes for connection instance
        
        """
        if not username or not password:
            raise ValueError(
                "Invalid parameter: username and password required")

        try:
            url = "{0}/auth/token".format(self.base_url)
            headers = {'content-type': 'application/json'}
            payload = {"username": username, "password": password}
            data = json.dumps(payload)
            resp = requests.post(
                url, data=data, headers=headers, proxies=self.proxies, verify=globals.g_verify)
            check(resp, 200)
            js = resp.json()
            self.user_token = js['token']

            # get my user_id (uid) within the Intel IoT Analytics Platform
            js = self.get_user_tokeninfo()
            self.user_id = js["payload"]["sub"]

        except Exception, err:
            raise RuntimeError('Auth ERROR: %s\n' % str(err))

    # given a user token, get the user_id
    def get_user_tokeninfo(self):
        """ Get user token details

        Returns:
        --------
        JSON message containing access token details
        e.g.,
        Response 200 OK (application/json)
            {
                "header": {
                    "typ": "JWT",
                    "alg": "RS256"
                },
                "payload": {
                    "jti": "7b1430a2-dd61-4a47-919c-495cadb1ea7b",
                    "iss": "http://enableiot.com",
                    "sub": "53fdff4418b547e4241b8358",
                    "exp": "2014-10-02T07:53:25.361Z"
                }
            }

        """
        url = "{0}/auth/tokenInfo".format(self.base_url)
        resp = requests.get(url, headers=get_auth_headers(self.user_token),
                            proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    # Health API
    def get_version(self):
        """ Get Cloud version and health information

        Returns:
        --------
        {
            "kind": "healthcheck",
            "isHealthy": true,
            "currentSetting": "prod",
            "name": "iotkit-dashboard",
            "build": "0.12.2",
            "date": "2015-02-19T15:11:05.907Z",
            "items": []
        }

        """
        url = "{0}/health".format(self.base_url)
        headers = {'content-type': 'application/json'}
        resp = requests.get(
            url, headers=headers, proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        return js

    # Re-initialize to get new token (use after creating a new account)
    def reinit(self, username, password):
        """ Re-authenticate to obtain new access token

        Args:
        -----
          username (str): username for IoT Analytics site
          password (str): password for IoT Analytics site

        Returns:
          user_token (str): updated access token

        """
        if not username or not password:
            raise ValueError("Invalid parameter: reinit(username, password)")
        url = "{0}/auth/token".format(self.base_url)
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(
            url, data=data, headers=headers, proxies=self.proxies, verify=globals.g_verify)
        check(resp, 200)
        js = resp.json()
        self.user_token = js['token']
