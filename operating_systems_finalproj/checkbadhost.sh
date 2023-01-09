#/usr/bin/bash badhostname
hostname=(`hostname`);

if [ $hostname == $1 ];
then
    echo ""
    echo ""
    echo "You are running on a RHEL8 system. You need to restart VS Code."
    echo ""
    echo ""
fi;
