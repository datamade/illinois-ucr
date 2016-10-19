Working with Illinois Crime Reports
==============================

The Illinois State Police releases state-wide crime data in its [Uniform Crime Reports](http://www.isp.state.il.us/crime/ucrhome.cfm) (UCRs), but those reports aren't always easy to work with. Most pressingly, the UCRs don't include unique IDs for each police jurisdiction, so it can be a pain to join them with different tables (say, to filter by a list of specific jurisdictions that you're interested in). This repo builds a [PostgreSQL database](http://www.postgresql.org/) with UCR data for 2014 and 2015, along with comprehensive [crosswalks](https://en.wikipedia.org/wiki/Schema_crosswalk) for querying by police jurisdiction.

## Installation

### Requirements
* [GNU Make](https://www.gnu.org/software/make/)
* [GNU Wget](https://www.gnu.org/software/wget/)
* [Python 3](https://www.python.org/downloads/)
* [csvkit](https://csvkit.readthedocs.io/en/latest/tutorial/1_getting_started.html#installing-csvkit)
* [PostgreSQL](http://www.postgresql.org/)

### Mac OS X
Most of these dependencies are installed by default. To get the rest using [pip](https://pypi.python.org/pypi/pip) and [homebrew](http://brew.sh):
```
brew install postgresql
pip install csvkit
```

### Ubuntu
Most of these dependencies are installed by default. To get the rest:
```
sudo apt-get install postgresql
pip install csvkit
```

## Making the database

Start by creating a Postgres database in the command line:

```
createdb illinois_ucr
```

Then use `make` to generate the tables:

```
make database
```

## Using the database

Once `make` finishes, take a look at your database by running `psql -d illinois_ucr -c "\d"`. You should see three tables:

```
                   List of relations
 Schema |         Name          | Type  |    Owner
--------+-----------------------+-------+--------------
 public | identifiers_crosswalk | table | <user>
 public | illinois_crosswalk    | table | <user>
 public | ucr_crime             | table | <user>
(3 rows)
```

- `ucr_crime` is the State Police 2014-15 crime report. It includes crimes organized by county as well as by police agency.
- `identifiers_crosswalk` is a master directory of police agencies across the United States. It can be filtered for Illinois using the `STATENAME` variable. (Full documentation of the crosswalk is available in the `documentation` directory.)
- `illinois_crosswalk` is a table that matches agency names between `identifiers_crosswalk` and `ucr_crime`. We built it using [Dedupe](https://dedupe.io/). 

### Sample query

For an example of using these tables for queries, see `scripts/sample_query.py`. The query in that script looks something like this:

```
SELECT (foo, bar, baz)
FROM identifiers_crosswalk
INNER JOIN illinois_crosswalk
USING ("NAME", "COUNTYNAME")
LEFT JOIN ucr_crime
USING ("Agency", "County")
WHERE "STATENAME" = 'ILLINOIS'
AND "FPLACE" = '{}'
GROUP BY "FPLACE"
```

Here, $FPLACE represents the jurisdictions we were interested in for one particular project.

## Can I see reports for a different year?

Possibly! We retrieve the UCR for 2014-15 in lines 24-26 of the `Makefile`:

```
.INTERMEDIATE: CrimeData_15_14.xlsx
CrimeData_15_14.xlsx :
    wget http://www.isp.state.il.us/docs/cii/cii15/ds/CrimeData_15_14.xlsx
```

To work with a report from a different year, find its corresponding UCR at the [State Police website](http://www.isp.state.il.us/crime/ucrhome.cfm) and try substituting the URL in line 26 before you run `make`. 
