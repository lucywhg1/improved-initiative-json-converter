import os
import json
import config
from formats import *

# Mapper for markdown generators
dispatch_get = {
    'homebrewery': homebrewery_format.get_markdown,
    'homebrewery_wide': homebrewery_format.get_markdown_wide
}


def setup_dir():
    # Create a converted folder in the origin directory and record path to config.
    dir_path = os.path.join(os.path.dirname(config.input_path), 'converted')
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    except Exception as error:
        print("Error creating output directory: {0}, {1}".format(
            error.__class__, error))
        raise

    config.dir_converted = dir_path


def overwrite_md(filepath, filename, content):
    print("Overwriting " + filename + "...")
    with open(filepath, 'w') as file:
        file.write(content)


def create_or_write_md(filename, content):
    # Attempt to create markdown with the given filename and content.
    # If overwriting, prompt user for behavior unless already set to overwrite all.
    filepath = os.path.join(config.dir_converted,
                            filename.replace(' ', '') + '.md')
    try:
        with open(filepath, 'x') as file:
            file.write(content)
    except FileExistsError:
        if config.overwrite_all:
            overwrite_md(filepath, filename, content)
        else:  # Prompt for overwrite behavior
            print("A file already exists at " + filepath + ".")
            filename_choice = input(
                "Type a new file name (no extension) below, '--overwrite', or '--overwrite -all':\n")
            if filename_choice.startswith('--overwrite'):
                overwrite_md(filepath, filename, content)

                if filename_choice.endswith('-all'):
                    config.overwrite_all = True
            else:  # Try again with the new name
                print("Creating with filename " + filename_choice + "...")
                create_or_write_md(filename_choice, content)


def convert_all(filepath, md_format, input_types):
    # Convert all records from the given JSON that match the chosen inputs.
    # For each, generate markdown in the chosen format.
    with open(filepath) as input_file:
        data = json.load(input_file)

    total = successes = 0

    for key in data:
        if any(input_type in key for input_type in input_types):
            total += 1
            record = data[key]
            if type(record) != dict and type(record) != list:
                print(
                    "Record {0} not JSON-loadable, type {1}. Skipping...".format(key, str(type(record))))
                continue

            try:
                record_md = ''
                if 'StatBlock' in record.keys():
                    record_md = dispatch_get[md_format](record['StatBlock'])
                else:
                    record_md = dispatch_get[md_format](record)

                create_or_write_md(record['Name'], record_md)
                successes += 1
            except Exception as error:
                print("Error loading {0}: {1}, {2}".format(
                    record['Id'], error.__class__, error))

    return total, successes
