from azure.storage.fileshare import ShareServiceClient

def list_shares_in_service(_account_name, _connection_string):
    output = []
    try:
        # Instantiate the ShareServiceClient from a connection string
        file_service = ShareServiceClient.from_connection_string(_connection_string)
        # List the shares in the file service
        my_shares = list(file_service.list_shares())
        output = [share['name'] for share in my_shares if share]
        status = True
        if len (output) == 0:
            msg_ret = f"No Shares found in account <{_account_name}>"
        else:
            msg_ret = f"List of Shares created in account <{_account_name}>"
    except Exception as error:
        status = False
        msg_ret = f"List of Shares not created in account <{_account_name}>. Error: <{error}>"

    return status, msg_ret, output
