UPDATE mysql.user SET password=PASSWORD("") WHERE user='root';
FLUSH PRIVILEGES;
exit