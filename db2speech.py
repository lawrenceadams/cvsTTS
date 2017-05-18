"""
db2speech2.py converts a list in a .csv form to .mp3's of the specified term
"""
# pylint: disable=invalid-name
import os
import csv
import argparse
from progress.bar import IncrementalBar
from gtts import gTTS


def processTerms(targetFile):
    """
    A function that opens a csv file and producdes .mp3 files of each term.abs
    Takes a local file .csv
    """
    with open(targetFile) as csv_file:
        terms = csv.reader(csv_file, delimiter=',')
        length_of_terms = sum(1 for row in terms)
        csv_file.seek(0)
        prog_bar = IncrementalBar(
            'Generating speech...', max=length_of_terms, suffix='Remaining time: %(eta)ds')

        for term in terms:
            prog_bar.message = 'Processing ID: ' + term[1]
            gTTS(text=term[0], lang='en', slow=False).save(term[1] + '.mp3')
            prog_bar.next()
        prog_bar.finish()

parser = argparse.ArgumentParser(description="Process CSV values to speech.")
parser.add_argument("source_file", nargs="?", default="empty_string")
parser.add_argument("--clean", action="store_true")

args = parser.parse_args()

if args.source_file != "empty_string":
    print("Opening: " + args.source_file)
    try:
        processTerms(args.source_file)
    except FileNotFoundError as e:
        print("File not found! Please file location and try again. \n \n")
        raise e
    except Exception as e:
        raise e

if args.clean:
    print("Cleaning .mp3 files.")
    for item in os.listdir(os.getcwd()):
        if item.endswith(".mp3"):
            os.remove(item)
