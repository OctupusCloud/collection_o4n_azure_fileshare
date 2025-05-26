#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

__metaclass__ = type

DOCUMENTATION = """
---
module: o4n_azure_manage_share
short_description: Create or Delete a share in a Azure Storage File
description:
  - Connect to Azure Storage file using connection string method
  - Create a file share in a Storage File account when state param is eq to present
  - Delete a file share in a Storage File account when state param is eq to absent
version_added: "1.0"
author: "Ed Scrimaglia"
notes:
  - Testeado en linux
requirements:
  - ansible >= 2.10
  - Establecer `ansible_python_interpreter` a Python 3 si es necesario.
options:
  state:
    description:
      Create or delete a share
    required: false
    type: string
    choices:
        - present
        - absent
    default: present
  share:
    description:
      Name of the share to be managed
    required: true
    type: string
  connection_string:
    description:
      String that include URL & Token to connect to Azure Storage Account. Provided by Azure Portal
      Storage Account -> Access Keys -> Connection String
    required: true
    type: string
  account_name:
    description:
      Storage Account Name Provided by Azure Portal
    required: true
    type: string
"""

RETURN = """
output:
  description: List of shares created or deleted
  type: dict
  returned: allways
  sample: 
    output: {
      "changed": false,
      "content": {
          "share": "share-to-test"
      },
      "failed": false,
      "msg": "File Share <share-to-test> <created> in account <octionstorage>"
    }
"""

EXAMPLES = """
tasks:
  - name: Create a share
    o4n_azure_manage_share:
      account_name: "{{ account_name }}"
      share: share-to-test
      connection_string: "{{ connection_string }}"
    register: output

  - name: Delete a share
    o4n_azure_manage_share:
      account_name: "{{ account_name }}"
      state: absent
      share: share-to-test
      connection_string: "{{ connection_string }}"
    register: output
"""


from azure.storage.fileshare import ShareClient
from ansible.module_utils.basic import AnsibleModule
import azure.core.exceptions as aze

def create_client_with_connection_string(_conn_string):
        # Instantiate the ShareServiceClient from a connection string
        from azure.storage.fileshare import ShareServiceClient
        file_service = ShareServiceClient.from_connection_string(_conn_string)

def manage_share(_share, _conn_string, _account_name, _state):
    output = {"share": _share}
    action = "none"
    try:
        # Instantiate the ShareClient from a connection string
        share = ShareClient.from_connection_string(_conn_string, share_name=_share)
        # Create or Delete the share
        if _state.lower() == "present":
            share.create_share()
            action = "created"
        elif _state.lower() == "absent":
            share.delete_share()
            action = "deleted"
        status = True
        msg_ret = f"File Share <{_share}> <{action}> in account <{_account_name}>"
    except aze.ResourceExistsError:
        msg_ret = f"File Share <{_share}> not created in account <{_account_name}>. Error: <The specified resource already exist>"
        status = True
    except aze.ResourceNotFoundError:
        msg_ret = f"File Share <{_share}> not deleted in account <{_account_name}>. Error: <The specified resource does not exist>"
        status = True
    except Exception as error:
        msg_ret = f"Error managing File Share <{_share}> in <{_account_name}>. Error: <{error}>"
        status = False

    return status, msg_ret, output


def main():
    module=AnsibleModule(
        argument_spec=dict(
            account_name=dict(required=True, type='str'),
            state=dict(required=False, type='str', choices=["present", "absent"], default='present'),
            share=dict(required=True, type='str'),
            connection_string=dict(required= True, type='str'),
        )
    )

    state = module.params.get("state")
    share = module.params.get("share")
    connection_string = module.params.get("connection_string")
    account_name = module.params.get("account_name")

    create_client_with_connection_string(connection_string)
    success, msg_ret, output = manage_share(share,connection_string,account_name,state)
    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)


if  __name__ == "__main__":
    main()
