#!/bin/bash

#WRK=$SCRATCH/investigation/gavle
WRK=$SCRATCH/investigation/icenu

#EXP="spp_050"
EXP="spp_sp_oper_retune1b"

# Is the exp in ec: or ectmp:
ec=ec

# Use "00 12 24" for multiple dates/times/fc lengths/members
DATES="20220715 20220717"
HH="12"
FCLEN="0012"
MEMB="001 002 003 004 005 006"

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
			echo "${ec}:harmonie/$exp/$yy/$mm/$dd/$hh/mbr$memb/ICMSHHARM+$fclen" >> $sfile
		    else
			echo "Existing file found $file"
		    fi
		done
	    done
	done
    done
done


# REFERENCE
for date in $DATES; do

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
		usr=fai

		#echo "ecp ec:/$usr/harmonie/spp_tuning_ref_fix_SP/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen"
		echo "${ec}:/$usr/harmonie/spp_tuning_ref_fix_SP/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen" >> $sfile
		#ecp ${ec}:/dujf/harmonie/de_gavle25S_P0/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen $file
	    else
		echo "Existing file found $file"
	    fi

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
    #ecp --parents --order=tape -F ${sfile} .

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
			    mv harmonie/$exp/$yy/$mm/$dd/$hh/mbr$memb/ICMSHHARM+$fclen $file
			else
			    echo "Existing file found $file"
			fi
		    done
		done
	    done
	done
    done

    # Remove the folder structure
    rm -rf harmonie/$exp
    
    # REFERENCE
    for date in $DATES; do

	# Loop over HH (date won't allow this...)
	for hh in $HH; do

	    yy=$(date -d $date +%Y)
	    mm=$(date -d $date +%m)
	    dd=$(date -d $date +%d)

	    # Loop over forecast lengths
	    for fclen in $FCLEN; do	       

		file=control_$date${hh}_${fclen}_000
		
		# Don't operate on existing data
		if [ ! -f $file ]; then
		    usr=fai

		    echo "Moving to $file"
		    mv $usr/harmonie/spp_tuning_ref_fix_SP/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen $file
		    #ecp ${ec}:/dujf/harmonie/de_gavle25S_P0/$yy/$mm/$dd/$hh/mbr000/ICMSHHARM+$fclen $file
		else
		    echo "Existing file found $file"
		fi

	    done
	done
    done
    
    # Remove the folder structure
    rm -rf $usr/harmonie/
    
else
    echo "Nothing to fetch, exiting..."
    exit 1
fi

exit 0
#harmonie/spp_icenu/2022/07/10/12/mbr001/

