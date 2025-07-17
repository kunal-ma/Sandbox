# Task: CLI-based FFMPEG wrapper for automated video processing
# Description: Automates and simplifies FFMPEG-based video processing operations and adds support for batch processing

# Permissions: None
# Dependencies: FFMPEG tools installed and available in PATH

# --------------------------------------------------

# Importing necessary libraries
import re
import os
import sys
import glob
import subprocess

# Error handling
def error(issue, id=-1):
    match issue:
        case 1:
            print("\nError : Invalid input !")
        case 2:
            print("\nError : File does not exist !")
        case 3:
            print(f"\nError : FFMPEG Error {id}")
        case _:
            print("\nError : Error in Error o.O")
    sys.exit()

# Loading files    
def load():
    args = len(sys.argv)
    match args:
        case 1:
            files = [os.path.relpath(f) for f in glob.glob('*.mp4')]
        case 2:
            files = [sys.argv[1]]
        case _:
            files = []
            error(1)
    return files

# Operation selection menu
def menu(file):
    if file == 'y':
        print("\nSelect Operations: \n")
    else:
        print(f"\nSelect Operations for {file}: \n")
    print("1. Trim")
    print("2. Rotate")
    print("3. Crop")
    print("4. Resize")
    print("5. Optimize")
    print("\n0. Skip")
    
    select = input("\nSelection (e.g. 1,2,3): ").strip().split(',')
    option = {"1": trim, "2": rotate, "3": crop, "4": resize, "5": optimize}

    if '0' in select:
        return []
    if not select or any(n not in option for n in select):
        error(1)

    operations = [option[n] for n in select]
    return operations

# Naming convention
def name(file, task, final=False):
    if callable(task):
        id = task.__name__[0]
    elif isinstance(task, str):
        id = task[0]
    else:
        id = "Error"
        error(1)

    name, ext = os.path.splitext(os.path.basename(file))
    if final:
        return os.path.join("output", name + ext)
    else:
        return f"{name}_{id}{ext}"

# Process executor
def process(param, prev=False):
    issue = subprocess.call(param)
    if issue:
        error(3, issue)
    if prev:
        subprocess.call(['ffplay', param[-1]])
        os.remove(param[-1])

# Operation handler
def handler(file, param, fname):
    pname = name(file, "prev") 
    param[-1] = pname
    process(param, True)
    
    check = input("\nAccept these changes ? (y/n) : ").strip()
    if check == 'y':
        param[-1] = fname
        process(param)
        return fname
    return None

# OPR : Trim video length
def trim(file, fname):
    while True:
        print("\nTimestamp format : hh:mm:ss")
        start = input("Start timestamp  : ").strip()
        end = input("End timestamp    : ").strip()
        
        param = ['ffmpeg', '-ss', start, '-to', end, '-i', file, '-c', 'copy', file]
        out = handler(file, param, fname)
        if out:
            return out

# OPR : Rotate video
def rotate(file, fname):
    while True:
        print("\nSelect rotation angle:")
        print("1. (→)  90° Clockwise")
        print("2. (←)  90° Anti-Clockwise")
        print("3. (↑↓) 180° Flip ")
        
        select = input("\nSelection : ").strip()
        match select:
            case "1":
                angle = '-90.0'
            case "2":
                angle = '90.0'
            case "3":
                angle = '180.0'
            case _:
                angle = None
                error(1)
        
        param = ['ffmpeg', '-display_rotation:v:0', angle, '-i', file, '-c', 'copy', file]
        out = handler(file, param, fname)
        if out:
            return out

# OPR : Crop video
def crop(file, fname):
    param = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', file]
    trace = subprocess.run(param, stdout=subprocess.PIPE, text=True)
    resol = trace.stdout.strip()
    
    param = ['ffmpeg', '-i', file, '-vf', 'cropdetect', '-t', '3', '-f', 'null', '-']
    trace = subprocess.run(param, stderr=subprocess.PIPE, text=True)
    match = re.findall(r'crop=\d+:\d+:\d+:\d+', trace.stderr)
    if match:
        fsize = f"{match[-1]}"
    else:
        fsize = "No crop detected !"

    while True:
        frame = fsize
        print(f"\nDimensions: {resol}")
        print(f"Detected crop: {fsize}\n")
        check = input("Use this crop? (y to accept, otherwise ""w:h:x:y""): ").strip()
        if check != 'y':
            frame = f"crop={check}"
        param = ['ffmpeg', '-i', file, '-vf', frame, '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'copy', file]
        out = handler (file, param, fname)
        if out:        
            return 1

# OPR : Change video resolution
def resize(file, fname):
    while True:
        print("\nSelect new resolution:")
        print("1. 360p")
        print("2. 480p")
        print("3. 720p")
        
        select = input("\nSelection : ").strip()
        match select:
            case "1":
                res = 360
            case "2":
                res = 480
            case "3":
                res = 720
            case _:
                res = None
                error(1)
        
        # ffmpeg -i input.mp4 -vf scale=-1:720 -c:v libx264 -preset slow -crf 24 -c:a copy output.mp4
        param = ['ffmpeg', '-i', file, '-vf', f'scale=-2:{res}', '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'copy', file]
        out = handler(file, param, fname)
        if out:
            return out

# OPR : Optimize video
def optimize(file, fname):
    while True:
        param = ['ffmpeg', '-i', file, '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-c:a', 'copy', file]
        out = handler(file, param, fname)
        if out:
            return out

# Main function
def main():
    def control(file, tasks):
        fname = file
        for i, task in enumerate(tasks):
            out = name(file, task, i == len(tasks) - 1)
            fname = task(fname, out)
    
    files = load()
    if not os.path.exists("output"):
        os.mkdir("output")
    
    if len(files) > 1 and input("\nApply same operation for all files ? (y/n) : ").strip() == 'y':
        tasks = menu('y')
        for file in files:
            control(file, tasks)
    else:
        for file in files:
            subprocess.call(['ffplay', file])
            tasks = menu(file)
            control(file, tasks)

main()
