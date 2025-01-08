# service_enum.py Documentation

## Overview
`service_enum.py` is a Python-based tool designed to facilitate network service enumeration. The script automates the process of collecting information about specific services running on a target IP address, such as SMB, LDAP, and FTP. By leveraging external tools like `smbclient`, `rpcclient`, and `nmap`, it provides detailed insights into the target system's configuration.

---

## Key Features
- **Comprehensive Enumeration**: Supports SMB, LDAP, and FTP enumeration using standard command-line tools.
- **Flexible Input**: Accepts configuration via a user-defined YAML file.
- **Detailed Output**: Saves results in an organized YAML format, making it easy to review and analyze.
- **Error Handling**: Validates input and gracefully handles errors from both the script and external tools.

---

## Requirements
### System Requirements
- Python 3.x
- External tools:
  - `smbclient`
  - `rpcclient`
  - `nmap` with the following scripts installed:
    - `ldap-search`
    - `ftp-anon`

### Python Dependencies
- `pyyaml`
- `pathlib`
- `subprocess`

Install required Python packages:
```bash
pip install pyyaml
```

---

## Usage

### Input YAML File
Create a YAML file with the following structure:
```yaml
# Example: input_services.yaml
ip: "192.168.1.100"
services:
  - smb
  - ldap
  - ftp
```
- `ip`: The target IP address.
- `services`: A list of services to enumerate (supported values: `smb`, `ldap`, `ftp`).

### Running the Script
Run the script from the command line:
```bash
python service_enum.py
```
You will be prompted to enter the path to the YAML input file:
```
Enter the path to the YAML file with detected open ports: input_services.yaml
```

### Output
The results will be saved in a file named `service_enum_results_<IP>.yaml`, where `<IP>` is the target IP address. For example:
```
service_enum_results_192.168.1.100.yaml
```
This file contains detailed output for each enumerated service.

---

## Function Breakdown

### 1. `run_command(command)`
Executes shell commands and returns the output.
- **Input**: A shell command as a string.
- **Output**: A dictionary containing:
  - `stdout`: Command output.
  - `stderr`: Command errors.
  - `returncode`: Exit status.

### 2. `smb_enumeration(ip)`
Performs SMB enumeration using `smbclient` and `rpcclient`.
- **Input**: Target IP address.
- **Output**: Results from both tools.

### 3. `ldap_enumeration(ip)`
Executes LDAP enumeration using the `ldap-search` script in `nmap`.
- **Input**: Target IP address.
- **Output**: LDAP data as returned by `nmap`.

### 4. `ftp_enumeration(ip)`
Checks for anonymous FTP access using the `ftp-anon` script in `nmap`.
- **Input**: Target IP address.
- **Output**: FTP enumeration results.

### 5. `process_services(ip, services)`
Iterates through the list of services and invokes the corresponding enumeration function.
- **Input**:
  - `ip`: Target IP address.
  - `services`: List of services to enumerate.
- **Output**: A dictionary of results for each service.

### 6. `validate_yaml(data)`
Validates the structure of the YAML input file.
- **Input**: Parsed YAML data.
- **Output**: Raises `ValueError` for invalid input.

### 7. `save_results(ip, results)`
Writes the enumeration results to a YAML file.
- **Input**:
  - `ip`: Target IP address.
  - `results`: Results of service enumeration.
- **Output**: YAML file.

### 8. `load_yaml(file_path)`
Parses the input YAML file.
- **Input**: Path to the YAML file.
- **Output**: Parsed YAML data.

### 9. `main()`
The main entry point of the script. Handles user input, invokes service enumeration, and saves results.

---

## Error Handling
- **File Not Found**: Alerts the user if the input YAML file is missing.
- **Invalid YAML**: Validates input format and structure, raising errors for malformed files.
- **Unsupported Services**: Skips services not included in the predefined list (`smb`, `ldap`, `ftp`).
- **Command Execution Errors**: Captures and logs errors from external tools.

---

## Example Workflow
1. Create an input YAML file (`input_services.yaml`) with the target IP and desired services.
2. Run the script:
   ```bash
   python service_enum.py
   ```
3. Provide the path to the YAML input file when prompted.
4. Review the output saved in the YAML results file.

---

## Enhancements for Future Versions
- Add support for more services and protocols.
- Enable multi-threading for faster enumeration.
- Implement verbose and quiet modes for output control.
- Include optional JSON output format.
- Add configuration file support for advanced options.

---

## Disclaimer
This script is intended for ethical and authorized use only. Unauthorized use on systems without explicit permission is prohibited.

---

## License
This project is licensed under the MIT License.

## Author
Paul Ammann
