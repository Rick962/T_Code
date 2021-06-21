#!/bin/bash
#30 5 * * * root /path/to/start.sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR
# if log > 50MB then del log
if [ -e "xsh.log" ];then
FILE_SIZE=`du -k "xsh.log" | awk '{print $1}'`
if [ $FILE_SIZE -gt 51200 ];then
sudo rm -f xsh.log
fi;
fi;

PLOG=$DIR/xsh.log
d=$(date "+%Y-%m-%d %H:%M:%S")
echo "*ch->kill: ",$d >>$PLOG
exec 2>>$PLOG

cd ..

ps auxww|grep dataServerChans |grep -v grep|awk '{print $2}' | xargs kill -9