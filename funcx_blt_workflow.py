from funcx.sdk.client import FuncXClient
import os
import subprocess



def blt_transfer(mode="u", remote_path=None, local_path=None, username=None):
	cmd = f"python3 blt_transfer.py -{mode} -n {username} -l {local_path} -r {remote_path}"
	print(subprocess.check_output(cmd, shell=True))

def convert_format(file, output, infmt="nexus", outfmt="phylip"):
	cmd = f"bioconvert --input {file} --infmt {infmt} --output {outpath} --outfmt {outfmt}"
	import subprocess
	return subprocess.check_output(cmd, shell=True)

if __name__ == '__main__':
	fxc = FuncXClient()
	remote_path=input("Where do you want to save the file?")
	username=input("What is your BLT username?")
	blt_transfer(mode="u", remote_path=remote_path, local_path=input("Where is the local file?"), username=username)
	func_uuid = fxc.register_function(convert_format)
	blt_small = "3c3f0b4f-4ae4-4241-8497-d7339972ff4a"
	res = fxc.run(remote_path, "file.phylip", endpoint_id=blt_small, function_id=func_uuid)
	while True:
		try:
			print(fxc.get_result(res))
			break
		except Exception as e:
			if "waiting-for-ep" in e:
				continue
			else:
				raise e
