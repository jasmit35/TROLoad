# TRO Load User's Guide

This application is currently designed to pick up any spreadsheets (files with a \*.xslx extension) from the stage directory. It will pickup and process multiple files. The files are renamed with a .bkp extension after processing. (The stage directory can be overridden by setting a parameter in the configuration file.)

## Monthly processing

You probably want to process more than the previous months data. It depends on if you have modified any transactions from prior months. For documentation purposes, we will process the proceding six months.

### On the database server - Backup the starting point

Before starting a new month, run a full export of the data as it currently stands. Use the instructions in the "exports" section of the "Postgres User's Guide".

### On Ninkasi - export the new data

Run Quicken and select the following options:

- Reports
- My saved reports and graphs
- The real oracle
- Transactions
- Select the icon to customize the report.
- Modify the dates to include the previous six months.
- Generate the report.
- Click the icon and chose to export to excel workbook.
- Save the spreadsheet to the shared space on Synology.

### On the application server - load the data

Verify the spreadsheet is in the correct directory with the xlsx extension:

`ll '/Volumes/SharedSpace/<environment>/TROStage'`

Use the makefile to run the application:

```
make dr-run
```

Review the log files from the load. If their are problems that can be corrected via Quicken, do so and start over at 'Monthly Processing'.

Add the previously found missing transactions:

```
cd ../sql
vi add_missing.sql
psql -h kmaster -p 5432 -d prod -U postgres
\i add_missing.sql
\q
```

### Check balances

Use the "Monthly Processing" instructions for the TROReports application to check the accuracy of the data for the month. If changes were made to the add_missing.sql script, repeat the load of the data.

The report should end with a 'Fineshed successfully' message.

jasmit
Go back to Quicken and select the following options:

- Reports
- My saved reports and graphs
- The real oracle
- Ending account balances
- Select the icon to customize the report.
- Modify the end date.
- Generate and print the report.
