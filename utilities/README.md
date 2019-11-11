This is a small utility to mount a remote folder into your 
file system through sshfs protocol. 

If you do not have already sshfs run:
        
    sudo apt-get install sshfs
        
then, you can run the script.

usage:

    mount_backup.sh mount_point rsa_file port ssh_cmd action
    
action can be: mount | umount.

NOTE: The folder has ready-only privilege.
