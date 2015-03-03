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
iot = iotkitclient.Connect(host=config.hostname, proxies=config.proxies)
iot.login(config.username, config.password)

# Create IoT Analytics account instance
acct = iotkitclient.Account(iot)
try:
    # Check if account exists
    acct.get_account(config.account_name)
except Exception, err:    
    raise RuntimeError("Unable to find account %s" % str(err))
    
# Link-to/Create a specific device in the account
device = iotkitclient.Device(acct)
device_id = iot.user_id + "_01"

try:
    # Check if device exists
    device.get_device(device_id)
except:
    # Define required device info parameters
    device_info = {
                    "deviceId": device_id, 
                    "gatewayId": device_id,
                    "name": "Device #1"
                  }
    # Create device
    print "Creating new device:", device_id
    device.create_device(device_info)
    # Obtain activation code
    act_code = acct.renew_activation_code()
    # Activate device
    device.activate_new_device(act_code)
    # Save device token to file **DO NOT LOSE THIS TOKEN**
    print "Writing device token to device.json..."
    device.save_config("device.json", True)
    
print "Device Info:"
iotkitclient.prettyprint(device.get_device())

print "Update Device Info:"
device_info = {
                "name": "Just changed my name"
              }
device.update_device(device_info, device_id)
iotkitclient.prettyprint(device.get_device())


    

    
    
    
