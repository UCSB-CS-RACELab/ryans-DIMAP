CREATE DATABASE BackupSys;

use BackupSys;

CREATE TABLE Users ( name char(32),	
					 auth char(32),
					 PRIMARY KEY(name)
					);

CREATE TABLE BackupJobs ( IP char(16),
						 User char(16),
						 Directory char(64),
						 FdPassword char(64),
						 SysTag char(10),
						 PRIMARY KEY (IP)
						 );
						  
						 