import yadisk
import os
import posixpath
from dotenv import load_dotenv

load_dotenv

client = yadisk.Client(token=os.getenv('YADISKTOKEN'))

def recursive_upload(client: yadisk.Client, from_dir: str, to_dir: str):
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)

        try:
            client.mkdir(dir_path)
        except yadisk.exceptions.PathExistsError:
            pass

        for file in files:
            file_path = posixpath.join(dir_path, file)
            p_sys = p.replace("/", os.path.sep)
            in_path = os.path.join(from_dir, p_sys, file)

            try:
                recursive_upload(in_path, file_path)
            except yadisk.exceptions.PathExistsError:
                pass


to_dir = "/test"
from_dir = "/home/ubuntu"
recursive_upload(client, from_dir, to_dir)
