from pathlib import Path
from pprint import pprint

import mytextgrid


def get_tier_names(source_dir):
    source_dir = Path(source_dir)

    names = []
    for path in source_dir.rglob('*.TextGrid'):
        try:
            tg = mytextgrid.read_from_file(path, encoding='utf-8')
            tg._path = path
        except Exception as e:
            print(f'Could not read {path}: {e}')
            continue
       
        for tier in tg:
            name = tier.name
            if name in names:
                continue
            names.append(name)
    return names

def create_aligned_tier_table(source_dir, primary_tier_name, secondary_tier_names):
    """
    Reads TextGrid files from a source directory, aligns them based on a
    primary tier's intervals, and organizes the data into a table.

    Parameters
    ----------
    source_dir: str
        The path to the directory containing TextGrid files.
    primary_tier_name:  str
        The name of the tier to use as the key for alignment.
    secondary_tier_names: list of str
        A list of names of the secondary tiers to align with the primary tier.

    Returns
    -------
    tuple
        A tuple containing a list of headers and a list of lists representing 
        the aligned table data.
    """
    # Ensure the source directory path is a Path object
    source_dir = Path(source_dir)

    # Initialize data structures
    aligned_data = {}
    headers = ['filename', primary_tier_name] + secondary_tier_names

    # Process each TextGrid file in the source directory
    for path in source_dir.rglob('*.TextGrid'):
        try:
            tg = mytextgrid.read_from_file(path, encoding='utf-8')
            tg._path = path
        except Exception as e:
            print(f'Could not read {path}: {e}')
            continue

        # Get the primary tier
        for tier in tg:
            tier.parent = tg

            primary_tiers = [tier for tier in tg if tier.name == primary_tier_name]
            if not primary_tiers:
                print(f'Primary tier "{primary_tier_name}" not found in {path}. Skipping.')
                continue

            primary_tier = primary_tiers[0]

            for primary_interval in primary_tier:
                if not primary_interval.text.strip():
                    continue
 
                interval_times = (primary_interval.xmin, primary_interval.xmax)

                row = [None]*len(headers)
                row[0] = path
                row[1] = primary_interval

                aligned_data[interval_times] = row

            for tier in tg:
                if tier == primary_tier:
                    continue
                if tier.name in secondary_tier_names:
                    for secondary_interval in tier:
                        interval_times = (secondary_interval.xmin, secondary_interval.xmax)

                        if interval_times in aligned_data:
                            try:
                                tier_index = headers.index(tier.name)
                                aligned_data[interval_times][tier_index] = secondary_interval
                            except:
                                continue
    # Convert the dictionary of aligned data into a list of lists for the table model
#    pprint(aligned_data)   
    table_rows = list(aligned_data.values())
    return headers, table_rows
