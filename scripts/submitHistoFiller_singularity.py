import os
import argparse
import itertools

def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)
    else:
        mes = f'Folder {d} already exists. You may want to remove it with `rm -r {d}`'
        raise ValueError(mes)

def launch_jobs(args):
    # create various path
    tagdir = os.path.join(args.outdir, args.tag + '_' + args.year, args.channel)
    create_dir(tagdir)

    singularity_script = 'insingularity.sh'
    launcher_script = 'filler.sh'
    condor_script = launcher_script.replace('.sh', '.condor')

    singularity_path = os.path.join(tagdir, singularity_script)
    launcher_path = os.path.join(tagdir, launcher_script)
    condor_path = os.path.join(tagdir, condor_script)

    logs_dir = os.path.join(tagdir, 'logs')
    create_dir(logs_dir)

    # Determine the main configuration file
    if args.cfg is None:
        if args.with_dnn:
            main_cfg_template = f"config/limits/mainCfg_{args.channel}_{args.year}_m{{MASS}}_s{{SPIN}}.cfg"
        else:
            main_cfg_template = f"config/mainCfg_{args.channel}_{args.year}.cfg"
    else:
        main_cfg_template = f"config/{args.cfg}.cfg"

    # Handle DNN-specific configurations
    if args.with_dnn:
        from create_limit_configs import Params
        pars = Params(args.year)
        spin_mass_dirs = []
        for spin, mass in itertools.product(pars.spins, pars.masses):
            subdir = os.path.join(tagdir, f"Spin{spin}_Mass{mass}")
            create_dir(subdir)
            spin_mass_dirs.append((spin, mass, subdir))

    # Create the singularity script
    with open(singularity_path, 'w') as s:
        if args.with_dnn:
            singularity_content = f"""#!/bin/bash
PROCESS_ID=$1
SPIN=$2
MASS=$3
echo $SCRAM_ARCH
export EXTRA_CLING_ARGS=-O2
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {os.getcwd()}
eval `scram r -sh`
source scripts/setup.sh
echo $PWD
testAnalysisHelper.exe {main_cfg_template} $PROCESS_ID {args.njobs} $PWD/Spin${{SPIN}}_Mass${{MASS}} {int(args.use_friend)}
"""
        else:
            singularity_content = f"""#!/bin/bash
PROCESS_ID=$1
echo $SCRAM_ARCH
export EXTRA_CLING_ARGS=-O2
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {os.getcwd()}
eval `scram r -sh`
source scripts/setup.sh
echo $PWD
testAnalysisHelper.exe {main_cfg_template} $PROCESS_ID {args.njobs} {tagdir} {int(args.use_friend)}
"""
        s.write(singularity_content)
    os.system(f'chmod u+rwx {singularity_path}')

    # Create the launcher script
    with open(launcher_path, 'w') as l:
        if args.with_dnn:
            launcher_content = f"""#!/bin/bash
JOB_ID=$1
SPIN=$2
MASS=$3
export KRB5CCNAME=/gwpool/users/{os.environ['USER']}/krb5cc_`id -u {os.environ['USER']}`
/usr/bin/eosfusebind -g; cd /eos/cms/;
cd {os.getcwd()}
/cvmfs/cms.cern.ch/common/cmssw-cc7 -B /gwdata:/gwdata -B /gwteras:/gwteras \\
    --command-to-run {singularity_path} $JOB_ID $SPIN $MASS
"""
        else:
            launcher_content = f"""#!/bin/bash
JOB_ID=$1
export KRB5CCNAME=/gwpool/users/{os.environ['USER']}/krb5cc_`id -u {os.environ['USER']}`
/usr/bin/eosfusebind -g; cd /eos/cms/;
cd {os.getcwd()}
/cvmfs/cms.cern.ch/common/cmssw-cc7 -B /gwdata:/gwdata -B /gwteras:/gwteras \\
    --command-to-run {singularity_path} $JOB_ID
"""
        l.write(launcher_content)
    os.system(f'chmod u+rwx {launcher_path}')

    # Create the condor script
    with open(condor_path, 'w') as c:
        condor_content = f"""Universe = vanilla
Executable = {launcher_path}

should_transfer_files = NO

+JobFlavour = "{args.queue}"
+JobBatchName = "{args.tag}"

output = {logs_dir}/$(Process).out
error = {logs_dir}/$(Process).err
log = {logs_dir}/$(Process).log
Requirements = ((machine == \"clipper.hcms.it\") || (machine == \"pccms12.hcms.it\") || (machine == \"pccms13.hcms.it\") || (machine == \"pccms14.hcms.it\"))
"""
        if args.with_dnn:
            condor_content += """
Arguments = $(Process) $(Spin) $(Mass)
queue Process, Spin, Mass from (
"""
            for spin, mass, _ in spin_mass_dirs:
                condor_content += f"  {spin}, {mass}\\n"
            condor_content += ")\\n"
        else:
            condor_content += f"""
Arguments = $(Process)
queue {args.njobs}
"""
        c.write(condor_content)

    # Submit the condor job
    launch_command = f'condor_submit {condor_path}'
    print(f'The following command was run: {launch_command}')
    os.system(launch_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command line parser of job options')
    parser.add_argument('-o', '--outdir', dest='outdir', required=False,
                        default=os.path.join('/data_CMS/cms/', os.environ['USER'], 'HHresonant_hist'),
                        help='Name of working space (defaults to timestamp)')
    parser.add_argument('-t', '--tag', required=True, help='Name of working space.')
    parser.add_argument('--cfg', help='Configuration file.', default=None)
    parser.add_argument('--njobs', required=False, type=int,
                        help='Number of jobs for parallelization', default=10)
    parser.add_argument('--year', required=True, choices=("UL16APV", "UL16", "UL17", "UL18"),
                        help='Data period.')
    parser.add_argument('--channel', required=True, choices=("ETau", "MuTau", "TauTau", "MuMu"),
                        help='Analysis channel.')
    parser.add_argument('--with_dnn', action='store_true',
                        help='Parallellize over spin and masses for DNN.')
    parser.add_argument('--use_friend', action='store_true',
                        help='Use TTree friend mechanism (implies the existence of another tree).')
    parser.add_argument('--queue', required=False, type=str, default='longlunch',
                        help='Size of the HTCondor queue.')

    FLAGS = parser.parse_args()

    launch_jobs(FLAGS)
