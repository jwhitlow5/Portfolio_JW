import subprocess
import os
import argparse



def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"err {command}: {stderr}")
    else:
        print(stdout)

def main():
    parser = argparse.ArgumentParser(description="input camera fps and output resolution")
    parser.add_argument("fps=660", help="frames per sec")
    parser.add_argument("h=64", help="height")
    parser.add_argument("w=640", help="width")
    args = parser.parse_args()
    fps = args.fps
    h=args.h
    w=args.w
    #run video acquisition using raspiraw
    run_command('./raspiraw -md 7 -t 1000 -ts /dev/shm/tstamps.csv -hd0 /dev/shm/hd0.32k -h ' + f'{h} -w {w} --vinc 1F --fps {fps} -sr 1 -o /dev/shm/out.%06d.raw')
    #concatenate RAW with bash
    run_command("ls /dev/shm/*.raw | while read i; do cat /dev/shm/hd0.32k \"$i\" > \"$i\".all; done")
    #use dcraw to convert RAW to TIFF
    run_command("ls /dev/shm/*.all | while read i; do ~/dcraw/dcraw -f -o 1 -v -6 -T -q 3 -W \"$i\"; done")
    #python script parses timestamp data
    run_command("python /dev/shm/make_concat.py 50 ./ ./output/")
    #convert tiff to png for analyze_particles.py
    run_command("ls /dev/shm/*.tiff | while read i; do convert \"$i\" \"/dev/shm/output/$(basename \"$i\" .tiff).jpg\"; done")
    #add logic here later
    #run particle analysis script on all frames
    run_command("python /dev/shm/analyze_particles.py")
if __name__ == "__main__":
    main()
