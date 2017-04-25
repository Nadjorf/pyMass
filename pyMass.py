import sys
import pexpect
import base64

devFile = open('devices', 'r')
devices = [i for i in devFile]

'''
Example of devices file:
1.1.1.1
2.3.4.5
abc.x.com
'''

switch_un = "__USER__"
# switch_pw = "__PASS__"

try:
    for dev in devices:
     child = pexpect.spawn('telnet', [dev.strip()])
     ''' If you want create a file for every device,
     exclude the '##' of lines 24-25 and put the '#' at
     lines 26 to 28
     '''
     ## output = file(dev.strip(),'w')
     ## child.logfile = output
     child.logfile = None
     ''' sys.stdout = Shows the output at terminal '''
     child.logfile = sys.stdout
     child.timeout = 2
     i = child.expect(['login:', 'Username:', pexpect.EOF, pexpect.TIMEOUT])
     if i==0:
       print "[-] Extreme switch. Move on..\n"
       child.kill(0)
     elif i==1:
       child.logfile = None
       child.sendline(switch_un)
       child.logfile = sys.stdout
       child.expect('Password:')
       child.logfile = None
       child.sendline(base64.b64decode("TTXXXXXXXDA="))
       child.logfile = sys.stdout
       i = child.expect (['>', '#', pexpect.EOF, pexpect.TIMEOUT])
       if i==0:
        print " [-] Huawei 1220 ..\n"
        child.logfile = None
        child.sendline('sys')
        child.logfile = sys.stdout
        child.expect(']')
        child.logfile = None
        child.sendline('undo info-center loghost 10.X.8.X')
        child.logfile = sys.stdout
        child.expect(']')
        child.logfile = None
        child.sendline('info-center loghost 10.X.26.X facility local4')
        child.logfile = sys.stdout
        child.expect(']')
        child.logfile = None
        child.sendline('quit')
        child.logfile = sys.stdout
        child.expect('>')
        child.sendline()
        child.logfile = None
        child.sendline('quit')
        child.logfile = sys.stdout
       elif i==1:
         print " [-] Cisco device ...\n"
         child.kill(0)
       elif i == 2:
         print " [-] Error EOF ...\n"
         child.kill(0)
       elif i == 3:
         print " [-] Timeout ...\n"
         child.kill(0)
     else:
      ## Any problem? move on
      pass

except (KeyboardInterrupt, pexpect.EOF, pexpect.TIMEOUT):
  pass
