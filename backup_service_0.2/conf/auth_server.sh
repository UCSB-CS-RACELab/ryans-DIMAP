#!/bin/bash

pubkey='PUB_KEY'

pubkeyroot='PUB_KEY_ROOT'

sudo echo $pubkey >> /home/ec2-user/.ssh/authorized_keys
sudo echo $pubkeyroot >> ~/.ssh/authorized_keys
