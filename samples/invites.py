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

# Connect and login to the IoT cloud
iot = iotkitclient.Request(host=config.hostname)
iot.login(config.username, config.password)
print "*** Connected. User ID: %s ..." % iot.user_id
acct = iot.account()
acct.get_account(config.account_name)
print "*** Using Account: %s (%s)" % (acct.id, config.account_name)
invite = acct.invites()

# Delete any pending invites
invite_list = invite.get_account_invites()
for user_email in invite_list:
    print "  *** Deleting old invites for", user_email
    invite.delete_invites(user_email)

# Display list of pending invites
invite_list = acct.invites().get_account_invites()
print "*** Pending invites for Account: %s" % config.account_name
for email in invite_list:
    print "   %s" % email

# Connect and login to IoT cloud as invitee
iot2 = iotkitclient.Request(host=config.hostname)
iot2.login(config.invitee_email, config.invitee_password)
acct2 = iot2.account()
invite2 = acct2.invites()

# find invite and accept
invite_list = invite2.get_user_invites(config.invitee_email)
for item in invite_list:
    invite_id = item["_id"]
    print "*** Accepting invite:", invite_id
    iotkitclient.prettyprint(invite2.accept_invite(invite_id))
    print "*** Deleting invites for:", config.invitee_email
    iotkitclient.prettyprint(invite.delete_invites(config.invitee_email))
