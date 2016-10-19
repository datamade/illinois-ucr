import psycopg2
import csv
import sys

DB = sys.argv[1]

conn = psycopg2.connect("dbname='{}'".format(DB))

cursor = conn.cursor()

fips_query = """SELECT MAX("Agency"),
		SUM("15pop") AS "Population 2015", 
		SUM("CH15") AS "Homicide 2015", 
		SUM("Rape15") AS "Rape 2015", 
		SUM("Rob15") AS "Robbery 2015", 
		SUM("AggBA15") AS "Aggravated assault 2015", 
		SUM("Burg15") AS "Burglary 2015", 
		SUM("Theft15") AS "Theft 2015", 
		SUM("MVT15") AS "Motor theft 2015", 
		SUM("Arson15") AS "Arson 2015", 
		SUM("Acca15") AS "Cannabis 2015", 
		SUM("Acsa15") AS "Controlled substance 2015", 
		SUM("Adpa15") AS "Drug paraphernalia 2015", 
		SUM("Ahsna15") AS "Hypodermic needle 2015", 
		SUM("Ameth15") AS "Methamphetamine 2015", 
		SUM("Adrug15") AS "Total drug crime 2015", 
		SUM("14pop") AS "Population 2014", 
		SUM("CH14") AS "Homicide 2014", 
		SUM("Rape14") AS "Rape 2014", 
		SUM("Rob14") AS "Robbery 2014", 
		SUM("AggBA14") AS "Aggravated assault 2014", 
		SUM("Burg14") AS "Burglary 2014", 
		SUM("Theft14") AS "Theft 2014", 
		SUM("MVT14") AS "Motor theft 2014", 
		SUM("Arson14") AS "Arson 2014", 
		SUM("Acca14") AS "Cannabis 2014", 
		SUM("Acsa14") AS "Controlled substance 2014", 
		SUM("Adpa14") AS "Drug paraphernalia 2014", 
		SUM("Ahsna14") AS "Hypodermic needle 2014", 
		SUM("Ameth14") AS "Methamphetamine 2014", 
		SUM("Adrug14") AS "Total drug crime 2014" 
                FROM identifiers_crosswalk 
                INNER JOIN illinois_crosswalk
                USING ("NAME", "COUNTYNAME")
                LEFT JOIN ucr_crime
                USING ("Agency", "County")
                WHERE "STATENAME" = 'ILLINOIS'
                AND "FPLACE" = '{}'
                GROUP BY "FPLACE"
                """
HEADER = ['Place', 'Agency', 'Population 2015', 'Homicide 2015', 'Rape 2015',
          'Robbery 2015', 'Aggravated assault 2015', 'Burglary 2015', 'Theft 2015',
          'Motor theft 2015', 'Arson 2015', 'Cannabis 2015', 'Controlled substance 2015',
          'Drug paraphernalia 2015', 'Hypodermic needle 2015', 'Methamphetamine 2015',
          'Total drug crime 2015', 'Population 2014', 'Homicide 2014', 'Rape 2014',
          'Robbery 2014', 'Aggravated assault 2014', 'Burglary 2014', 'Theft 2014',
          'Motor theft 2014', 'Arson 2014', 'Cannabis 2014',
          'Controlled substance 2014', 'Drug paraphernalia 2014',
          'Hypodermic needle 2014', 'Methamphetamine 2014', 'Total drug crime 2014']

reader = csv.reader(sys.stdin)
next(reader)

writer = csv.writer(sys.stdout)
writer.writerow(HEADER)

for name, fips in reader:
    cursor.execute(fips_query.format(fips))
    crimes = cursor.fetchone()
    if crimes:
        writer.writerow((name,) + crimes)
    else:
        writer.writerow((name,) + (None,) * (len(HEADER) -1) )

cursor.close()
conn.close()
