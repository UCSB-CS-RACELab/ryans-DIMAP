UPDATE mysql.user SET password=PASSWORD("bacula142") WHERE user='bacula';
UPDATE mysql.user SET password=PASSWORD("mysql142") WHERE user='root';
FLUSH PRIVILEGES;
exit
