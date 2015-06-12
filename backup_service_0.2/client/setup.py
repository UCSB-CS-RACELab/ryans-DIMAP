

# Install bacula-client package
from subprocess import call
print "Installing Bacula"
status = call("sudo yum install bacula-client -y > /dev/null" , shell=True)
if status != 0:
        print "bacula-client installation failed"


# Call script that adds the backup server's keys to ~/.ssh/authorized_keys
from os import path
print "Adding backup server keys to authorized keys"
if path.isfile("auth_server.sh"):
        status = call("./auth_server.sh", shell=True)
        if status != 0:
                print "Failed to authorize server access"
else:
        print "File auth_server.sh missing."
