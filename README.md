Simpler Illinois Crime Reports
==============================

The Illinois State Police releases state-wide crime data in its [Uniform Crime Reports](http://www.isp.state.il.us/crime/ucrhome.cfm) (UCRs), but those reports aren't always easy to work with. If you wanted to take a list of relevant places in Illinois and find their crime statistics in a UCR, for example, you'd have to jump through a lot of hoops to match across differently formatted police jurisdictions. This database removes most of those hoops.

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

Start by generating a Postgres database in the command line:

`createdb illinois_ucr`

We made this database specifically to get information about crimes in Chicago suburbs in 2014 and 2015. To generate that data as a CSV file, run:

`make crimes`

To just make the underlying database for every jurisdiction in Illinois:

`make database`

## Changing year or location

If you want to look at a different year or different jurisdictions, you can change a few lines of our code and run either of the above commands.

### Change the year

We retrieve the UCR by year in lines 24-26 of the `Makefile`:

```
.INTERMEDIATE: CrimeData_15_14.xlsx
CrimeData_15_14.xlsx :
    wget http://www.isp.state.il.us/docs/cii/cii15/ds/CrimeData_15_14.xlsx
```

To work with data from a different year, find its corresponding UCR at the [State Police website](http://www.isp.state.il.us/crime/ucrhome.cfm) and substitute the URL in line 26 before you run `make`.

### Change the location

We specify places of interest in the file `places.csv`. In line 59 of `Makefile`, we use those locations to query the database via the script `ucr_places.py`: 

```
output/suburb_crimes.csv : places.csv ucr_crime illinois_crosswalk identifiers_crosswalk
    mkdir -p output
    cat places.csv | python scripts/ucr_places.py $(PG_DB) > output/suburb
```

To work with different places, simply change `places.csv` to include only the places you're interested in before you run `make`. Make sure to follow the same schema (first column: placename, second column: FIPS code) so that `ucr_places.py` works properly. 
