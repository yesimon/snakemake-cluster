snakemake-cluster
=================

Simple snakemake cluster submission wrapper.

This command submits the snakemake master process to the cluster, which then launches the
individual jobs with the correct cluster arguments.

```
Usage:
  snakemake-cluster -J myjob -- [snakemake-args]

Options:
  --cluster-config: Set cluster.yaml (default: cluster.yaml)
  --cluster-submitter: Set cluster submitter
    (default: ~/.config/snakemake/cluster-submitter.py)
  --jobscript: Set jobscript (default: ~/.config/snakemake/jobscript.sh)
  --verbose: Print actual submissions commands
  --lock: Don't set option --nolock
  --no-rerun-incomplete: Don't set option '--rerun-incomplete'
  --no-user-cluster-config: Don't use user's cluster config as the base template
    (default: ~/.config/snakemake/cluster.yaml)
```

Example:
  `snakemake-cluster -J myjob --snakefile do_stuff.sf last_rule`

Installing
----------
This wrapper requires the `qbsub` wrapper script around `qsub` located here:
https://github.com/broadinstitute/qbsub

For a simple one liner to download to `~/bin`:
```
mkdir -p ~/bin && wget https://raw.githubusercontent.com/broadinstitute/qbsub/master/bin/qbsub -o ~/bin/qbsub && chmod +x ~/bin/qbsub
```

Simply clone the repository and run `make`. This will by default install the
`snakemake-cluster` script to `~/bin`. Therefore you will need to add `~/bin` to
your `$PATH`.
```
git clone https://github.com/yesimon/snakemake-cluster.git
cd snakemake-cluster
make
```

Snakemake Cluster Config
------------------------
The cluster config is where you store cluster resource requirements for each type of rule. The
first location is `~/.config/snakemake/cluster.yaml` which applies to all projects, while the
project specific config at `<project_dir>/cluster.yaml` can be used to add additional cluster
configs, overriding the user `cluster.yaml` if there are any conflicts. The expected format is below:

`<project_dir>/cluster.yaml`
```yaml
__default__:
  n: 1
  queue: short
  mem: 8
  log: '{log}'

bwa:
  queue: long
  time: '18:00'
  n: 2
  mem: 4
```

Time is listed in hours and is optional, `n` corresponds to the number of cores, `mem` is the
maximum memory in gigabytes for the job. The `log: '{log}'` directive is necessary for logging to
be redirected to the correct location. An example corresponding `Snakefile`:

`<project_dir>/Snakefile`
```python
rule bwa:
    input: 'fastq/{sample}.1.fastq', 'fastq/{sample}.2.fastq'
    output: 'alignment/{sample}.bwa.sam'
    log: 'log/alignment/{sample}.bwa.log'
    shell:
        '''
        bwa mem -t 2 -a ~/db/bwa {input[0]} {input[1]} > {output}
        '''

rule mapped_bam:
    input: 'alignment/{sample}.bwa.sam'
    output: 'alignment/{sample}.bwa.bam'
    log: 'log/alignment/{sample}.samtools_mapped.log'
    shell:
        '''
        samtools view -h -b -F 4 -o {output} {input}
        '''
```

In this case, the `bwa` rule jobs will get the `bwa` cluster config resources,
while the `mapped_bam` rule will get the `__default__` cluster config resources.

Snakemake Pipeline Layout
-------------------------
This wrapper doesn't make any assumptions about the format of the pipeline. It
is recommended to have a `log` directive for all rules.
