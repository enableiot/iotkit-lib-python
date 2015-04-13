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
#iot.login(config.username, config.password)
print "*** Connected but not logged in."

# Get user object
user = iot.user()

email = config.username
password = config.password

# login as new user
iot.login(email, password)
user_id = iot.user_id

# get user info
print "** Getting user information"
info = user.get_user_info(user_id)
iotkitclient.prettyprint(info)

# update user
user_info = {
    "id": user_id,
    "attributes":{
        "phone":"123456789",
        "test_attrib1":"test_value1",
        "new":"next_string_value"
    }
}
print "** Updating user information"
user.update_user(user_info)
info = user.get_user_info(user_id)
iotkitclient.prettyprint(info)

# change user password
newpassword = "Woo45oo"
user.change_password(email, password, newpassword)
# login with new password
iot.login(email, newpassword)

# Request a password reset
print "** Requesting password reset..."
user.request_password_reset(email)
print "Please check your email for a reset token"
reset_token = raw_input("Enter the reset_token from the link in the password reset email (...?token=<reset_token>) and press [Enter] to continue.")
user.reset_password(reset_token, password)
print "   Password reset."

# login with reset password
iot.login(email, password)

# Delete test user
#print "** Deleting test user %s (%s)" % (email, user_id)
#user.delete_user(user_id)




