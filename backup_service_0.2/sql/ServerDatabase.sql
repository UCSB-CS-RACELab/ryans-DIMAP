CREATE DATABASE BackupSys;

use BackupSys

CREATE TABLE Users (user_id varchar(64), password varchar(64), PRIMARY KEY(user_id) ) ;

CREATE TABLE BackupJobs ( IP char(16),
			    User varchar(64),
			    Directory char(64),
			    FdName char(64),
			    SysTag char(10),
			    PRIMARY KEY (IP),
			    FOREIGN KEY (User) REFERENCES Users (user_id)
			 ) ;
			  
CREATE TABLE JobIDs(JobID char(64),
		    User varchar(64),
		    IP char(16),
		    Time char(32),
		    PRIMARY KEY(JobID),
		    FOREIGN KEY (User) REFERENCES Users (user_id)) ;
 
