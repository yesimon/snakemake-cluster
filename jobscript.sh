#!/bin/bash
# properties = {properties}

function handle_qdel {{
    echo "Killed by scheduler"
    touch {jobfailed}
}}

trap handle_qdel USR2
trap handle_qdel TERM

{exec_job}

# if the job succeeds, snakemake
# touches jobfinished, thus if it exists cat succeeds. if cat fails, the error code indicates job failure
# an error code of 100 is needed since UGER only prevents execution of dependent jobs if the preceding
# job exits with error code 100
cat {jobfinished} &>/dev/null && exit 0 || exit 1
