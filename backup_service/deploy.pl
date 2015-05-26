#!/usr/bin/perl -w
##
## deploy.pl for backup server system.
## WARNING: This is not a careful script, please be careful.
##
## 2015, Ryan Halbrook
##

sub install {
    my ($name) = @_;
    print "Installing ".$name."\n";
    if (!(system("yum install $name -y") == 0)) { 
    	die "Failed to Install: $?";
    }
}

sub command {
    my($name) = @_;
    if (!(system($name) == 0)) { 
    	die "Failed to Install: $?";
    }
}

if (!defined $ARGV[0]) {
	die "Installation Failed: Please specify IP address.";
}

$address = $ARGV[0];

# Install required MySQL packages.
install("mysql-server");
install("mysql-devel");

# Install required Bacula packages.
install("bacula-director-mysql");
install("bacula-console");
install("bacula-storage-mysql");
install("bacula-client");

command("service mysqld start");

# Configure the database for use with bacula. 
command("/usr/libexec/bacula/grant_mysql_privileges -u root -p");
command("/usr/libexec/bacula/create_mysql_database -u root -p");
command("/usr/libexec/bacula/make_mysql_tables -u root -p");
command("/usr/libexec/bacula/grant_bacula_privileges -u root -p");

command("mysql -u root < sql/ServerDatabase.sql");
command("mysql -u root < sql/ServerUser.sql");

command("mysql -u root < sql/set_db_psw.sql");

command("mkdir /bacula-scripts");
command("chown bacula /bacula-scripts");
command("cp conf/post-backup.py /bacula-scripts/post-backup.py");

command("cp conf/bacula-dir.conf /etc/bacula/bacula-dir.conf");
command("cp conf/bacula-sd.conf /etc/bacula/bacula-sd.conf");
command("cp conf/bacula-fd.conf /etc/bacula/bacula-fd.conf");
command("cp conf/bconsole.conf /etc/bacula/bconsole.conf");

command("sed -i 's/MY_IP/$address/g' /etc/bacula/bacula-dir.conf");


command("mkdir /bacula");
command("chown bacula /bacula");

command("chkconfig mysqld on");
command("chkconfig bacula-dir on");
command("chkconfig bacula-sd on");
command("chkconfig bacula-fd on");


command("service bacula-dir start");
command("service bacula-sd start");
command("service bacula-fd start");

install("python-twisted-web");

#command("cp conf/auth_server.sh .");
#command("ssh-keygen -t rsa");
#command(

print "Installation succcessful.\n"


