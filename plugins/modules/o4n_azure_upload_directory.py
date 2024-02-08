#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

__metaclass__ = type

DOCUMENTATION = """
---
module: o4n_azure_upload_directory
short_description: Upload a Directories/Sub Directory to a Storage File
description:
  - Connect to Azure Storage file using connection string method
  - Create a Directory and upload all files in a share in a Storage File account 
version_added: "2.0"
author: "Ed Scrimaglia"
notes:
  - Testeado en linux
requirements:
  - ansible >= 2.10
options:
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
  parent_path:
    description:
      full parent path where directory will be created
    required: false
    type: string
  source_path:
    description:
      path, local directory where files to be uploaded are
    required: true
    type: string
  dest_path:
    description:
      directory to create where files should be uploaded
    required: true
    type: string
  files:
    description:
      files to deleted from File ShRE
    required: true
    choices:
      - 'file*'
      - 'file*.txt'
      - 'file*.tx*'
      - 'file*.*'
      - file.tx*
      - '*.txt'
      - 'file.*'
      - '*.*'
      - 'file.txt'
    type: string
"""

RETURN = """
output:
  description: Directory created and list of files uploaded
  type: dict
  returned: allways
  sample: 
    "output": {
        "changed": false,
        "content": [
            "o4n_azure_list_files.py",
            "o4n_azure_list_shares.py",
            "o4n_azure_download_files.py",
            "o4n_azure_manage_shares.py",
            "__init__.py",
            "o4n_azure_manage_directory.py",
            "o4n_azure_upload_files.py",
            "o4n_azure_delete_files.py",
            "o4n_azure_list_directories.py"
        ],
        "failed": false,
        "msg": "Files uploaded to Directory </dir1> in share <share-to-test2>"
    }
"""

EXAMPLES = """
tasks:
  - name: Upload files
    o4n_azure_upload_files:
      account_name: "{{ connection_string }}"
      share: share-to-test
      connection_string: "{{ connection_string }}"
      source_path: /dir1/dir2
      dest_path: /dir1
      files: file*.txt
    register: output

  - name: Upload files
    o4n_azure_upload_files:
      account_name: "{{ connection_string }}"
      share: share-to-test
      connection_string: "{{ connection_string }}"
      source_path: /dir1/dir2
      files: file*.t*
      dest_path: /dir1/dir2
    register: output
"""

import os
from azure.storage.fileshare import ShareClient
import azure.core.exceptions as aze
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_get_right_path import right_path
from azure.storage.fileshare import ShareClient
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_list_shares import list_shares_in_service
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_select_files_pattern import select_files
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_get_right_path import right_path

def create_directory(_connection_string, _share, _directory, _print_path):
    status = True
    share = ShareClient.from_connection_string(_connection_string, _share)
    try:
        new_directory = share.get_directory_client(directory_path=_directory)
        action = "created"
        new_directory.create_directory()
        msg_ret = f"Directory <{_print_path}> created in share <{_share}>"
        msg_ret = f"Directory <{_print_path}> <{action}> in share <{_share}>"
    except aze.ResourceExistsError:
        msg_ret = f"Directory <{_print_path}> not <{action}>. The Directory already exist>"
    except Exception as error:
        msg_ret = f"Error managing Directory <{_print_path}> in share <{_share}>. Error: <{error}>"
        status = False

    return status, msg_ret, _print_path

def create_subdirectory(_connection_string, _share, _directory, _parent_directory, _print_path, _print_path_parent):
    share = ShareClient.from_connection_string(_connection_string, _share)
    status = True
    try:
        parent_dir = share.get_directory_client(directory_path=_parent_directory)
        action = "created"
        parent_dir.create_subdirectory(_directory)
        msg_ret = f"Sub Directory <{_print_path}> <{action}> under Directory <{_print_path_parent}> in share <{_share}>"
    except aze.ResourceExistsError as error:
        msg_ret = f"Sub Directory <{_print_path}> not <{action}> in Parent Directory <{_print_path_parent}>. The Directory already exist>"
    except aze.ResourceNotFoundError:
        status = False
        msg_ret = f"Sub Directory <{_print_path}> not <{action}>. Resource <{_print_path_parent}> and/or <{_print_path}>in share <{_share}> do not exist>"
    except Exception as error:
        msg_ret = f"Error managing Sub Directory <{_print_path}> in Parent Directory <{_print_path_parent}>, share <{_share}>. Error: <{error}>"
        status = False

    return status, msg_ret, _print_path_parent + _print_path

def upload_files(_account_name, _share, _connection_string, _source_path, _source_file, _dest_path):
  found_files = []
  _dest_path, print_path = right_path(_dest_path)
  try:
      # get files form local file system
      base_dir = os.getcwd() + "/" + _source_path + "/"
      search_dir = os.path.dirname(base_dir)
      files_in_dir = os.listdir(search_dir)
      # Instantiate the ShareClient from a connection string
      status, msg_ret, shares_in_service = list_shares_in_service(_account_name, _connection_string)
      if status:
        share_exist = [share_name for share_name in shares_in_service if share_name == _share]
      if len(share_exist) == 1:
        share = ShareClient.from_connection_string(_connection_string, _share)
        status, msg_ret, found_files = select_files(_source_file, files_in_dir)
        source_path = _source_path + "/" if _source_path else ""
        dest_path = _dest_path + "/" if _dest_path else ""
        if len(found_files) > 0:
            for file_name in found_files:
                file = share.get_file_client(dest_path + file_name)
                # Upload files
                with open(source_path + file_name, "rb") as source_file:
                    file.upload_file(source_file)
            status = True
            msg_ret = f"Files uploaded to Directory <{print_path}> in share <{_share}>"
        else:
            status = False
            msg_ret = f"Files not uploaded to Directory <{print_path}> in share <{_share}>. No file to upload"
      else:
        msg_ret = f"Files not uploaded to Directory <{print_path}>. Error: Share <{_share}> not found"
        status = False
  except Exception as error:
      msg_ret = f"File not uploaded to Directory <{print_path}> in share <{_share}>. Error: <{error}>"
      status = False

  return status, msg_ret, found_files


def main():
    module=AnsibleModule(
        argument_spec=dict(
            account_name=dict(required=True, type='str'),
            share = dict(required=True, type='str'),
            connection_string = dict(required=True, type='str'),
            parent_path = dict(required=False, type='str', default=''),
            source_path=dict(required=False, type='str', default=''),
            files=dict(required=True, type='str'),
            dest_path=dict(required=False, type='str', default='')
        )
    )

    account_name = module.params.get("account_name")
    share = module.params.get("share")
    connection_string = module.params.get("connection_string")
    parent_path = module.params.get("parent_path")
    dest_path = module.params.get("dest_path")
    path_sub, print_path = right_path(dest_path)
    parent_path_sub, print_path_parent = right_path(parent_path)
    source_path = module.params.get("source_path")
    files = module.params.get("files")

    success = False
    if not parent_path_sub:
        success, msg_ret, output = create_directory(connection_string, share, path_sub, print_path)
    else:
        success, msg_ret, output = create_subdirectory(connection_string, share, path_sub, parent_path_sub, print_path, print_path_parent)
    
    if success:
        success, msg_ret, output = upload_files(account_name, share, connection_string, source_path, files, dest_path)

    if success:
        module.exit_json(failed=False, msg=msg_ret, content=output)
    else:
        module.fail_json(failed=True, msg=msg_ret, content=output)

if __name__ == "__main__":
    main()