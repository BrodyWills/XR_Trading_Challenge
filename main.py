import csv
import argparse

# Setup parser and arguments for file names
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--team-map', metavar='team_map')
parser.add_argument('-p', '--product_master', metavar='product_master')
parser.add_argument('-s', '--sales', metavar='sales')
parser.add_argument('--team-report', metavar='team_report')
parser.add_argument('--product-report', metavar='product_report')
args = parser.parse_args()

# Ensure all file names are given
if not all(vars(args).values()):
    print("Error: Missing filename parameter")
    exit()

# Define dictionaries to hold data
teams = {}
products = {}
sales_dict = {}
team_report = {}
product_report = {}

# Open Team Map file and read data into teams dictionary
with open(args.team_map) as team_map_file:
    csv_reader = csv.reader(team_map_file, delimiter=',')
    next(csv_reader)  # skip header
    for row in csv_reader:
        teams[row[0]] = row[1]
        team_report[row[1]] = 0

# Open Product Master file and read data into products dictionary
with open(args.product_master) as product_master_file:
    csv_reader = csv.reader(product_master_file, delimiter=',')
    for row in csv_reader:
        products[row[0]] = [row[1], row[2], row[3]]
        product_report[row[1]] = [0, 0, 0]

# Open Sales file and read in data and read data into sales dictionary
with open(args.sales) as sales_file:
    csv_reader = csv.reader(sales_file, delimiter=',')
    for row in csv_reader:
        sales_dict[row[0]] = [row[1], row[2], row[3], row[4]]

# Process sales data
for sale in sales_dict.values():
    product = products[sale[0]]
    team = teams[sale[1]]

    # Update team's gross revenue
    team_report[team] += float(product[1]) * float(product[2]) * float(sale[2])

    # Update product's gross revenue, units sold, discount cost
    product_report[product[0]][0] += float(product[1]) * float(product[2]) * float(sale[2])
    product_report[product[0]][1] += float(sale[2]) * float(product[2])
    product_report[product[0]][2] += float(product[1]) * (float(sale[3]) / 100)

# Write Team Report to file
with open(args.team_report, 'w+', newline='') as team_report_file:
    csv_writer = csv.writer(team_report_file)
    csv_writer.writerow(['Team', 'GrossRevenue'])
    for key, value in sorted(team_report.items(), key=lambda x: x[1], reverse=True):
        csv_writer.writerow([key, "{:.2f}".format(value)])

# Write Product Report to file
with open(args.product_report, 'w+', newline='') as product_report_file:
    csv_writer = csv.writer(product_report_file)
    csv_writer.writerow(['Name', 'GrossRevenue', 'TotalUnits', 'DiscountCost'])
    for key, value in sorted(product_report.items(), key=lambda x: x[1], reverse=True):
        csv_writer.writerow([key, "{:.2f}".format(value[0]), int(value[1]), "{:.2f}".format(value[2])])
