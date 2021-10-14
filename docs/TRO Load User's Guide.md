# TRO Load User's Guide

This application is currently designed to pick up any spreadsheets (files with a *.xslx extension) from the stage directory. It will pickup and process multiple files. The files are renamed with a .bkp extension after processing.

## Monthly processing
You probably want to process more than the previous months data. It depends on if you have recatorized any transactions from prior months. For documentation purposes, we will process the proceding six months.

### On Ganeymede

Run Quicken and select the following options:

* Reports
* TRO reports
* Transactions

Modify the dates to inclusde the previous six months.
Generate the report.

Click the icon and chose to exprt to excel workbook.

Save the spreadsheet to my home directory on Woz.

### On bbnode01

Change to the stage directoy for troload:

`cd ~/prod/troload/local/stage`

Copy over the spreadsheet:

`scp woz.local:~/*.xlsx .`

Change back to the main troload directory and use the Makefile to run the load:

`cd ~/prod/troload`

`make rm`

`make run`

`make logs`

Check the reports:

`cd prod/troload/local/rpt`

`ls -lta`

`view TROLoad_2021_08_09_23_26.rpt`

The report should end with a 'Fineshed successfully' message.






