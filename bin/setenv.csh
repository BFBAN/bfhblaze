#
# Set the PATH and LD_LIBARY_PATH for running blaze executables
#

if ($#argv != 1) then
    echo "Usage: $0 blaze_root_dir"
else
    if ( $?OUTDIR == 0 ) then
        set OUTDIR=$1/out/linux/debug
    endif

    set BLAZE_PATH=$OUTDIR/bin
    echo $PATH | grep $BLAZE_PATH >& /dev/null
    if ( $? != 0 ) then
        setenv PATH ${BLAZE_PATH}:${PATH}
    endif

    set PACKAGE_DIR=../packages
    if ( -f $1/make/config.mak ) then
        set PACKAGE_DIR=`grep PACKAGE_DIR $1/make/config.mak | sed 's/PACKAGE_DIR[ ]*=[ ]*//'`
    endif

    set PACKAGE_DIR=$1/$PACKAGE_DIR
    echo "PACKAGE_DIR=$PACKAGE_DIR"

    if ( `uname -m` == "x86_64" ) then
        set ORACLE_PATH=$PACKAGE_DIR/oracle/10.2.0.3/linux64/lib
    else
        set ORACLE_PATH=$PACKAGE_DIR/oracle/10.2.0.3/linux32/lib
    endif

    echo "ORACLE_PATH=$ORACLE_PATH"

    set BLAZE_LD_LIBRARY_PATH=${ORACLE_PATH}:${BLAZE_PATH}
    if ( $?LD_LIBRARY_PATH == 0 ) then
        setenv LD_LIBRARY_PATH
    endif
    echo $LD_LIBRARY_PATH | grep $BLAZE_LD_LIBRARY_PATH >& /dev/null
    if ( $? != 0 ) then
        setenv LD_LIBRARY_PATH ${BLAZE_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}
    endif

endif
