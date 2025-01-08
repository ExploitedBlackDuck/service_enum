import yaml
from pathlib import Path
from subprocess import run, PIPE, CalledProcessError

def run_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = run(command, shell=True, text=True, stdout=PIPE, stderr=PIPE, check=True)
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except CalledProcessError as e:
        return {
            "stdout": e.stdout.strip() if e.stdout else "",
            "stderr": e.stderr.strip() if e.stderr else "",
            "returncode": e.returncode
        }

def smb_enumeration(ip):
    """Performs SMB enumeration."""
    print(f"[+] Enumerating SMB on {ip}...")
    return {
        "smbclient": run_command(f"smbclient -L \\{ip} -N"),
        "rpcclient": run_command(f"rpcclient -U \"\" {ip}")
    }

def ldap_enumeration(ip):
    """Performs LDAP enumeration."""
    print(f"[+] Enumerating LDAP on {ip}...")
    return run_command(f"nmap -p 389 --script ldap-search {ip}")

def ftp_enumeration(ip):
    """Performs FTP enumeration."""
    print(f"[+] Enumerating FTP on {ip}...")
    return run_command(f"nmap -p 21 --script ftp-anon {ip}")

def process_services(ip, services):
    """Processes services for enumeration."""
    enum_functions = {
        "smb": smb_enumeration,
        "ldap": ldap_enumeration,
        "ftp": ftp_enumeration
    }
    results = {}
    for service in services:
        func = enum_functions.get(service)
        if func:
            print(f"[+] Running {service} enumeration...")
            results[service] = func(ip)
        else:
            print(f"[-] Unknown service: {service}")
    return results

def validate_yaml(data):
    """Validates the structure of the input YAML."""
    if not isinstance(data, dict):
        raise ValueError("Input YAML must be an object.")
    if "ip" not in data or "services" not in data:
        raise ValueError("YAML must contain 'ip' and 'services' keys.")
    if not isinstance(data["services"], list):
        raise ValueError("'services' must be a list.")
    if not all(isinstance(service, str) for service in data["services"]):
        raise ValueError("Each service in 'services' must be a string.")

def save_results(ip, results):
    """Saves results to a YAML file."""
    output_file = Path(f"service_enum_results_{ip}.yaml")
    try:
        with output_file.open("w") as outfile:
            yaml.dump(results, outfile, default_flow_style=False)
        print(f"[+] Enumeration complete. Results saved to {output_file}")
    except Exception as e:
        print(f"[-] Failed to save results: {e}")

def load_yaml(file_path):
    """Loads and parses a YAML file."""
    try:
        with file_path.open("r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error decoding YAML: {e}")

def main():
    input_file = input("Enter the path to the YAML file with detected open ports: ").strip()
    try:
        input_path = Path(input_file)
        if not input_path.is_file():
            print(f"[-] File not found: {input_file}")
            return

        data = load_yaml(input_path)
        validate_yaml(data)

        ip = data["ip"]
        services = data["services"]

        print(f"[+] Starting service enumeration for {ip}...")
        results = process_services(ip, services)

        save_results(ip, results)

    except FileNotFoundError:
        print(f"[-] The specified file does not exist: {input_file}")
    except ValueError as ve:
        print(f"[-] Input validation error: {ve}")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
