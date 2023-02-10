from azure.storage.fileshare import ShareClient
import azure.core.exceptions as aze
from ansible_collections.octupus.o4n_azure_fileshare.plugins.module_utils.util_list_shares import list_shares_in_service


def list_directories_in_share(_account_name, _connection_string, _share, _dir, _print_path):
    output = []
    status, msg_ret, shares_in_service = list_shares_in_service(_account_name, _connection_string)
    if status:
        share_exist = [share_name for share_name in shares_in_service if share_name == _share]
    if len(share_exist) == 1:
        share = ShareClient.from_connection_string(_connection_string, _share)
        try:
            # List directories in share
            my_files = {"results": list(share.list_directories_and_files(directory_name=_dir))}
            status = True
            output = [{"name": file['name'],"file_id": file['file_id'],"is_directory": file['is_directory']} for file in my_files['results'] if file['is_directory']]
            if len(output) == 0:
                msg_ret = f"No Directories found for path <{_print_path}> in share <{_share}>"
            else:
                msg_ret = f"List of Directories created for path <{_print_path}> in share <{_share}>"
        except aze.ResourceNotFoundError:
            msg_ret = f"List of Directories not created for path <{_print_path}> in share <{_share}>. Error: path not found"
            status = False
        except Exception as error:
            status = False
            msg_ret = f"List of Directories not created for path <{_print_path}> in share <{_share}>. Error: <{error}>"
    else:
        msg_ret = f"List of Directories not created for path <{_print_path}> in share <{_share}>. Error: Share not found"
        status = False

    return status, msg_ret, output