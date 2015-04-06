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

# Get list of rules and print details for each one

import iotkitclient
import config
import time
import json
import random

rule_name = "Test Rule " + str(int(random.random() * 100000))

iot = iotkitclient.Request(host=config.hostname)
iot.login(config.username, config.password)
print "*** Connected. User ID: %s ..." % iot.user_id
acct = iot.account()
acct.get_account(config.account_name)
rule = acct.rule()
rule_info = {
    "name": rule_name,
    "description": "This is a test rule",
    "priority": "Medium",
    "type": "Regular",
    "status": "Active",
    "actions": [
            {
                "type": "http",
                "target": [
                    "http://test.com"
                ],
                "http_headers":
                {
                    "header1": "value1",
                    "header2": "value2"
                }
            }
    ],
    "conditions": {
        "operator": "OR",
        "values": [
            {
                    "component": {
                        "dataType": "Number",
                        "name": config.component_name
                    },
                "type": "basic",
                "values": [
                        "65.0"
                    ],
                "operator": ">"
            }
        ]
    },
    "resetType": "Automatic",
    "population": {
        "ids": [
            "685.1.1.1"
        ],
        "attributes": None
    }
}

rule.add_rule(rule_info)

rules = rule.get_rules()
for r in rules:
    if r["name"] == rule_name:
        id = r["externalId"]
        info = rule.get_rule(id)
        iotkitclient.prettyprint(info)
        print "*** Updating Rule %s" % id
        rule_info["description"] = "This is an updated rule"
        try:
            rule.update_rule(rule_info)
            rule.update_rule_status("Archived")
        except:
            pass
        iotkitclient.prettyprint(rule.get_rule(id))

rule.update_rule_status("Active")
