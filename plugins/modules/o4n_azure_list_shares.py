#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

__metaclass__ = type

DOCUMENTATION = """
---
module: o4n_azure_list_shares
short_description: List File Shares in Storage Account
description:
  - Connecto to Azure Storage file using connection string method
  - List File Shares in service
  - Return a list of Shares in Service
version_added: "1.0"
author: "Ed Scrimaglia"
notes:
  - Testeado en linux
requirements:
  - ansible >= 2.10
options:
  connection_string:
    description:
      - String that include URL & Token to connect to Azure Storage Account. Provided by Azure Portal
      - Storage Account -> Access Keys -> Connection String
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
  description: List of shares
  type: dict
  returned: allways
  sample: 
    output: {
      "changed": false,
      "content": [
          "automation-filesharing",
          "share-bp-cu3",
          "share-to-test",
          "share-to-test2"
      ],
      "failed": false,
      "msg": "List of Shares created in account <octionstorage>"
    }
"""

EXAMPLES = """
tasks:
  - name: Delete files
    o4n_azure_list_shares:
      account_name: "{{ account_name }}"
      connection_string: "{{ connection_string }}"
    register: output
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_list_shares import list_shares_in_service


def main():
    module=AnsibleModule(
        argument_spec=dict(
            account_name=dict(required=True, type='str'),
            connection_string=dict(requiered=True, type='str')
        )
    )

    connection_string = module.params.get("connection_string")
    account_name = module.params.get("account_name")
    
    success, msg_ret, output = list_shares_in_service(account_name, connection_string)

    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)


if __name__ == "__main__":
    main()