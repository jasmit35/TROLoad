# TRO Load User's Guide

This application is currently designed to pick up any spreadsheets (files with a *.xslx extension) from the stage directory. It will pickup and process multiple files. The files are renamed with a .bkp extension after processing. (The stage directory can be overridden by setting a parameter in the configuration file.)

## Monthly processing
You probably want to process more than the previous months data. It depends on if you have modified any transactions from prior months. For documentation purposes, we will process the proceding three months.

### On Ganeymede

Run Quicken and select the following options:

* Reports
* My saved reports and graphs
* The real oracle
* Transactions
* Select the icon to customize the report.
* Modify the dates to inclusde the previous three months.
* Generate the report.
* Click the icon and chose to export to excel workbook.
* Save the spreadsheet to the shared space on Synology.

Go back to Quicken and select the following options:

* Reports
* My saved reports and graphs
* The real oracle
* Ending account balances
* Select the icon to customize the report.
* Modify the end date.
* Generate and print the report.

### On enki

Verify the spreadsheet is in the correct directory with the xlsx extension:

`ls '/Volumes/Shared space/TROStage'`

Modify the crontab to run troload in the test environment:

`crontab -e`

~~~text
#
#  TRO Load
53 TROLOAD_TEST=/Users/jeff/test/troload
54 20 16 10 03 * $RUNPY_TEST $TROLOAD_TEST/src/troload.py -e test >$TROLOAD_TEST/local/log/troload.out 2>&1
~~~

## Appendix A: Setup for initial load
Their are initial values that need to be loaded before the first data from Quicken. Execute the following to do so:

### For the Devl environment:

```
cd /Users/jeff/devl/TROLoad/local/sql
psql -h localhost -p 5430 -d devl -U postgres
```

### For the Test environment:

```
cd /Users/jeff/test/TROLoad/local/sql
psql -h localhost -p 5432 -d test -U postgres
```

### For the Prod environment:

```
cd /Users/jeff/prod/TROLoad/local/sql
psql -h kmaster -p 5432 -d prod -U postgres
```

### For all environments:

```
\i grant_permsissions.sql
\i set_start.sql
\i set_beginning_balances.sql
\q
```
The report should end with a 'Fineshed successfully' message.






