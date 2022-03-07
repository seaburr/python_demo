import asyncio
import multiprocessing
import time
import os
import shutil
from multiprocessing import Pool
import concurrent.futures
from multiprocessing.pool import ThreadPool


source_directory = "/Volumes/Photos/Best Of"
serial_dest_dir = "/tmp/serial_files"
async_dest_dir = "/tmp/async_files"
multip_dest_dir = "/tmp/multip_files"
thread_dest_dir = "/tmp/thread_files"


# Generate list of files to download.
file_list = list()
for root, directory, name in os.walk(source_directory):
    for file in name:
        file_list.append(os.path.join(root, file))


async def copy_file(source, destination):
    shutil.copy2(source, destination)


async def async_copy():
    tasks = [copy_file(source=source, destination=async_dest_dir) for source in file_list]
    await asyncio.gather(*tasks)


def copy(source, destination):
    shutil.copy2(source, destination)


if __name__ == '__main__':

    core_count = multiprocessing.cpu_count()

    # Copy files in series.
    print(f"Copying {len(file_list)} files serially.")
    start_time = time.time()
    #for file in file_list:
    #    shutil.copy2(file, serial_dest_dir)
    completion_time = time.time() - start_time
    print(f"--- {completion_time} seconds ---")

    # Copy files using asyncio.
    print(f"Copying {len(file_list)} files asynchronously.")
    start_time = time.time()
    asyncio.run(async_copy())
    completion_time = time.time() - start_time
    print(f"--- {completion_time} seconds ---")

    # Copy files using multiprocessing.
    print(f'Copying {len(file_list)} files using multiprocessing ({core_count} subprocesses).')
    start_time = time.time()
    files_with_dest = list()
    for file in file_list:
        files_with_dest.append((file, multip_dest_dir))
    with Pool(core_count) as p:
        p.starmap(copy, files_with_dest)
    completion_time = time.time() - start_time
    print(f"--- {completion_time} seconds ---")

    # Copy files using threading.
    print(f'Copying {len(file_list)} files using threading ({core_count} threads).')
    start_time = time.time()
    files_with_dest = list()
    for file in file_list:
        files_with_dest.append((file, thread_dest_dir))
    with ThreadPool(8) as tp:
        tp.starmap(copy, files_with_dest)
    completion_time = time.time() - start_time
    print(f"--- {completion_time} seconds ---")





