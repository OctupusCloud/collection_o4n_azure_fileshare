from azure.storage.fileshare import ShareClient
import azure.core.exceptions as aze
from ansible_collections.escrimaglia.o4n_azure_storagefile_test.plugins.module_utils.util_list_shares import list_shares_in_service



def list_files_in_share(_account_name, _connection_string, _share, _dir, _print_path):
    output = {}
    status, msg_ret, shares_in_service = list_shares_in_service(_account_name, _connection_string)
    if status:
        share_exist = [share_name for share_name in shares_in_service if share_name == _share]
    if len(share_exist) != 1:
        status = False
        msg_ret = f"Invalid File Share name: <{_share}>. Share does not exist in Account Storage <{_account_name}>"
        return status, msg_ret, []
    else:
        share = ShareClient.from_connection_string(_connection_string, _share)
        try:
            # List files in the directory
            my_files = {"results": list(share.list_directories_and_files(directory_name=_dir))}
            status = True
            output = [{"name": file['name'], "size": file['size'], "file_id": file['file_id'],
                        "is_directory": file['is_directory']} for file in my_files['results'] if
                        not file['is_directory']]
            if len(output) == 0:
                msg_ret = f"No Files found for path <{_print_path}> in share <{_share}>"
            else:
                msg_ret = f"List of Files created for path <{_print_path}> in share <{_share}>"
        except aze.ResourceNotFoundError:
            msg_ret = f"No files to list for path <{_print_path}> in share <{_share}> ,path not found"
            status = False
        except Exception as error:
            status = False
            msg_ret = f"List of Files not created for path <{_print_path}> in share <{_share}>. Error: <{error}>"

    return status, msg_ret, output