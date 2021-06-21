#!/bin/sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR
# if log > 50MB then del log
if [ -e "moni_ch.log" ];then
FILE_SIZE=`du -k "moni_ch.log" | awk '{print $1}'`
if [ $FILE_SIZE -gt 51200 ];then
sudo rm -f moni_ch.log
fi;
fi;

PLOG=$DIR/moni_ch.log

pid_cs=`ps -aux|grep -v 'grep'|grep -c 'dataServerChans'`

d=$(date "+%Y-%m-%d %H:%M:%S")
echo "*->",$d,$pid_cs >>$PLOG
exec 2>>$PLOG

ulimit -c unlimited
source /etc/profile

if [ $pid_cs -eq 0 ]
then
echo "*ch->>>pid_cs=0,then restart." >>$PLOG
sh ./start_ch.sh
fi;