import time

from config import *
from blt_transfer import upload_file_to_blt, download_file_from_blt

def blt_transfer_func(mode="u",
                      remote_path=None,
                      local_path=None,
                      username=None):
    if mode == "u":
        upload_file_to_blt(local_path=local_path,
                           remote_path=remote_path,
                           username=username,
                           force=True)
    elif mode == "d":
        download_file_from_blt(local_path=local_path,
                               remote_path=remote_path,
                               username=username,
                               force=True)

def run_function_and_print_result(fxc,
                                  py_fn,
                                  py_fn_args,
                                  ep_id="3c3f0b4f-4ae4-4241-8497-d7339972ff4a"
                                  ):
    func_uuid = fxc.register_function(py_fn)
    res = fxc.run(*py_fn_args, endpoint_id=ep_id, function_id=func_uuid)
    while True:
        try:
            print("Waiting for results...")
            time.sleep(SLEEP_TIME)
            byte_string = fxc.get_result(res)
            real_string = str(byte_string, encoding="utf-8")
            print(real_string.replace("\\n", '\n'))
            break
        except Exception as e:
            if "waiting-for" in str(e):
                continue
            raise e