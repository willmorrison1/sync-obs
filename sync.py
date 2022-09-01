#!/usr/bin/python3

import argparse
import os
import time
import zipfile
from datetime import date, datetime
import json
from dataclasses import dataclass
import shutil
import glob


@dataclass
class Config:
    source: str
    destination: str
    archive_dir: str
    delete_empty_dirs: bool
    archive_older_than_mins: int
    archive_max_fill_fraction: float
    sync_repeat_time_mins: float
    rsync_opts: str

    def __post_init__(self, **kwargs):
        if not os.path.isabs(self.source) or not os.path.isabs(self.archive_dir):
            raise ValueError(
                "source and archive dir must not be relative directories. ")
        if not isinstance(self.archive_older_than_mins, int):
            raise TypeError("archive_older_than_mins must be int")
        if (self.archive_max_fill_fraction > 0.98) or \
                (self.archive_max_fill_fraction < 0.1):
            raise ValueError(
                "archive_max_fill_fraction should be between 0.1 and 98")
        if self.archive_older_than_mins < 0:
            raise ValueError("archive_older_than_mins must be positive integer")
        make_archive_dir(self.archive_dir)


def parse_config(config_file):
    with open(config_file) as json_file:
        config = Config(**json.load(json_file))
        return config


def app_setup(config_file):
    config = parse_config(config_file)
    return config


def app_cleanup(config):
    archive_usage = shutil.disk_usage(config.archive_dir)
    while (archive_usage.used / archive_usage.total) > config.archive_max_fill_fraction:
        archive_file_pattern = os.path.join(config.archive_dir, "???????.zip")
        files = glob.glob(f'{archive_file_pattern}')
        files.sort(key=os.path.getmtime, reverse=True)
        if len(files) > 0:
            os.remove(files.pop())
        else:
            print("Ran out of archive files to remove") 
            break


def make_archive_dir(archive_dir):
    """Make the archive directory."""
    if not os.path.exists(archive_dir):
        print("Archive " + archive_dir + " does not exist")
        os.makedirs(archive_dir, exist_ok=True)
        print("Created " + archive_dir)


def add_file_to_zip(zip_path, raw_file, compress_level_int=7):
    """Add file to a zip archive."""
    zip_pathdir = os.path.dirname(zip_path)
    if not os.path.exists(zip_pathdir):
        os.makedirs(zip_pathdir, exist_ok=True)
    z = zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED,
                        compresslevel=compress_level_int)
    z.write(raw_file)
    z.close()
    os.remove(raw_file)


def rsync_upload_file(filename, destination, rsync_opts):
    rsync_result = os.system(rsync_opts + " " + filename + " " +
                             os.path.join(destination, ""))
    if rsync_result != 0:
        raise ValueError(f"Rsync failed with result {rsync_result}")


def file_age(filename):
    file_ctime = os.path.getmtime(filename)
    file_age_mins = (time.time() - file_ctime) / 60
    return file_age_mins


def archive_file(filename, archive_dir):
    zipfile_name = date.today().strftime("%Y%j") + ".zip"
    zipfile_path = os.path.join(archive_dir, zipfile_name)
    if not os.path.exists(os.path.dirname(zipfile_path)):
        os.makedirs(os.path.dirname(zipfile_path))
    add_file_to_zip(zip_path=zipfile_path, raw_file=filename)


def delete_empty_src_directories(source_dir):
    for root, dirs, files in os.walk(os.path.join(source_dir + '')):
        if not os.listdir(root) and not root == source_dir:
            os.rmdir(root)


def sync_files(config):
    for path, folders, files in os.walk(config.source):
        for file in files:
            filename = os.path.join(path, file)
            try:
                sync_file(filename, config)
            except ValueError as e:
                print(e)

    if config.delete_empty_dirs:
        try:
            delete_empty_src_directories(config.source)
        except ValueError as e:
            print(f'Delete dirs failed. {e}')


def sync_file(filename, config):
    print(f'Rsyncing {filename}')
    rsync_upload_file(filename, config.destination, config.rsync_opts)
    if file_age(filename) > config.archive_older_than_mins:
        print(f'Archiving {filename}')
        archive_file(filename, config.archive_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Sync data to remote server and do local backup.')
    parser.add_argument(
        '--config_file', help='Directory to configuration file', type=str,
        default="sync_config.json")

    args = parser.parse_args()
    repeat_time_wait = 0
    while True:
        print(f'sleeping for {repeat_time_wait} minutes')
        time.sleep(repeat_time_wait * 60)
        time_start = datetime.utcnow()
        config = app_setup(args.config_file)
        sync_files(config)
        app_cleanup(config)
        time_end = datetime.utcnow()
        time_taken = (time_end - time_start).total_seconds()
        repeat_time_wait = config.sync_repeat_time_mins - (time_taken / 60)
        if repeat_time_wait < 0:
            repeat_time_wait = 0
