from funcx.sdk.client import FuncXClient
import os
import subprocess
import time

from blt_helpers import blt_transfer_func, run_function_and_print_result
from config import *

def convert_format(file, output, infmt="nexus", outfmt="phylip"):
    cmd = f"bioconvert --input {file} --infmt {infmt} --output {output} --outfmt {outfmt}"
    import subprocess
    return subprocess.check_output(cmd, shell=True)


def run_raxml_cmd(input_file,
                  run_name,
                  model_of_evolution="GTRGAMMA",
                  thread_count=12,
                  random_seed=None):
    import random
    r_sd = random_seed if random_seed is not None else random.randint(
        0, 200000000)
    cmd = f"raxmlHPC -T {thread_count} -m {model_of_evolution} -n {run_name} -s {input_file} -p {r_sd}"
    import subprocess
    return subprocess.check_output(cmd, shell=True)

def cleanup(input_file, run_name, intermediary, blt_username):
    cmd = f"rm -f {intermediary} ; rm -f /home/users/{blt_username}/*{run_name} ; rm -f {input_file}"
    import subprocess
    return subprocess.check_output(cmd, shell=True)


if __name__ == '__main__':
    fxc = FuncXClient()

    username = input("What is your BLT username? ")
    local_file = input("Where is the local file? ")
    remote_path = input("Where do you want to save the file on BLT? ")

    blt_transfer_func(mode="u",
                      remote_path=remote_path,
                      local_path=local_file,
                      username=username)
    print("Uploaded input file.")

    print("Converting .nex to .phylip...")
    run_function_and_print_result(fxc, convert_format,
                                  [remote_path, INTERMEDIARY_FILENAME],
                                  ep_id=BLT_SMALL_ID)
    print("Generating tree with raxml...")
    run_function_and_print_result(fxc, run_raxml_cmd,
                                  [INTERMEDIARY_FILENAME, RUN_NAME],
                                  ep_id=BLT_XLARGE_ID)
    _ = input()
    output_loc = input("Please paste in the output file name: ")
    final_loc = input("Where should the local file be saved? ")

    blt_transfer_func(mode="d",
                      remote_path=output_loc,
                      local_path=final_loc,
                      username=username)

    print(f"Please open the tree at {final_loc} with FigTree.")

    yes = input("Would you like to cleanup your files? y/N: ")
    if yes.lower() == "y":
      run_function_and_print_result(fxc, cleanup, [remote_path, RUN_NAME, INTERMEDIARY_FILENAME, username], ep_id=BLT_SMALL_ID)

    print("Done.")

    