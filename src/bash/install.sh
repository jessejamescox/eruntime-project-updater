#!/bin/bash

# Create destination folder
DESTINATION="/etc/rt_updater"
VERSION="0.0.1"
NAME="rt_updater_v${VERSION}.tgz"
URL="https://github.com/jessejamescox/eruntime-project-updater/raw/master/${NAME}"
mkdir -p ${DESTINATION}

wget ${URL}
tar -xzf ${NAME} -C /etc

echo ""
echo "Installation complete."
echo ""

rm ${NAME}

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "* * * * * python /etc/rt_updater/rt_updater_v0.0.1.py >/dev/null 2>&1" >> mycron
#install new cron file
crontab mycron
rm mycron

# Exit from the script with success (0)
exit 0
