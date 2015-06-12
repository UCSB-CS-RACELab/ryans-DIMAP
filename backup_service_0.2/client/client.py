import pycurl
import json
import cStringIO

def prompt():

    done = False

    while not done:
        userInput = raw_input('backDrop 0.2 > ')
        strs = userInput.split(" ")

        if len(strs) < 1:
            continue

        command = strs[0]

        if command == 'authtest':
            if len(strs) < 3:
                print 'Usage: authtest <user> <key>'
                continue
            userName = strs[1]
            key = strs[2]
            authTest(userName, key)

        elif command == 'startbackups':
            if len(strs) < 4:
                print 'Usage: startbackups <user> <key> <ip>'
                continue
            userName = strs[1]
            key = strs[2]
            ip = strs[3]
            startBackups(userName, key, ip)

        elif command == 'listoptions':
            if len(strs) < 3:
                print 'Usage: listoptions <user> <key>'
                continue
            userName = strs[1]
            key = strs[2]
            listRestoreOptions(userName, key)

        elif command == 'restoremachine':
            if len(strs) < 5:
                print 'Usage: restoremachine <user> <key> <ip> <restoreoption>'
                continue
            userName = strs[1]
            key = strs[2]
            ip = strs[3]
            restoreOption = strs[4]
            restoreMachine(userName, key, ip, restoreOption)


        elif command == 'exit':
            break

        elif command == '':
            continue

        else:
            print 'Unkown command'


def authTest(user, key):
    data = json.dumps({"command":"auth-test", "user":user})
    print callAPI(data, key)


def startBackups(user, key, ip):
    data = json.dumps({"command":"start-backups", "user":user, "ip": ip})
    print callAPI(data, key)

def listRestoreOptions(user, key):
    data = json.dumps({"command":"list-available", "user":user})
    print callAPI(data, key)

def restoreMachine(user, key, ip, restoreOption):
    data = json.dumps({"command":"restore-new-machine", "user":user, "ip":ip, "restoreOption":restoreOption})
    print callAPI(data, key)

def callAPI(data, key):
    buffer = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://128.111.179.151:8243/backDrop/v1.0.0")
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(pycurl.HTTPHEADER, ['Authorization : Bearer ' + key])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.perform()

    response = buffer.getvalue()
    buffer.close()
    return response

def main():
	prompt()



if __name__ == "__main__":
	main()
