#!/bin/bash

#
# Set the PATH and LD_LIBARY_PATH for running blaze executables
#

if [ $# -lt 1 ]; then
    echo "Usage: $0 blaze_root_dir"
else
    if [ "$OUTDIR" == "" ]; then
        OUTDIR=$1/out/linux/debug
    fi

    BLAZE_PATH=$OUTDIR/bin
    echo $PATH | grep $BLAZE_PATH > /dev/null 2>&1
    if [ $? != 0 ]; then
        export PATH=$BLAZE_PATH:$PATH
    fi

    PACKAGE_DIR=../packages
    if [ -f $1/make/config.mak ]
    then
        PACKAGE_DIR=`grep PACKAGE_DIR $1/make/config.mak | sed 's/PACKAGE_DIR[ ]*=[ ]*//'`
    fi

    PACKAGE_DIR=$1/$PACKAGE_DIR
    echo "PACKAGE_DIR=$PACKAGE_DIR"

    if [ $(uname -m) == "x86_64" ]; then
        ORACLE_PATH=$PACKAGE_DIR/oracle/10.2.0.3/linux64/lib
    else
        ORACLE_PATH=$PACKAGE_DIR/oracle/10.2.0.3/linux32/lib
    fi

    echo "ORACLE_PATH=$ORACLE_PATH"

    BLAZE_LD_LIBRARY_PATH=$ORACLE_PATH:$BLAZE_PATH
    echo $LD_LIBRARY_PATH | grep $BLAZE_LD_LIBRARY_PATH > /dev/null 2>&1
    if [ $? != 0 ]; then
        export LD_LIBRARY_PATH=$BLAZE_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
    fi
fi
