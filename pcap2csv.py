import os
import csv

cmd = "tshark -n -r {0} -T fields -Eheader=y -e ip.addr > tmp.csv"

os.system(cmd.format("wireshark_sample.pcap"))

result = []

with open("tmp.csv", "r") as infile:
    for line in infile:
        if line == "\n":
            continue
        else:
            result.append(line.strip().split(","))

with open('sample.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for line in result:
        writer.writerow(line)

os.system("rm tmp.csv")