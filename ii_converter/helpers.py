import os
import json
import config
from formats import *


supported_formats = ['homebrewery', 'homebrewery_wide']


def dispatch_get(md_format, obj, obj_name):
    # Mapper for markdown generators
    if md_format == supported_formats[0]:
        return homebrewery_format.get_markdown(obj, obj_name)
    elif md_format == supported_formats[1]:
        return homebrewery_format.get_markdown(obj, obj_name, wide=True)


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
                print("Creating " + filename_choice + ".md...")
                create_or_write_md(filename_choice, content)


def check_record_name(record, record_id):
    if 'Name' in record.keys():
        return record['Name']
    else:
        def prompt_for_name():
            name_input = input(
                record_id + ' does not have a Name. Type one below or press enter for Unknown Name.\n' +
                'Type --inspect to view the record.\n')

            if not name_input:
                return 'Unknown Name'
            elif name_input == '--inspect':
                print(record, end='\n\n')
                return prompt_for_name()
            else:
                return name_input

        return prompt_for_name()


def convert(filepath, md_format, filtered_types):
    # Convert all records from the given JSON that match the chosen filters.
    with open(filepath) as input_file:
        data = json.load(input_file)

    total = successes = 0

    def single_convert(record, record_id):
        # Convert a single record by generating markdown for the given format.
        nonlocal total
        total += 1
        if type(record) != dict and type(record) != list:
            print(
                "Record {0} not JSON-loadable, type {1}. Skipping...".format(
                    record_id, str(type(record))))
            return

        try:
            record_name = check_record_name(record, record_id)
            record_markdown = dispatch_get(md_format, record, record_name)

            create_or_write_md(record_name, record_markdown)
            nonlocal successes
            successes += 1
        except Exception as error:
            print("Error loading {0}: {1}, {2}".format(
                record_id, error.__class__, error))

    if '.' not in next(iter(data)):
        # Looking at single record, since key does not contain period, e.g. 'Creatures.12abc'
        single_convert(data, "Single record from " + filepath)
    else:  # Must be multiple records, handle each.
        for key in data:
            if any(record_type in key for record_type in filtered_types):  # record matches filters
                single_convert(data[key], key)

    return total, successes
