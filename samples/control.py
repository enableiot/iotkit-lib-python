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
import json

# actuation message bodymsg
msg = {
    "complexCommands": [],
    "commands": [{
        "transport": "ws",
        "componentId": None,
        "parameters": [{
            "name": "LED",
                    "value": None
        }]
    }]
}

# Connect to IoT Analytics site and authenticate
print "Connecting to %s ..." % config.hostname
iot = iotkitclient.Request(host=config.hostname)
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

device_id = iot.user_id + "_01"

# Link to a specific device in the account
device = acct.device()
try:
    device.get_device(device_id)
except:
    device_info = {
        "deviceId": device_id,
        "gatewayId": device_id,
        "name": "Device #1"
    }
    device.create_device(device_info)
    act_code = acct.renew_activation_code()
    device.activate_new_device(act_code)
    device.save_config("device.json", True)

device.load_config("device.json")
print "Using Device: %s ..." % device_id

# Set up actuator component - if it doesn't exist
cname = "motor"
ctype = "powerswitch.v1.0"
comp = device.component()
if comp.get_component(cname):
    print "Found component:", comp.id
else:
    comp.add_component(cname, ctype)

# Set up actuation message
msg["commands"][0]["componentId"] = str(comp.id)
msg["commands"][0]["parameters"][0]["value"] = "1"
print "*** Sending actuation message:"
iotkitclient.prettyprint(msg)
acct.send_control_msg(msg)

# List actuation history for this device
print "*** Listing actuation history:"
start_time = 0
js = acct.list_control_msgs(device_id, start_time)
iotkitclient.prettyprint(js)
