#!/bin/bash

WRK=$SCRATCH/investigation/icenu

#EXP=spp_sp_icenu_a120_small
EXP=spp_sp_oper_icenu_a120_small

SDATE=20220715
EDATE=20220715
#SDATE=20230217
#EDATE=20230217
HH="12"  # use "00 12" for multiple times

FCLEN="0006 0024" # use "0012 0024" for multiple times

MEMB="001 002 003 004 005 006" # use "001 002" for multiple members

#set -eux

# FORECAST
date=$SDATE
while [ $date -le $EDATE ]; do

    # Loop over HH (date won't allow this...)
    for hh in $HH; do

	# Loop over members
	for memb in $MEMB; do

	    yy=$(date -d $date +%Y)
	    mm=$(date -d $date +%m)
	    dd=$(date -d $date +%d)

	    # Loop over forecast lengths
	    for fclen in $FCLEN; do	       

		# Don't fetch existing data
		file=$WRK/${EXP}_$date${hh}_${fclen}_$memb
		if [ ! -f $file ]; then
		    echo "Fetching $file"
		    ecp ec:harmonie/$EXP/$yy/$mm/$dd/$hh/mbr$memb/ICMSHHARM+$fclen $file
		else
		    echo "Existing file found $file"
		fi
	    done
	done
    done

    # Increment date
    date=$(date -d "$date + 1 days" +'%Y%m%d')
done


# REFERENCE
date=$SDATE
while [ $date -le $EDATE ]; do

    # Loop over HH (date won't allow this...)
    for hh in $HH; do

	yy=$(date -d $date +%Y)
	mm=$(date -d $date +%m)
	dd=$(date -d $date +%d)

	# Loop over forecast lengths
	for fclen in $FCLEN; do	       

	    # Don't fetch existing data
	    file=$WRK/control_$date${hh}_${fclen}_000
	    if [ ! -f $file ]; then
		echo "Fetching $file"
		#if [ $yy == 2022 ]; then
		    usr=fai
		#elif [ $yy == 2023 ]; then
		#    usr=snh
		#fi
		echo "ecp ec:/$usr/harmonie/spp_tuning_ref_fix_SP/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen"
		ecp ec:/$usr/harmonie/spp_tuning_ref_fix_SP/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen $file
	    else
		echo "Existing file found $file"
	    fi

	done
    done

    # Increment date
    date=$(date -d "$date + 1 days" +'%Y%m%d')
done


#harmonie/spp_icenu/2022/07/10/12/mbr001/

