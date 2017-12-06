#/bin/bash

if [ -f /etc/sysconfig/appname ];then
  systemctl stop `cat /etc/sysconfig/appname`_java
else
  exit 1
fi

rm -rf /home/admin/logs/*

if [ -b /dev/vdb ];then
    echo "OK"
else
    exit 1
fi

echo "n
p
1


w
" | fdisk /dev/vdb && mkfs.xfs /dev/vdb1

blkid /dev/vdb1  | awk '{print $2}' | awk -F'"' '{print $2}'

echo "UUID=`blkid /dev/vdb1  | awk '{print $2}' | awk -F'"' '{print $2}'` /home/admin/logs        xfs     defaults        0 0" >> /etc/fstab

mount -a

df -lh

chown -R admin.admin /home/admin/logs

systemctl start `cat /etc/sysconfig/appname`_java

ps -ef | grep `cat /etc/sysconfig/appname`
