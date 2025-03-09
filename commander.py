from models import commander_model
import subprocess

while True:
    prompt = input(">>> ")
    for _ in range(3):
        command = commander_model.generate(prompt)
        print(command)
        output = subprocess.run([r"C:\Program Files\Git\bin\bash.exe", "-c", command], shell=True, capture_output=True)
        print(output)
        print(output.stdout.decode())
        if output.stderr != b'':
            print(output.stderr.decode())
            continue
        break 