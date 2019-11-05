#!/bin/bash

### mount backup RBP_lab undert UCO 236425
### requirements:
## sudo apt-get install sshfs

if [[ $@ == "" ]]
then
    echo -e "\nscript to mount or unmount RBP_lab backup folder in the user target directory by sshfs\n\narguments:\n\tmount_point:\tpath to taget dir\n\trsa_file:\tpath to rsa_key file\n\taction:\tmount|umount (str)\nusage:\n\tmount_backup.sh mount_point rsa_file action"
    exit 0
fi

mount_point=$1
rsa=$2
port=$3
ssh_cmd=$4
action=$5

echo -e "running script with arguments:\n\ttarget:\t${mount_point}\n\trsa_file:\t${rsa}\n\taction:\t${action}\n"
echo -e "\nNOTE:\tmounted in read-only mode\n\n"
if [[ $action == "mount" ]]
then
    echo "mount backup at ${mount_point} done"
    sshfs -o nonempty,reconnect,IdentityFile=${rsa},port=$port,ro $ssh_cmd ${mount_point}
    echo -e "PLEASE run 'mount_backup.sh ${mount_point} ${rsa} umount' once you are done."
elif [[ $action == "umount" ]]
then
        echo "un-mount backup from ${mount_point}"
        fusermount -u ${mount_point}
else
    echo "no action to perform,exit"
    exit 0
fi