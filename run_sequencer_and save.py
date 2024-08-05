import os
import sys
from subprocess import Popen,STDOUT
import random as rd
def run_simulation(simulation, DART_HOME, DART_LOCAL, DART_TOOLS, direction=True, phase=True, maket=True, dart=True):
    ext = '.bat' if sys.platform == 'win32' else '.sh'
    if direction and phase and maket and dart:
        steps = ['dart-full']
    else:
        steps = []
        if direction:
            steps.append('dart-directions')
        if phase:
            steps.append('dart-phase')
        if maket:
            steps.append('dart-maket')
        if dart:
            steps.append('dart-only')

    env = os.environ.copy()
    env['DART_HOME'] = DART_HOME
    env['DART_LOCAL'] = DART_LOCAL

    process = None
    log = open('run.log', 'w')

    for step in steps:
        cmd = (['bash'] if sys.platform != 'win32' else []) + [step + ext, simulation.split(os.sep + 'simulations' + os.sep, 1)[-1]]
        print(cmd)
        process = Popen(cmd, cwd=DART_TOOLS, env=env, stdout=log, stderr=STDOUT, shell=sys.platform == 'win32', universal_newlines=True)
        if process.wait() > 0:
            break
    log.close()
    return 0 if process is None else process.returncode
def run_sequence(sequencexml,DART_HOME,DART_LOCAL,DART_TOOLS,start=True):
    ext = '.bat' if sys.platform == 'win32' else '.sh'
    state = "-start" if start else "-continue"
    env = os.environ.copy()
    env['DART_HOME'] = DART_HOME
    env['DART_LOCAL'] = DART_LOCAL
    process = None
    log = open('run.log', 'w')
    cmd = (['bash'] if sys.platform != 'win32' else []) + [DART_TOOLS+"/dart-sequence"+ext,sequencexml,state]
    process = Popen(cmd, env=env, shell= False,universal_newlines=True)
    print(process.args)
    outs,errs = process.communicate()
    print(errs)
    print("finished batch")
    log.close()
    return 0 if process is None else process.returncode
number_of_sequences = 20
while True :
    os.system(f"python C:/DART/user_data/simulations/Simulation_monastir5_2parc/sequencemaker.py {number_of_sequences}")
    run_sequence("Simulation_monastir5_2parc/allproperty.xml","C:/DART","C:/DART/user_data","C:/DART/tools/windows")
    os.system(f"python saveTIFF.py {rd.random()}")
#run_simulation("Simulation_monastir5_2parc","C:/DART","C:/DART/user_data","C:/DART/tools/windows")