CREATE USER 'BackupSys'@'localhost' IDENTIFIED BY 'PWD';
GRANT ALL PRIVILEGES ON BackupSys.* TO 'BackupSys'@'localhost';

FLUSH PRIVILEGES;
