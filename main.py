import csv
import argparse

# TODO:
# fix decimal places in output files
# add headers to output files
# clean up

# Setup parser and arguments for file paths
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--team-map', metavar='team_map')
parser.add_argument('-p', '--product_master', metavar='product_master')
parser.add_argument('-s', '--sales', metavar='sales')
parser.add_argument('--team-report', metavar='team_report')
parser.add_argument('--product-report', metavar='product_report')

args = parser.parse_args()

# Define dictionaries to hold data
teams = {}
products = {}
sales_dict = {}
team_report = {}
product_report = {}

# Open Team Map file
with open(args.team_map) as team_map_file:
    csv_reader = csv.reader(team_map_file, delimiter=',')

    # Skip header
    next(csv_reader)

    # Read data into teams dictionary
    for row in csv_reader:
        teams[row[0]] = row[1]
        team_report[row[1]] = 0

# Open Product Master file
with open(args.product_master) as product_master_file:
    csv_reader = csv.reader(product_master_file, delimiter=',')

    # Read data into products dictionary
    for row in csv_reader:
        products[row[0]] = [row[1], row[2], row[3]]
        product_report[row[1]] = [0, 0, 0]

# Open Sales file and read in data
with open(args.sales) as sales_file:
    csv_reader = csv.reader(sales_file, delimiter=',')

    # Read data into sales dictionary
    for row in csv_reader:
        sales_dict[row[0]] = [row[1], row[2], row[3], row[4]]

# Process sales data
for sale in sales_dict.values():
    product = products[sale[0]]
    team = teams[sale[1]]

    # Update team's gross revenue (product price * lot size * number of lots sold)
    team_report[team] += float(product[1]) * float(product[2]) * float(sale[2])

    # Update product's gross revenue (product price * lot size * number of lots sold)
    product_report[product[0]][0] += float(product[1]) * float(product[2]) * float(sale[2])
    # Update product's total units sold (lots sold * lot size)
    product_report[product[0]][1] += float(sale[2]) * float(product[2])
    # Update product's discount cost (price * discount)
    product_report[product[0]][2] += float(product[1]) * (float(sale[3]) / 100)

# Write Team Report to file
with open(args.team_report, 'w+', newline='') as team_report_file:
    csv_writer = csv.writer(team_report_file)

    for key, value in team_report.items():
        csv_writer.writerow([key, value])

# Write Product Report to file
with open(args.product_report, 'w+', newline='') as product_report_file:
    csv_writer = csv.writer(product_report_file)

    for key, value in product_report.items():
        csv_writer.writerow([key, value[0], value[1], value[2]])
