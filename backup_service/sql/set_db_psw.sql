UPDATE mysql.user SET password=PASSWORD("DB_PASSWORD") WHERE user='bacula';
UPDATE mysql.user SET password=PASSWORD("ROOT_DB_PASSWORD") WHERE user='root';
FLUSH PRIVILEGES;
exit
