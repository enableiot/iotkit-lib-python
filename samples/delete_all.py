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

# Link to a specific IoT Analytics account
acct = iotkitclient.Account(iot)
try:
    acct.get_account(config.account_name)

    # Link to a specific device in the account
    device = iotkitclient.Device(acct)
    device_id = iot.user_id + "_01"
    try:
        device.get_device(device_id)
        
        # Delete all components named "temp" on this device
        comp = iotkitclient.Component(device)
        while True:
            try:
                comp.get_component(config.component_name)
                print "Deleting component \"%s\" (%s)" % (config.component_name, comp.id)
                comp.delete_component(comp.id)
            except:
                break 

        # Delete device
        print "Deleting device \"%s\"" % device_id
        device.delete_device(device_id)
        
    except:        
        print "Cannot find device: %s ..." % device_id
        
    # Delete account
    print "Deleting account \"%s\" (%s)" % (config.account_name, acct.id)
    acct.delete_account(acct.id)
    pass
except:
    print "Cannot find account: %s ..." % config.account_name