#!/bin/sh
TESTFILE=/.timelimit
LOGFILE=`ls -ac /arma3/profiles/arma3server_* | cat | head -1`
RESULT=1
touch -d '-1 mins' $TESTFILE

if [ $LOGFILE -nt $TESTFILE ]; then
  RESULT=0
fi
rm $TESTFILE
exit $RESULT

