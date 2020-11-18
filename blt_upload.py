#!/usr/bin/env python3

import sys
import argparse
import pysftp

def upload_file_to_blt(local_path=None, remote_path="~"):
	if not local_path or not remote_path:
		print("ERROR: Local Path and Remote Path are Required.")
		sys.exit(1)
	print(f"Uploading {local_path} to BLT at location {remote_path}")

def download_file_from_blt(local_path=".", remote_path=None):
	print(f"Downloading {remote_path} to BLT at location {remote_path}")
	if not local_path or not remote_path:
		print("ERROR: Local Path and Remote Path are Required.")
		sys.exit(1)