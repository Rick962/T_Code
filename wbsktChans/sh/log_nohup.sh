#!/bin/bash
#30 5 * * * root /path/to/tasksFireCoins.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR

# if log > 50MB then del log
if [ -e "log_nohup.log" ];then
FILE_SIZE=`du -k "log_nohup.log" | awk '{print $1}'`
if [ $FILE_SIZE -gt 51200 ];then
sudo rm -f log_nohup.log
fi;
fi;

PLOG=$DIR/log_nohup.log
d=$(date "+%Y-%m-%d %H:%M:%S")
echo "*->",$d >>$PLOG
exec 2>>$PLOG

cd ..

# if log > 50MB then del log
if [ -e "nohup.out" ];then
FILE_SIZE=`du -k "nohup.out" | awk '{print $1}'`
if [ $FILE_SIZE -gt 51200 ];then
sudo rm -f nohup.out
echo "*log_nohup->nohup.out more than 50MB,and then restart ./sh/start.sh" >>$PLOG
sh ./sh/start_td.sh
fi;
fi;