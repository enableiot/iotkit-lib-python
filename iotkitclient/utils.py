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

import json
import time, re

def check(resp, code):
    if resp.status_code != code:
        raise RuntimeError(
            "Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text))


def get_auth_headers(token=None):
    headers = {
        #'Authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }
    if token:
        headers["Authorization"] = 'Bearer ' + token
    return headers


def prettyprint(js):
    print json.dumps(js, sort_keys=True, indent=4, separators=(',', ': '))


def update_properties(obj, var):
    if obj and var:
        for key, value in var.items():
            setattr(obj, key, value)
    else:
        raise ValueError("Invalid object %s or dictionary." %
                         (obj.__name__))

def convert_epoch(msecs, utc=False):
    secs = int(float(msecs)/1000)
    msecs = msecs - secs*1000
    #print '*****', x, secs, msecs
    if utc:
        return "%s.%03d" % (time.strftime("%m-%d-%Y %H:%M:%S", time.gmtime(secs)), int(msecs))
    else:
        return "%s.%03d" % (time.strftime("%m-%d-%Y %H:%M:%S", time.localtime(secs)), int(msecs))

def utc_to_epoch(utc):
    import datetime
    t = '2015-04-09T20:41:07.647Z'
    x = 1428612067
    d = re.split('[^\d]', t)[:-1]
    d[6] = str(int(d[6])*1000)
    d=datetime.datetime(*map(int, d))
    unix_epoch = datetime.datetime(1970, 1, 1)
    return (d - unix_epoch).total_seconds() * 1000

def utc_to_local(utc):
    msecs = utc_to_epoch(utc)
    return convert_epoch(msecs)