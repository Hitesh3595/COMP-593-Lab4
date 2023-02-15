import re
import sys
import os

def get_log_file_path_from_cmd_line():
    """Retuns file path provided in command."""
    if len(sys.argv) < 2:
        print("Please provide log file path.")
        exit()
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("Please provide a valid path.")
        exit()
    return file_path


def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    """Gets a list of records in a log file that match a specified regex.

    Args:
        log_file (str): Path of the log file
        regex (str): Regex filter
        ignore_case (bool, optional): Enable case insensitive regex matching. Defaults to True.
        print_summary (bool, optional): Enable printing summary of results. Defaults to False.
        print_records (bool, optional): Enable printing all records that match the regex. Defaults to False.

    Returns:
        (list, list): List of records that match regex, List of tuples of captured data
    """
    with open(log_file) as file:
        data = file.readlines()

    if ignore_case:
        match_type = "case-insensitive match"
        extra_kwargs = {
            "flags": re.IGNORECASE,
        }
    else:
        # case sensitive match
        match_type = "match"
        extra_kwargs = {}

    count = 0
    matched_records = []
    df_list = []
    for line in data:
        matched = re.search(regex, line, **extra_kwargs)
        if not matched:
            continue

        count += 1
        matched_records.append(line)
        if print_records:
            print(line)

        df_list.append(matched.groups())

    if print_summary:
        print(f'The log file contains {count} records that {match_type} the regex "{regex}"')

    return matched_records, df_list
