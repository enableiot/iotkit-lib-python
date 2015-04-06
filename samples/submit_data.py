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

import iotkitclient
import config
import time

# Connect to IoT Analytics site and authenticate
print "Connecting to %s ..." % config.hostname
iot = iotkitclient.Request(host=config.hostname, proxies=config.proxies)
iot.login(config.username, config.password)
print "Connected. User ID: %s ..." % iot.user_id

# Link to a specific IoT Analytics account
acct = iot.account()
try:
    acct.get_account(config.account_name)
except:
    acct.create_account(config.account_name)
    iot.reinit(config.username, config.password)
print "Using Account: %s ..." % config.account_name

# Link to a specific device in the account
device = acct.device()
device_id = iot.user_id + "_01"
try:
    device.get_device(device_id)
except Exception, ex:
    raise RuntimeError(str(ex))

device.load_config("device.json")
print "Using Device: %s ..." % device_id

comp = device.component()
if not comp.get_component(config.component_name):
    comp.add_component(config.component_name, config.component_type)

print "Using Component: %s (%s) ..." % (config.component_name, comp.id)

data = [
    (int(time.time() * 1000 - 500), "65.3"),
    (int(time.time() * 1000 - 400), "57.5"),
    (int(time.time() * 1000 - 300), "61.4"),
    (int(time.time() * 1000 - 200), "59.2"),
    (int(time.time() * 1000 - 100), "66.5"),
    (int(time.time() * 1000), "65.3")
]
dataseries = device.package_data_series(data, comp.id)
device.send_data(dataseries)
print "Submitted data: "
iotkitclient.prettyprint(dataseries)

# save latest device-info
device.get_device(device_id)
device.save_config("device.json", True)
