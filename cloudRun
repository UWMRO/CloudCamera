#!/bin/bash

echo
echo ==== Using cloudRun $CLOUD_DIR ====
echo

usage() {
    echo "usage: $0 start|stop|stopall|restart|status" >&2
    exit 1
}

if test $# != 1; then
    usage
fi
cmd=$1

# Return the actor's pid, or the empty string.
#
get_pid() {
    PID=""
    pid=`/bin/ps -e -ww -o pid,user,command | egrep -v 'awk|grep' | grep 'cloudProcess.py' | awk '{print $1}'`
    PID=$pid
	
    PID2=""
    pid2=`/bin/ps -e -ww -o pid,user,command | egrep -v 'awk|grep' | grep 'CloudCam.py' | awk '{print $1}'`
    PID2=$pid2

    PID3=""
    pid3=`/bin/ps -e -ww -o pid,user,command | egrep -v 'awk|grep' | grep 'wiggleCloud.py' | awk '{print $1}'`
    PID3=$pid3


    PID4=""
    pid4=`/bin/ps -e -ww -o pid,user,command | egrep -v 'awk|grep' | grep 'clouduino_interface.py' | awk '{print $1}'`
    PID4=$pid4
    
    if test "$pid"; then
        echo "cloudProcess is running as process $pid"
    else
        echo "cloudProcess is not running"
    fi


    if test "$pid2"; then
        echo "CloudCam is running as process $pid2"
    else
        echo "CloudCamera is not running"
    fi

    if test "$pid3"; then
        echo "wiggleCloud is running as process $pid3"
    else
        echo "wiggleCloud is not running"
    fi

    if test "$pid4"; then
        echo "clouduino_interface is running as process $pid4"
    else
        echo "clouduino_inteface is not running"
    fi


}

# Start a new actor. Complain if the actor is already running,  and do not start a new one.
#
do_start() {
    get_pid
    
    if test "$PID"; then
        echo "NOT starting new CloudCamera. Use restart if you want a new one."
        return
    fi
    
    echo "Starting new CloudCamera..."

    # run the actor, as follows:
    # disable buffering of stdout using "stdbuf -o0"
    # redirect stdout to logger at priority "warning" and stderr at priority "error"
    {
        nohup python cloudProcess.py  
    }  &
    
    # Check that it really started...
    #
    sleep 1
    get_pid

    if test "$PID"; then
        echo " done."
    else
        echo " FAILED!"
    fi
}

# Stop runCloudProcess. 
#
do_stop() {
    get_pid
    
    if test ! "$PID"; then
        return
    fi
    
    echo "Stopping runCloudProcess."
    kill -TERM $PID
    echo "Stopping CloudCam."
    kill -TERM $PID2
    echo "Stopping wiggleCloud."
    kill -TERM $PID3
    echo "Stopping clouduino_interface."
    kill -TERM $PID4
}


# Stop all Cloud associated process.
#
do_stopall() {
    get_pid

    if test ! "$PID"; then
        return
    fi

    echo "Stopping runCloudProcess."
    kill -TERM $PID

    if test ! "$PID2"; then
        return
    fi

    echo "Stopping CloudCam."
    kill -TERM $PID2

    if test ! "$PID3"; then
        return
    fi

    echo "Stopping wiggleCloud."
    kill -TERM $PID3

    if test ! "$PID4"; then
        return
    fi

    echo "Stopping clouduino_interface."
    kill -TERM $PID4

}

# Stop any running actor fairly violently. 
#
do_stopdead() {
    get_pid
    
    if test ! "$PID"; then
        return
    fi
    
    echo "Stopping arcticICC gently."
    kill -TERM $PID
    sleep 2

    echo "Stopping arcticICC meanly."
    kill -KILL $PID
    kill -KILL $PID2
    kill -KILL $PID3
    kill -KILL $PID4
}

case $cmd in
    start) 
        do_start
        ;;
    stop)
        do_stop
        ;;
    stopall)
	do_stopall
	;;
    stopdead)
        do_stopdead
        ;;
    status)
        # Check whether the actor is running
        get_pid
        ;;
    restart)
        do_stop
        sleep 2
        do_start                
        ;;
    *)
        usage
        ;;
esac

exit 0

