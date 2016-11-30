install:
	@mkdir -p ~/bin
	@ln -sf `pwd`/snakemake-cluster ~/bin
	@mkdir -p ~/.config/snakemake
	@ln -sf `pwd`/jobscript.sh ~/.config/snakemake
	@ln -sf `pwd`/cluster-submitter.py ~/.config/snakemake
	@hash snakemake-cluster 2> /dev/null || echo 'Make sure to add $$HOME/bin to $$PATH'

clean:
	rm ~/bin/snakemake-cluster
	rm ~/.config/snakemake/jobscript.sh
	rm ~/.config/snakemake/cluster-submitter.py
