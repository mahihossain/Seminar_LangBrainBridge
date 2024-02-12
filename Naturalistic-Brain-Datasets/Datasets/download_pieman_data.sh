for i in {1..82}; do
    if [ $i -lt 10 ]
    then
	cd "sub-00"$i/func || continue
	datalad install -g *pieman_run-1_space-fsaverage6_hemi-L_desc-clean.func.gii
	datalad install -g *pieman_run-1_space-fsaverage6_hemi-R_desc-clean.func.gii
	cd "../../"
    else
    	cd "sub-0"$i/func || continue
	datalad install -g *pieman_run-1_space-fsaverage6_hemi-L_desc-clean.func.gii
	datalad install -g *pieman_run-1_space-fsaverage6_hemi-R_desc-clean.func.gii
	cd "../../"
    fi
done
