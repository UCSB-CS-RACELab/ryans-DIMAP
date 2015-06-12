CREATE USER 'BackupSys'@'localhost' IDENTIFIED BY 'mysql142';
GRANT ALL PRIVILEGES ON BackupSys.* TO 'BackupSys'@'localhost';

FLUSH PRIVILEGES;
