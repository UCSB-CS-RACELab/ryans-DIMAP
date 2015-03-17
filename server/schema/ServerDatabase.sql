CREATE DATABASE BackupSys;

use BackupSys;

CREATE TABLE Users ( name char(32),	
					 auth char(32),
					 PRIMARY KEY(name)
					);

CREATE TABLE BackupJobs ( IP char(16),
			    User char(16),
			    Directory char(64),
			    FdName char(64),
			    SysTag char(10),
			    PRIMARY KEY (IP)
			 );
			  
CREATE TABLE JobIDs(JobID Integer,
		    User char(16),
		    PRIMARY KEY(JobID));
 
