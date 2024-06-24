import os
import subprocess

# Constants
CHUNK_SIZE = 512 * 1024 * 1024

def get_file_sizes(directory):
    file_sizes = []
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            filesize = os.path.getsize(filepath)
            file_sizes.append((filepath, filesize))
    return file_sizes

def chunk_files(file_sizes):
    chunks = []
    current_chunk = []
    current_size = 0

    for filepath, filesize in file_sizes:
        if current_size + filesize > CHUNK_SIZE and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
        
        current_chunk.append(filepath)
        current_size += filesize

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def commit_and_push(chunk, commit_message):
    # Stage files
    subprocess.run(['git', 'add'] + chunk, check=True)

    # Commit
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

    # Push
    subprocess.run(['git', 'push'], check=True)

def main():
    file_sizes = get_file_sizes('.')
    chunks = chunk_files(file_sizes)

    for index, chunk in enumerate(chunks):
        commit_message = f"Add downloaded images, part {index + 1}"
        commit_and_push(chunk, commit_message)

if __name__ == "__main__":
    main()
