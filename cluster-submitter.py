#!/usr/bin/env python3
import math
import os
import sys
import re
from snakemake.utils import read_job_properties

jobscript = sys.argv[-1]
mo = re.match(r'(\S+)/snakejob\.\S+\.(\d+)\.sh', jobscript)
assert mo
sm_tmpdir, sm_jobid = mo.groups()
props = read_job_properties(jobscript)

# set up job name, project name
jobname = '{rule}-{jobid}'.format(rule=props['rule'], jobid=sm_jobid)
cluster = props['cluster']
mem_per_core = math.ceil(float(cluster['mem']) / int(cluster['n']))

if cluster['mem'] > 16:
    reservation = 'y'
else:
    reservation = 'n'

res_req = {
    'm_mem_free': '{}G'.format(mem_per_core),
    'h_vmem': '{}G'.format(mem_per_core),
}

if 'time' in cluster:
    res_req['h_rt'] = '{}:00'.format(cluster['time'])
res_req_str = ','.join('{}={}'.format(k, v) for k, v in res_req.items())

cmd = ('qbsub --profile -r y -N {jobname} -q {queue} -R {reservation} '
       '-l {res_req} '
       '-n {n} -o {log}'.format(
           jobname=jobname,
           queue=cluster['queue'],
           reservation=reservation,
           res_req=res_req_str,
           log=cluster.get('log') or 'log/default.log',
           n=cluster['n']))

dependencies = set(sys.argv[1:-2])
if dependencies:
    cmd += " -hold_jid '{}'".format(','.join(dependencies))

# the actual job
cmd += ' %s' % jobscript

# the part that strips bsub's output to just the job id
cmd += r' | tail -1 | cut -f 3 -d \ '

os.system(cmd)
