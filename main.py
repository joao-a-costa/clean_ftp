def clean_ftp():
    # Import required libraries
    import ftplib
    #import logging
    from datetime import datetime, timedelta

    # Set up logging
    #logging.basicConfig(filename='cleanup_ftp.log', level=logging.INFO, format='%(asctime)s %(message)s')

    # Define constants
    FTP_SERVER = "FTPADDRESS"         # The FTP server URL
    FTP_USER = "FTPUSER"               # The FTP username
    FTP_PASS = "FTPPASSWORD"               # The FTP password
    FTP_FOLDERS = ["/FOLDER1/", "/FOLDER2/"]  # List of FTP folders to be cleaned up
    MAX_AGE_DAYS_BACKUP = 360               # The maximum age of files in days
    MAX_FILES = 5                           # The maximum number of files to keep
    BACKUP_FOLDER = "/BACKUPFOLDER/"# The FTP backup folder
    IGNORE_FOLDERS = ["/FOLDERIGNORE/"]
    DEBUG = False

    # Connect to FTP once and reuse connection
    with ftplib.FTP(FTP_SERVER) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        print("Connected to FTP!")

        # Ensure backup folder exists
        try:
            ftp.cwd(BACKUP_FOLDER)
        except ftplib.error_perm:
            ftp.mkd(BACKUP_FOLDER)

        # Function to cleanup FTP folders **recursively**
        def cleanup_ftp(folder, max_files, backup_folder):
            if folder in IGNORE_FOLDERS:
                print(f"Skipping {folder}")
                return

            print(f"Cleaning up {folder}")
            ftp.cwd(folder)
            listing = []
            ftp.dir(listing.append)

            files = []
            subfolders = []

            # Identify files and folders
            for line in listing:
                parts = line.split()
                name = parts[-1]
                if line.startswith("d"):  # Directory
                    subfolders.append(name)
                else:  # File
                    files.append(name)

            files_with_dates = []

            for file in files:
                try:
                    mod_time_str = ftp.sendcmd("MDTM " + file).split()[1]
                    mod_time = datetime.strptime(mod_time_str, "%Y%m%d%H%M%S")
                    files_with_dates.append((file, mod_time))
                except ftplib.all_errors:
                    continue  # Skip if unable to get date

            # Sort files by modification time
            files_with_dates.sort(key=lambda x: x[1])

            # Remove old files
            while len(files_with_dates) > max_files:
                oldest_file, _ = files_with_dates.pop(0)
                print(f"Moving {oldest_file} to backup")
                if not DEBUG:
                    ftp.rename(folder + oldest_file, backup_folder + oldest_file)

            # **Recursively clean subfolders**
            for subfolder in subfolders:
                cleanup_ftp(folder + subfolder + "/", max_files, backup_folder)

        # Function to clean up backup folder
        def cleanup_ftp_backup(folder, days):
            ftp.cwd(folder)
            files = ftp.nlst()

            now = datetime.now()
            for file in files:
                try:
                    mod_time_str = ftp.sendcmd("MDTM " + file).split()[1]
                    mod_time = datetime.strptime(mod_time_str, "%Y%m%d%H%M%S")
                    age = (now - mod_time).days

                    if age > days:
                        print(f"Deleting {file} (Age: {age} days)")
                        if not DEBUG:
                            ftp.delete(file)
                except ftplib.all_errors:
                    continue

        # Run cleanup for each folder **recursively**
        for folder in FTP_FOLDERS:
            cleanup_ftp(folder, MAX_FILES, BACKUP_FOLDER)
        cleanup_ftp_backup(BACKUP_FOLDER, MAX_AGE_DAYS_BACKUP)

# Ensure the script runs when executed
if __name__ == "__main__":
    clean_ftp()