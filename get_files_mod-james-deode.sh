#!/bin/bash

#WRK=$SCRATCH/investigation/gavle
WRK=$SCRATCH/investigation/deode_spp

#EXP="spp_050"
EXP="CY49t2_NorwaySouth_SPP_50km"

# Is the exp in ec: or ectmp:
ec=ec

# Use "00 12 24" for multiple dates/times/fc lengths/members
DATES="20250525"
HH="00"
FCLEN="0000 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012"
#MEMB="001 002 003 004 005 006"
MEMB="000 001 002 003"

#set -eux

# Go to work dir
cd $WRK || exit 1

sfile=sourcelist_tmp
[ -f ${sfile} ] && rm ${sfile}

echo "Set ECFS wd as ${ec}:harmonie"
#ecd ${ec}:harmonie
echo "ECFS wd is now:"
epwd
echo ""

# EXPERIMENT 
for exp in $EXP; do

    #echo ""
    #echo "Looking for experiment $exp relative to this ECFS wd, which contains:"
    #els ec:$exp
    #echo ""

    # FORECAST
    for date in $DATES; do

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
		    file=$WRK/${exp}_$date${hh}_${fclen}_$memb
		    if [ ! -f $file ]; then
			#echo "Fetching $file"
			echo "${ec}:deode/$exp/archive/$yy/$mm/$dd/$hh/mbr$memb/ICMSHDEOD+${fclen}h00m00s" >> $sfile
		    else
			echo "Existing file found $file"
		    fi
		done
	    done
	done
    done
done

# Check does sfile exist
if [ -f ${sfile} ]; then
    # Fetch from ECFS
    echo ""
    echo "The sourcelist contains:"
    cat ${sfile}

    echo "Now copy with parents"
    ecp --parents --order=tape -F ${sfile} .

    echo "Copy completed!"
    rm ${sfile}

    # Rename the fetched files
    
    # EXPERIMENT 
    for exp in $EXP; do

	# FORECAST
	for date in $DATES; do

	    # Loop over HH (date won't allow this...)
	    for hh in $HH; do

		# Loop over members
		for memb in $MEMB; do

		    yy=$(date -d $date +%Y)
		    mm=$(date -d $date +%m)
		    dd=$(date -d $date +%d)

		    # Loop over forecast lengths
		    for fclen in $FCLEN; do	       

			file=${exp}_$date${hh}_${fclen}_$memb

			# Don't operate on existing data
			if [ ! -f $file ]; then
			    
			    echo "Moving to $file"
			    #mv harmonie/$exp/$yy/$mm/$dd/$hh/mbr$memb/ICMSHHARM+$fclen $file
			    mv deode/$exp/archive/$yy/$mm/$dd/$hh/mbr$memb/ICMSHDEOD+${fclen}h00m00s $file
			else
			    echo "Existing file found $file"
			fi
		    done
		done
	    done
	done
    done

    # Remove the folder structure
    rm -rf deode/$exp
    
else
    echo "Nothing to fetch, exiting..."
    exit 1
fi

exit 0
#harmonie/spp_icenu/2022/07/10/12/mbr001/

