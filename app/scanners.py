import subprocess

def run_nmap_scan(target):
    try:
        result = subprocess.check_output(
            [r"C:\Program Files (x86)\Nmap\nmap.exe", "-sV", target],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Scan error: {e.output}"
    except FileNotFoundError:
        return "Error:nmap not found. Make sure it's installed and added to the PATH"