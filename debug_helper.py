import os
import subprocess
import time

cadwork_path = r"C:\cadwork.dir\ci_start.exe"
file_to_open = r"C:\Users\MichaelBrunner\Downloads\wandelement.3d"

print(f"Launching {cadwork_path} with file {file_to_open}")

process = subprocess.Popen([cadwork_path, file_to_open])

print("Application launched.")