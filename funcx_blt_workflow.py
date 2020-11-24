from funcx.sdk.client import FuncXClient
import os
import subprocess
from .blt_transfer import upload_file_to_blt, download_file_from_blt


def blt_transfer(mode="u", remote_path=None, local_path=None, username=None):
    if mode == "u":
        upload_file_to_blt(local_path=local_path,
                           remote_path=remote_path,
                           username=username)
    elif mode == "d":
        download_file_from_blt(local_path=local_path,
                               remote_path=remote_path,
                               username=username)


def convert_format(file, output, infmt="nexus", outfmt="phylip"):
    cmd = f"bioconvert --input {file} --infmt {infmt} --output {outpath} --outfmt {outfmt}"
    import subprocess
    return subprocess.check_output(cmd, shell=True)


def run_function_and_print_result(py_fn, py_fn_args, ep_id="3c3f0b4f-4ae4-4241-8497-d7339972ff4a"):
    func_uuid = fxc.register_function(convert_format)
    res = fxc.run(*py_fn_args
                  endpoint_id=blt_small,
                  function_id=func_uuid)
    while True:
        try:
            print(fxc.get_result(res))
            break
        except Exception as e:
            if "waiting-for-ep" in e:
                continue
            else:
                raise e


if __name__ == '__main__':
    fxc = FuncXClient()
    remote_path = input("Where do you want to save the file?")
    username = input("What is your BLT username?")
    blt_transfer(mode="u",
                 remote_path=remote_path,
                 local_path=input("Where is the local file?"),
                 username=username)
    run_function_and_print_result(convert_format, [remote_path, "int_file.phylip"], ep_id="3c3f0b4f-4ae4-4241-8497-d7339972ff4a")
    
