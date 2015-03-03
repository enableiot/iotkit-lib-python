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
    
device_id = iot.user_id + "_01"
device = iotkitclient.Device(acct, device_id)
comp = iotkitclient.Component(device)
comp.get_component(config.component_name)

t0 = 0
t1 = None
devices = [device_id]
components = [comp.id]
data = acct.search_data(t0, t1, devices, components, csv=False)
print "\nSimple query..."
iotkitclient.prettyprint(data)

data = acct.search_data(t0, t1, devices, components, csv=True)
print "\nSimple query (CSV format)..."
iotkitclient.prettyprint(data)

print "\nAdvanced query..."
# filters = {
    # "gatewayIds" : ["<gid1>", "<gid2>"],
    # "deviceIds" : ["<did1>", "<did2>"],
    # "componentIds" : ["<cid1>", "<cid2>"],
    # "from" :  <start_datetime>,
    # "to" :  <end_datetime>,
    # "returnedMeasureAttributes" : ["att_1", "att_2"],
    # "showMeasureLocation" :  <true/false>,
        # "aggregations":<include/exclude/only>,
    # "devCompAttributeFilter" : {
        # "filterName1" : ["filter_value1", "filter_value2"],
        # "filterName2" : ["filter_value1", "filter_value2"]
    # },
    # "measurementAttributeFilter" : {
        # "filterName1" : ["filter_value1", "filter_value2"],
        # "filterName2" : ["filter_value1", "filter_value2"]
    # },
    # "valueFilter" : {
        # "value" : ["filter_value1", "filter_value2"]
    # },
    # "componentRowLimit" :  <limit_value>,
    # "countOnly" :  <true/false>,
    # "sort" : [{
            # "sortField1" : "<sort_order>"
        # }, {
            # "sortField2" : "<sort_order>"
        # }       
    # ]
# }
filters = {
            "from" :  0,
            "devCompAttributeFilter" : {
                "componentType" : ["temperature.v1.0"]
            },
            "componentRowLimit" :  1,
            "sort" : [{"Timestamp" : "Desc"}]
        }
data = acct.advanced_data_query(filters)
iotkitclient.prettyprint(data)



    

    
    
    
