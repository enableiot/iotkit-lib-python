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
import random

# Connect and login to the IoT cloud
iot = iotkitclient.Request(host=config.hostname)
iot.login(config.username, config.password)
print "*** Connected. User ID: %s ..." % iot.user_id

# Get account object for test account
acct = iot.account()
acct.get_account(config.account_name)
print "*** Using Account: %s (%s)" % (acct.id, config.account_name)

# Get component type catalog object for test account
catalog = acct.component_catalog()
print "*** Listing existing Component Catalog"
# find latest temperature sensor version
sensor_version = "1.0"
sensor_type = "temperature"
for type in catalog.get_comp_types():
    print type["id"]
    if (type["dimension"] == sensor_type and
       type["version"] is not None):
        if type["version"] >= sensor_version:
            sensor_version = type["version"]
# increment sensor version
sensor_version = float(sensor_version) + 0.1

# Define new component type properties
comp_type_id = sensor_type + ".v" + str(sensor_version)
comp_type_info = {
                    "dimension": sensor_type,
                    "version": str(sensor_version),
                    "type": "sensor",
                    "dataType":"Number",
                    "format": "float",
                    "min": -150,
                    "max": 150,
                    "measureunit": "Degress Celsius",
                    "display": "timeSeries"
                 }

print "*** Adding new component type (%s) to Component Catalog" % comp_type_id
# Create new component type
info = catalog.add_comp_type(comp_type_info)
iotkitclient.prettyprint(info)

# Update new component (sensor version will be incremented)
sensor_version = float(sensor_version) + 0.1
new_comp_type_id = sensor_type + ".v" + str(sensor_version)
print "*** Updating component type (%s) in Component Catalog..." % comp_type_id
print "    ...will create %s" % new_comp_type_id

# Create random min/max sensor values
max = int(random.random()*100)
new_info = {
    "max": max,
    "min": -1 * max
}
print "    min: %d" % new_info["min"]
print "    max: %d" % new_info["max"]
info = catalog.update_comp_type(comp_type_id, new_info)
iotkitclient.prettyprint(info)

print "*** Get component type (%s) details:" % new_comp_type_id
info = catalog.get_comp_type(new_comp_type_id)
iotkitclient.prettyprint(info)


