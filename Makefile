# -----------------------------------------
# Makefile directives
# -----------------------------------------

MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

PG_DB = illinois_ucr
CHECK_RELATION = psql -d $(PG_DB) -c "\d $@" > /dev/null 2>&1

.PHONY: database
database : ucr_crime illinois_crosswalk identifiers_crosswalk

# -----------------------------------------
# Pull crime data for Illinois
# -----------------------------------------

# get UCR report for 2014-15
.INTERMEDIATE: CrimeData_15_14.xlsx
CrimeData_15_14.xlsx :
	wget http://www.isp.state.il.us/docs/cii/cii15/ds/CrimeData_15_14.xlsx

.INTERMEDIATE: CrimeData_15_14.csv
CrimeData_15_14.csv : CrimeData_15_14.xlsx
	in2csv -f xls $< > $@

# create postgres table for suburban crime
ucr_crime : CrimeData_15_14.csv
	$(CHECK_RELATION) || ( \
	sed 's/--//g' $< | csvsql --db "postgresql:///$(PG_DB)" --table $@ --insert)

# -------------------------------------
# Build crosswalks for police agencies 
# -------------------------------------

# raw data published online at <https://www.icpsr.umich.edu/icpsrweb/NACJD/studies/35158>
identifiers_crosswalk.csv : raw/identifiers_crosswalk.tsv
	csvformat -t $< | python scripts/clean_identifiers.py > $@ 

identifiers_crosswalk : identifiers_crosswalk.csv
	$(CHECK_RELATION) || ( \
	csvsql --db "postgresql:///$(PG_DB)" --table $@ --insert $< && \
	psql -d $(PG_DB) -c "ALTER TABLE $@ ALTER COLUMN \"FPLACE\" TYPE TEXT" && \
	psql -d $(PG_DB) -c "UPDATE $@ SET \"FPLACE\" = LPAD(\"FPLACE\", 5, '0')")

# create postgres DB for the fixed crosswalk
illinois_crosswalk : joined_crosswalk.csv
	$(CHECK_RELATION) || ( \
	csvcut -c "NAME","COUNTYNAME","Agency","County" $< |\
        csvsql --db "postgresql:///$(PG_DB)" --table $@ --insert)