import csv
import argparse


prev_time = 0
parser = argparse.ArgumentParser(description="Print timestamps to CSV")
parser.add_argument("interval", help="slowdown time (s)")
parser.add_argument("filepathcsv", help="csv filepath")
parser.add_argument("filepath", help="raw filepath")
args = parser.parse_args()
timedelay = args.interval
with open(args.filepathcsv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    time = 0
    for index, row in enumerate(csv_reader):
        
        if index > 0:
            print(f"file '{args.filepath}out.%06d.raw.tiff\\nduration %08f'" % (int(row[1]), timedelay * (int(row[2]) - time) / 1000000))
        time += int(row[2])
