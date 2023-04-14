# clean_ftp
This script is a Python function named clean_ftp that performs cleanup operations on a specified FTP server. It takes no input arguments and does not return any output.

The script first imports the required libraries, including ftplib for communicating with the FTP server and datetime for manipulating dates and times. It then defines several constants, including the FTP server URL, username, and password, as well as a list of folders to be cleaned up, a maximum age of files in days, the maximum number of files to keep, the FTP backup folder, and a list of folders to ignore during cleanup.

The script then creates a backup folder if it doesn't exist and defines two functions: cleanup_ftp and cleanup_ftp_backup.

The cleanup_ftp function recursively deletes files in an FTP folder that are older than the maximum age while keeping a maximum number of files. Deleted files are moved to the backup folder in the FTP. The function skips processing if the current folder is in the ignore list.

The cleanup_ftp_backup function deletes backup files in the FTP folder that are older than the specified number of days. The function loops through all files in the folder and deletes any files that are older than the specified number of days.

Finally, the script opens an FTP connection, logs in, and cleans up the specified folder by calling the cleanup_ftp function for each folder in the FTP_FOLDERS list, followed by the cleanup_ftp_backup function for the backup folder. The script can be customized by modifying the constants at the top of the script to suit specific cleanup requirements.
