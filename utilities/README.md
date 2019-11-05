This is a small utility to mount the RBP_bioinfo backup folder into your 
file system. This will be performed by sshfs protocol, and it can work only
with Linux OS. 

If you do not have already sshfs run:
        
        sudo apt-get install sshfs
        
then, you can run the script.

usage:

    mount_backup.sh mount_point rsa_file port ssh_cmd action
    
action can be: mount or umount.

NOTE: The folder has ready-only privilege.
