#!/usr/bin/env python
"""
jsstdrpt.pv
"""
#
#  Imports
#
import datetime
import logging
import pathlib
#
#  Globals
#
rpt_file = None
rpt_path = None


def make_std_out_dir(dir=None):
    logging.info("begin make_std_out_dir({})".format(dir))

    if dir is None:
        output_dir = pathlib.Path.home() / "local" / "log"
    else:
        output_dir = pathlib.Path(dir)

    try:
        output_dir.mkdir(parents=True)
    except FileExistsError:
        pass

    logging.info("end   make_std_out_dir - returns {}".format(output_dir))
    return output_dir


def start_std_rpt(output_dir, prefix, format="%Y_%m_%d_%H_%M", version=None):
    global rpt_file
    global rpt_path

    logging.info(f"begin start_std_rpt({output_dir}, {prefix}, {format})")
    today = datetime.datetime.now().strftime(format)
    rpt_path = str(output_dir) + f"/{prefix}_{today}.rpt"
    rpt_file = open(rpt_path, "w")

    rpt_file.write(("=" * 132) + "\n")
    start_date = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S %z")
    rpt_file.write("Report " + prefix + " started at " + start_date + "\n")
    rpt_file.write(f"{prefix} version information - {version}\n")

    rpt_file.write(("=" * 132) + "\n")
    logging.info("end   start_std_rpt - returns None")


def finish_std_rpt(return_code):
    global rpt_file

    end_date = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S %z")

    if return_code == 0:
        rpt_file.write(f"\nFinished successfully at {end_date}\n")
    else:
        rpt_file.write(
            f"\nFailed with return code {return_code} at {end_date}\n"
        )
    rpt_file.write(("=" * 132) + "\n")
    rpt_file.close()
    logging.info("end   finish_std_rpt - returns None ")


def write(output_string):
    global rpt_file

    rpt_file.write(output_string)


def get_std_rpt_file():
    global rpt_file

    return rpt_file.name


def get_contents():
    with open(rpt_path) as file_contents:
        return file_contents.read()
