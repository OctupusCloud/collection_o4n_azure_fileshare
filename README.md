# Octupus Collection

Collection o4n_azure_fileshare helps apps to manage Azure FileShare Storage  
By Ed Scrimaglia

## Required

Ansible >= 2.10  
Python package azure-storage-file-share >= 12.15.0  

## Modules

- o4n_azure_manage_share  
  Create and Delete File Shares in a Storage Account  

- o4n_azure_list_shares  
  List File Shares in service in a Storage Account  

- o4n_azure_manage_directory  
  Create and Delete Directories and Sub Directories in a File Share

- o4n_azure_list_directories  
  List Directories and Sub Directories  

- o4n_azure_upload_files  
  Upload files from a local File System to a File Share  

- o4n_azure_download_files  
  Download files from a File Share to a local File System  

- o4n_azure_list_files  
  List Files on any Directory in a File Share  

- o4n_azure_delete_files  
  Delete files from any Directory in a File Share  

- o4n_azure_upload_directory  
  Create a Directory/Sub Directory and upload files from a local File System to a file share
