#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

__metaclass__ = type

DOCUMENTATION = """
---
module: o4n_azure_list_directories
short_description: List Directories in a File Share
description:
  - Connect to Azure Storage file using connection string method
  - List Directories in a File Share
  - Return a list of Directories in a File Share
version_added: "1.0"
author: "Ed Scrimaglia"
notes:
  - Testeado en linux
requirements:
  - ansible >= 2.10
options:
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
  share:
    description:
      Name of the share to be managed
    required: true
    type: string
  path:
    description:
      path, directory, whose directories must be listed. If not present, path is the root of the File Share
    required: false
    type: string
"""

RETURN = """
output:
  description: List of Directories
  type: dict
  returned: allways
  sample: 
    output: {
      "changed": false,
      "content": [
          {
              "file_id": "13835104234770530304",
              "is_directory": true,
              "name": "dir1"
          },
          {
              "file_id": "13835121826956574720",
              "is_directory": true,
              "name": "Dir2"
          }
      ],
      "failed": false,
      "msg": "List of Directories created for Directory </> in share <share-to-test2>"
    }
"""

EXAMPLES = """
tasks:
  - name: Delete files
    o4n_azure_list_directories:
      account_name: "{{ account_name }}"
      connection_string: "{{ connection_string }}"
      share: "{{ share }}"
      path = /dir1/dir2
    register: output

  - name: Delete files
    o4n_azure_list_directories:
      account_name: "{{ account_name }}"
      connection_string: "{{ connection_string }}"
      share: "{{ share }}"
    register: output
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.escrimaglia.o4n_azure_storagefile_test.plugins.module_utils.util_list_shares import list_shares_in_service
from ansible_collections.escrimaglia.o4n_azure_storagefile_test.plugins.module_utils.util_list_directories import list_directories_in_share
from ansible_collections.escrimaglia.o4n_azure_storagefile_test.plugins.module_utils.util_get_right_path import right_path


def main():
    module=AnsibleModule(
        argument_spec=dict(
            account_name=dict(required=True, type='str'),
            share=dict(required=True, type='str'),
            connection_string=dict(required=True, type='str'),
            path=dict(required=False, type='str'),
        )
    )

    share = module.params.get("share")
    connection_string = module.params.get("connection_string")
    account_name = module.params.get("account_name")
    path = module.params.get("path")
    path_sub = right_path(path)

    success, msg_ret, output = list_directories_in_share(account_name, connection_string, share, path_sub)

    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)


if __name__ == "__main__":
    main()
