def clean_ftp(request):
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

    # create backup folder if it doesn't exist
    with ftplib.FTP(FTP_SERVER) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        # change the current working directory to the subdirectory
        # try to change to the subdirectory; if it doesn't exist, create it
        try:
            ftp.cwd(BACKUP_FOLDER)
        except:
            ftp.mkd(BACKUP_FOLDER)

    # Define a function to recursively delete files in an FTP folder that are older
    # than MAX_AGE_DAYS while keeping a maximum number of MAX_FILES. Deleted files are
    # moved to BACKUP_FOLDER in the FTP.
    def cleanup_ftp(ftp, folder, max_files, backup_folder):
        # Skip processing if the current folder is in the ignore list
        if folder in IGNORE_FOLDERS:
            return

        ftp.cwd(folder)
        listing = []
        ftp.dir(listing.append)
        items = [item.split()[-1] for item in listing if item[0] != 'd']
        dirs = [item.split()[-1] for item in listing if item[0] == 'd'][2:]
        files = []
        for file in items:
            try:
                # try to get the modification time of the file
                ftp.sendcmd("MDTM " + file)
                files.append(file)
            except ftplib.all_errors:
                # if we can't get the modification time, assume it's a directory
                dirs.append(file)
        files.sort(key=lambda f: ftp.sendcmd("MDTM " + f).split()[1])
        for file in files:
            if max_files > 0 and len(files) > max_files:
                oldest_file = files.pop(0)
                if not DEBUG:
                    ftp.rename(folder + oldest_file, backup_folder + oldest_file)
                max_files -= 1
                #logging.info(f"{oldest_file} moved to {backup_folder}")
        for dir in dirs:
            cleanup_ftp(ftp, folder + dir + "/", max_files, backup_folder)

    def cleanup_ftp_backup(ftp, folder, days):
        # Change to the folder
        ftp.cwd(folder)

        # Get a list of all files in the folder
        files = ftp.nlst()[2:]

        # Get the current date and time
        now = datetime.now()

        # Loop through the files and delete the old ones
        for file in files:
            # Get the modification time of the file
            mod_time_str = ftp.sendcmd("MDTM " + file).split()[1]
            mod_time = datetime.strptime(mod_time_str, "%Y%m%d%H%M%S")

            # Calculate the age of the file in days
            age = (now - mod_time).days

            # If the file is older than the specified number of days, delete it
            if age > days:
                if not DEBUG:
                    ftp.delete(file)
                #logging.info(f"Deleting backup {file} with age {age} bigger than {days}")

    # Example usage:
    # Open an FTP connection, log in, and clean up the specified folder
    with ftplib.FTP(FTP_SERVER) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        for folder in FTP_FOLDERS:
            cleanup_ftp(ftp, folder, MAX_FILES, BACKUP_FOLDER)
        cleanup_ftp_backup(ftp, BACKUP_FOLDER, MAX_AGE_DAYS_BACKUP)