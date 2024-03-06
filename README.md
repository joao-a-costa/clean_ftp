# Cleanup FTP

## Introduction

This script, `clean_ftp.py`, is designed to facilitate the cleanup of files within specified FTP folders. It connects to a specified FTP server, logs in, and recursively deletes files that exceed a specified age while maintaining a maximum number of files. Additionally, it backs up the deleted files to a designated backup folder on the FTP server.

## Features

- **FTP Server Connection**: Establishes a connection to the specified FTP server using the provided credentials.

- **Cleanup Functionality**: Recursively deletes old files in the specified FTP folders, ensuring that the total number of files does not exceed a specified limit.

- **Backup Mechanism**: Moves the deleted files to a designated backup folder on the FTP server for archival purposes.

- **Customization**: Allows customization of FTP server details, cleanup criteria (age and maximum files), and backup folder location.

- **Logging (Optional)**: Includes optional logging functionality to track the cleanup process. Logging can be enabled by uncommenting relevant sections in the code.

## Prerequisites

Before using the script, ensure you have the following:

- Python 3.x installed on your machine.
- The `ftplib` library, part of the Python standard library, is available.

## Configuration

To use the script, you need to configure the following parameters within the script:

- `FTP_SERVER`: The URL of the FTP server.
- `FTP_USER`: The FTP username for authentication.
- `FTP_PASS`: The FTP password for authentication.
- `FTP_FOLDERS`: A list of FTP folders to be cleaned up.
- `MAX_AGE_DAYS_BACKUP`: The maximum age of files in days for the backup cleanup.
- `MAX_FILES`: The maximum number of files to keep during cleanup.
- `BACKUP_FOLDER`: The FTP backup folder where deleted files are archived.
- `IGNORE_FOLDERS`: (Optional) A list of folders to be excluded from cleanup.
- `DEBUG`: Set to `True` to enable debug mode, where files are not deleted or moved. Set to `False` for normal operation.

## Usage

To execute the script, run it as a standalone Python script:

python clean_ftp.py

Ensure the script has the necessary permissions to connect to the specified FTP server and perform cleanup operations.

## Notes

- The script uses the FTP MDTM command to retrieve file modification times. Ensure that your FTP server supports this command.
- Take precautions and thoroughly review the script before executing it on critical systems to avoid unintended data loss.

## License
- This script is provided under the MIT License. Feel free to modify and distribute it according to your needs.
