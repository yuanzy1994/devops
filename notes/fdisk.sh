#/bin/bash
mkdir -pv /home/admin/logs &> /dev/null
chown admin:admin /home/admin/logs
LOG_PATH=/home/admin/logs
DISK_FLAG=1

function pre_check() {
    egrep  "^admin" /etc/passwd > /dev/null && ls $LOG_PATH
    if [ $? -ne 0 ];then
	echo "${LOG_PATH}不存在！"
        exit 1
    fi
    if [ -b /dev/vdb1 ];then
        echo "/dev/vdb1设备已存在！"
        exit 1
    elif [ -b /dev/xvdb1 ];then
        echo "/dev/xvdb1设备已存在！"
        exit 1
    fi
}

function disk_type(){
    if [ -b /dev/vdb ];then
        DISK='/dev/vdb'
    elif [ -b /dev/xvdb ];then
        DISK='/dev/xvdb'
    else
	echo "没有检测到磁盘！"
        exit 1
    fi
}

function file_sys(){
    if [ 'mkfs.xfs' == `ls /sbin/ | grep  mkfs.xfs` ];then
        ACTION=mkfs.xfs
        FILE_SYS=xfs
    elif [ 'mkfs.ext4' == `ls /sbin/ | grep  mkfs.ext4` ];then
        ACTION=mkfs.ext4
        FILE_SYS=ext4
    else
        ACTION=mkfs.ext3
        FILE_SYS=ext3
    fi
}

function do_fdisk() {
    echo "n
    p
    1


    w
    " | fdisk ${DISK} && ${ACTION} -f ${DISK}${DISK_FLAG}
}

function auto_mount(){
    UUID=`blkid ${DISK}${DISK_FLAG}  | awk '{print $2}' | awk -F'"' '{print $2}'`
    if [ -n $UUID ];then
	echo "磁盘UUID为空！"
	exit 1
    fi
    grep "$UUID"  /etc/fstab
    if [ $? -eq 0 ];then
	echo "/etc/fstab已存在该条记录！"
	exit 1
    fi
    echo "UUID=$UUID /home/admin/logs        ${FILE_SYS}     defaults        0 0" >> /etc/fstab
    mount -a
    chown -R admin.admin /home/admin/logs
}

function check_stats(){
    df -lh | grep /home/admin/logs | grep $DISK
    if [ $? -ne 0 ];then
        echo "mount failed!" > /tmp/mount.stats
	echo "挂载失败！"
        exit 1
    else
        echo "mount success!" > /tmp/mount.stats
	echo "挂载成功！"
        chown -R admin.admin /home/admin/logs
        exit 0
    fi
}

pre_check

disk_type

file_sys

do_fdisk

auto_mount

check_stats

chown -R admin:admin /home/admin/logs
rm -f fdisk.sh
