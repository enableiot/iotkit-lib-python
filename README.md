PROJECT NOT UNDER ACTIVE MANAGEMENT

This project will no longer be maintained by Intel.

Intel has ceased development and contributions including, but not limited to, maintenance, bug fixes, new releases, or updates, to this project.  

Intel no longer accepts patches to this project.

If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the open source software community, please create your own fork of this project.  

Contact: webadmin@linux.intel.com
# iotkit-lib-python
Thie library provides Python bindings to the [IoT Analytics REST API](https://github.com/enableiot/iotkit-api/wiki/Api-Home "").

## Installation
1. Clone the iotkit-lib-python repository from GitHub
2. Install the library:

   ``` bash
cd iotkit-lib-python
python setup.py install
```

## API Guide

The library provides 6 classes
* Connect
* Account
* Device
* Component
* Alert
* Rule
* Control

### Request
IoT Analytics Request class
```
request_obj = Request(host, proxies=None, username=None, password=None)
get_user_tokeninfo():
get_version():
login(username, password):
reinit(username, password):
account(): create Account object
user(): create User object
invites(): create Invite object

```

### Account
IoT Analytics Account Management class
```

advanced_data_query(payload):
aggregated_report(payload):
create_account(account_name):
delete_account(account_id):
get_account(account_name, account_id=None):
get_activation_code():
get_info():
list_account_users():
list_control_msgs(device_id, start_time=0):
load_cert(infile):
renew_activation_code():
search_data(time0, time1, devices, components, csv=None):
send_control_msg(payload):
update_account(acct_info):
device(): create Device object
alert(): create Alert object
rule(): create Rule object
invites(): create Invite object
user(): create User object
componentCatalog(): create ComponentCatalog object
```
### Alert
IoT Analytics Alert class
```

add_alert_comment(alert_id, alert_comment):
get_alert(alert_id):
get_alerts():
reset_alert(alert_id):
update_alert_status(alert_id, alert_status):
```

### Component
IoT Analytics Component (Sensor) class
```

def add_component(self, name, type):
delete_component(self, cid):
get_component(self, component_name, cid=None):
```

### ComponentCatalog
IoT Analytics Component Catalog class
```

add_comp_type():
get_comp_type():
get_comp_types():
update_comp_type():
```

### Device 
IoT Analytics Device class
```

activate_new_device(activation_code):
create_device(device_info, activate=False):
delete_device(device_id=None):
get_attributes():
get_device(device_id=None):
get_devices():
get_tags():
load_config(configFile):
package_data_series(dataSeries, cid, loc=None):
save_config(configFile, overWrite=False):
send_data(dataSeries):
update_device(device_info, device_id=None):

component() - Create Component object
```

### Invites
IoT Analytics Invites class
```

accept_invite(email):
add_invite(email):
delete_invites(email):
get_account_invites():
get_user_invites(email):
```

### Rules
IoT Analytics Rules class
```

add_draft_rule(rule_info):
add_rule(rule_info):
delete_draft_rule(rule_id):
find_rule(rule_name):
get_rule(rule_id):
get_rules():
update_rule(rule_info):
update_rule_status(rule_status):
```

### User
IoT Analytics User Management class
```

add_user(email, password, toc=True)
get_user_info(user_id)
delete_user(user_id)
update_user(user_info)
change_password(username, oldpassword, newpassword)
reset_password(reset_token=None, newpassword)
request_password_reset(email)
```


