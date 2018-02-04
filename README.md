# Jasons-Analysis-Project
Udacity Database Querying Project

## Contents

- [Installation](#installation)
	- [Install VirtualBox](#install-virtualbox)
	- [Install Vagrant](#install-vagrant)
	- [Download Project](#download-project)
- [Configuration](#configuration)
	- [Setup Virtual Machine](#setup-virtual-machine)
	- [Download newsdata.sql](#download-newsdata.sql)
	- [Prepare Newsdata Database](#prepare-newsdata-database)
- [Running Project](#running-project)
	- [Create Views](#create-views)
	- [Run jasons_analysis_project](#run-jasons_analysis_project)

## Installation

### Install Python3
[Download python3](https://www.python.org/downloads/)
This project requires Python3 or greater to run, download the version compatible with your operating system.

### Install VirtualBox 
[Download VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

### Install Vagrant
[Download Vagrant](https://www.vagrantup.com/downloads.html)
Be sure to download and install the appropriate version for your operating system. To confirm that Vagrant has been correctly installed, in your operating systems command prompt type `vagrant --version`, if the response is something akin to `Vagrant 1.8.5` you can proceed to the next step.

### Download Project
[Download Jasons-Analysis-Project](https://github.com/Minimalistic/Jasons-Analysis-Project)
Save the project to a local folder of your choice.

## Configuration

### Setup Virtual Machine
Using a terminal or command prompt, navigate to the project directory and type `vagrant up` to start preparing the vagrant environment.  It may take a few minutes depending on internet speed etc.  When the process has completed, run `vagrant ssh` and you will be logged in to your VM.

### Download newsdata.sql
[Download newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
Within the `.zip` file, you specifically need `newsdata.sql`.  `newsdata.sql` is the database that this project will query information from.  Download it and place it in the vagrant directory that's shared with your newly started VM, specifically place the file here `~/Jasons-Analysis-Project/FSND-Virtual-Machine/vagrant/newsdata.sql` in the same folder as `jasons_analysis_project.py`.

### Prepare Newsdata Database
Within your running Vagrant VM, run the command:
`psql -d news -f newsdata.sql;`

## Running Project

### Create Views
**Note** This project has been designed to automatically create or replace all views necessary, direct interaction with the `psql` interface should be unnecessary.  

Regardless, here are the following views that are created by the project upon start:

`top_slugs_view`
```sql
CREATE OR REPLACE VIEW top_slugs_view AS SELECT path,
	COUNT(*) AS num_views FROM log                       
	WHERE status = '200 OK'                              
	AND NOT path = '/'                                   
	GROUP BY path ORDER BY num_views DESC;
```

`alt_view`
```sql
CREATE OR REPLACE VIEW alt_view AS SELECT author, num_views
    FROM articles, top_slugs_view
    WHERE top_slugs_view.path = CONCAT('/article/', slug)
    ORDER BY num_views DESC;
```

`x_view`
```sql
CREATE OR REPLACE VIEW x_view AS SELECT author, sum(num_views)
    FROM alt_view
    GROUP BY author;
```

`errors_day_view`
```sql
CREATE OR REPLACE VIEW errors_day_view AS SELECT
	DATE(time), COUNT(*) AS num_views
	FROM log
	WHERE status = '404 NOT FOUND'
	GROUP BY status, DATE
	ORDER BY num_views DESC;
```

`hits_day_view`
```sql
CREATE OR REPLACE VIEW hits_day_view AS SELECT
	DATE(time), COUNT(*) AS num_views
	FROM log GROUP BY DATE(time);
```

### Run jasons_analysis_project
From within your running Vagrant VM, ensure you're in the `vagrant` folder that contains `jasons_analysis_project.py` and type the command `python3 jasons_analysis_project.py` and press `enter`.

You should now see something like:
```
-------------------------------------------------
Welcome to Jason's Python Database Query Machine!
-------------------------------------------------
1) Top 3 Articles
2) Top Authors
3) Days With Greatest Percent Request Errors
4) Exit

Select an option 1-4: 
```
Enter a number `1` through `3` to query information from the database or enter `4` to exit the project.