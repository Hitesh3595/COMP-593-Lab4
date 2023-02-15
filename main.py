import os
import re
import sys

import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# add path to import common functions

from common import filter_log_by_regex, get_log_file_path_from_cmd_line


def main():
    log_file = get_log_file_path_from_cmd_line()
    dest_port_dict = tally_port_traffic(log_file)
    for port_num, count in dest_port_dict.items():
        if count >= 100:
            generate_port_traffic_report(log_file, port_num)
    
    generate_invalid_user_report(log_file)
    generate_source_ip_log(log_file, "220.195.35.40")


def tally_port_traffic(log_file):
    """
    Reads given log file and check number of records of each destination port

    Params:
        log_file: path of log file
    
    Returns:
        A dict with destination-port-number as key and number of records as its value.
    """

    file = open(log_file)
    log_data = file.readlines()
    file.close()

    dest_port_dict = {}

    regex = r"DPT=(.*?) "
    for line in log_data:
        match = re.search(regex, line)
        if not match:
            continue

        matched_groups = match.groups()
        port = matched_groups[0]
        try:
            dest_port_dict[port] += 1
        except KeyError:
            dest_port_dict[port] = 1

    return dest_port_dict


def generate_port_traffic_report(log_file, port_number):
    """
    Creates a csv file which will contains logs with given destination port

    Params:
        log_file (str): path of log file
        port_number (int | str): destination port whose logs we want to see
    """

    regex = r'^([a-zA-Z]{3} \d+) ([0-9:]{8}).*SRC=(.*?) DST=(.*?) .* SPT=(.*?) DPT=(%(port_number)s) '
    regex = regex % {"port_number": port_number}
    _, data = filter_log_by_regex(log_file, regex)

    file_name = os.path.join(CURRENT_DIR, f"destination_port_{port_number}_report.csv")
    columns = [
        "Date",
        "Time",
        "Source IP Address",
        "Destination IP Address",
        "Source Port",
        "Destination Port",
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, index=False)
    return


def generate_invalid_user_report(log_file):
    """
    Creates csv file which will contains log data of invalid users.

    Params:
        log_file: path of log file
    """

    regex = r"^([a-zA-Z]{3} \d+) ([0-9:]{8}).*Invalid user ([a-zA-Z0-9]+) from ([0-9\.]+)"
    _, data = filter_log_by_regex(log_file, regex)

    file_name = os.path.join(CURRENT_DIR, "invalid_users.csv")
    columns = ["Date", "Time", "Username", "IP Address"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, index=False)
    return


def generate_source_ip_log(log_file, ip_address: str):
    """
    Creates a new file which will contains logs of given ip-address only.

    Params:
        log_file: path of log file
        ip_address: IP address of which we want to see logs
    """

    regex = rf"SRC=({ip_address})"
    data, _ = filter_log_by_regex(log_file, regex)

    ip_address = ip_address.replace(".", "_")
    file_name = os.path.join(CURRENT_DIR, f"source_ip_{ip_address}.log")

    with open(file_name, 'a') as f:
        f.writelines(data)

    return

if __name__ == '__main__':
    main()
