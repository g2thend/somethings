#!/bin/bash
. /etc/openvpn/scripts/config.sh
. /etc/openvpn/scripts/functions.sh

username=$(echap "$username")
password=$(echap "$password")

# Authentication
user_pass=$(mysql -h$HOST -P$PORT -u$USER -p$PASS $DB -sN -e "SELECT user_pass FROM user WHERE user_id = '$username'")
# Check the user
if [ "$user_pass" == '' ]; then
  echo "$username: bad account."
  exit 1
fi


if [ "$password" == "$user_pass" ]; then
  echo "$username: authentication ok."
  #echo "$username  $password "   >> /etc/openvpn/scripts/login.log
  exit 0
else
  echo "$username: authentication failed."
  exit 1
fi
