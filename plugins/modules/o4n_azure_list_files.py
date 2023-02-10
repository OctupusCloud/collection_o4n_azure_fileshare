#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

__metaclass__ = type

DOCUMENTATION = """
---
module: o4n_azure_list_files
short_description: List Files in a File Share
description:
  - Connect to Azure Storage file using connection string method
  - List Files in a File Share
  - Return a list of Files in a File Share
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
      path, directory, whose files must be listed
    required: false
    type: string
"""

RETURN = """
output:
  description: List of files
  type: dict
  returned: allways
  sample: 
    output: {
      "changed": false,
      "content": [
          {
              "file_id": "9799948237879115776",
              "is_directory": false,
              "name": "o4n_azure_delete_files.py",
              "size": 12240
          },
          {
              "file_id": "16141016513216774144",
              "is_directory": false,
              "name": "o4n_azure_download_files.py",
              "size": 13353
          },
          {
              "file_id": "12682251999396233216",
              "is_directory": false,
              "name": "o4n_azure_manage_directory.py",
              "size": 9937
          },
          {
              "file_id": "10376408990182539264",
              "is_directory": false,
              "name": "o4n_azure_manage_shares.py",
              "size": 4359
          },
          {
              "file_id": "17293938017823621120",
              "is_directory": false,
              "name": "o4n_azure_upload_files.py",
              "size": 10611
          },
          {
              "file_id": "14988095008609927168",
              "is_directory": false,
              "name": "__init__.py",
              "size": 0
          }
      ],
      "failed": false,
      "msg": "List of Files created for Directory </dir1> in share <share-to-test2>"
    }
"""

EXAMPLES = """
tasks:
  - name: Delete files
    o4n_azure_list_files:
      account_name: "{{ account_name }}"
      connection_string: "{{ connection_string }}"
      share: "{{ share }}"
      path = /dir1/dir2
    register: output
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_list_files import list_files_in_share
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_get_right_path import right_path


def main():
  module = AnsibleModule(
    argument_spec=dict(
      account_name=dict(required=True, type='str'),
      share=dict(required=True, type='str'),
      connection_string=dict(required=True, type='str'),
      path=dict(required=False, type='str', default=''),
    )
  )

  share = module.params.get("share")
  connection_string = module.params.get("connection_string")
  account_name = module.params.get("account_name")
  path = module.params.get("path")
  path_sub, print_path = right_path(path)

  success, msg_ret, output = list_files_in_share(account_name, connection_string, share, path_sub, print_path)

  if success:
      module.exit_json(failed=False, msg=msg_ret, content=output)
  else:
      module.fail_json(failed=False, msg=msg_ret, content=output)


if __name__ == "__main__":
    main()