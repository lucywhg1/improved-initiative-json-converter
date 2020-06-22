#!/usr/bin/env python
import argparse
import config
import helpers


def get_types_filtered():  # Prompt for custom entity conversion filter
    print("Supported Improved Initiative record categories are:")
    for record_type in config.record_types.keys():
        print("  - " + record_type)

    types_filtered_input = input(
        "What record types do you want to include? [Separate by ', '] \n")

    types_filtered = []

    for record_type in types_filtered_input.split(', '):
        if not record_type.lower() in config.record_types.keys():
            print("Unique record type included: " + record_type)
            types_filtered.append(record_type)
        else:
            types_filtered.append(config.record_types[record_type.lower()])

    return types_filtered


def run():  # Command line user view
    # Parse arguments
    parser = argparse.ArgumentParser(description='Process parameters.')
    parser.add_argument('input_path', metavar='I', type=str,
                        help='filepath for input JSON')
    parser.add_argument('--markdown_format', metavar='M', type=str, choices=helpers.dispatch_get.keys(),
                        help='markdown format for output: ' + ', '.join(helpers.dispatch_get.keys()))
    parser.add_argument('--overwrite', metavar='OV', type=bool,
                        help='whether to overwrite existing output files')
    parser.add_argument('--filter', metavar='F', type=bool,
                        help='whether to filter which entities to convert')
    args = parser.parse_args()

    # Set config
    config.input_path = args.input_path
    if args.markdown_format:
        config.md_format = args.markdown_format
    if args.overwrite:
        config.overwrite_all = args.overwrite

    if args.filter:
        config.types_filtered = get_types_filtered()
    else:
        config.types_filtered = config.record_types.values()  # default supported types

    helpers.setup_dir()  # Create output folder

    # Convert files
    print('==========')
    completion_data = helpers.convert_all(
        config.input_path, config.md_format, config.types_filtered)  # track total vs. success
    print("All done! Of {0} matched entities, {1} successfully converted.".format(
        *completion_data))


if __name__ == '__main__':
    run()
