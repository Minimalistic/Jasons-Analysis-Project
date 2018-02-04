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
	- [Run jasons_analysis_project](#run-jasons_analysis_project)

## Installation

### Install Python3
This project requires Python3 or greater to run, download the version compatible with your operating system from [python.org](https://www.python.org/downloads/).

### Install VirtualBox 
The first step of running this project is to download and install VirtualBox download it from [virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).  

### Install Vagrant
Download Vagrant from [vagrantup.com](https://www.vagrantup.com/downloads.html), be sure to install the appropriate version for your operating system. To ensure Vagrant has been correctly installed, in your operating systems command prompt type `vagrant --version`, if the response is something akin to `Vagrant 1.8.5` you can proceed to the next step.

### Download Project
Go to [GitHub and download or clone the project repository](https://github.com/Minimalistic/Jasons-Analysis-Project) to a local folder of your choice.

## Configuration

### Setup Virtual Machine
Using a terminal or command prompt, navigate to the project directory and type `vagrant up` to start preparing the vagrant environment.  It may take a few minutes depending on internet speed etc.  When the process has completed, run `vagrant ssh` and you will be logged in to your VM.

### Download newsdata.sql
newsdata.sql is the sql database that this project will query information from.  Download newsdata.sql and place it in the vagrant directory that's shared with your newly started VM, specifically place the folder here `~/Jasons-Analysis-Project/FSND-Virtual-Machine/vagrant/newsdata.sql` in the same folder as `jasons_analysis_project.py`.

### Prepare Newsdata Database
Within your running Vagrant VM, run the command `psql -d news -f newsdata.sql;`

## Running Project

### Create Views
**Note** This project has been designed to automatically create or replace all views necessary, direct interaction with the `psql` interface should be unnecessary.  

Regardless, here are the following views that are created by the project upon start:

`top_slugs_view`
```
CREATE OR REPLACE VIEW top_slugs_view AS SELECT path, 
	COUNT(*) AS num_views FROM log                       
	WHERE status = '200 OK'                              
	AND NOT path = '/'                                   
	GROUP BY path ORDER BY num_views DESC;
```

`alt_view`
```
CREATE OR REPLACE VIEW alt_view AS SELECT author, num_views
    FROM articles, top_slugs_view
    WHERE top_slugs_view.path = CONCAT('/article/', slug)
    ORDER BY num_views DESC;
```

`x_view`
```
CREATE OR REPLACE VIEW x_view AS SELECT author, sum(num_views)
    FROM alt_view
    GROUP BY author;
```

`errors_day_view`
```
CREATE OR REPLACE VIEW errors_day_view AS SELECT
	DATE(time), COUNT(*) AS num_views
	FROM log
	WHERE status = '404 NOT FOUND'
	GROUP BY status, DATE
	ORDER BY num_views DESC;
```

`hits_day_view`
```
CREATE OR REPLACE VIEW hits_day_view AS SELECT
	DATE(time), COUNT(*) AS num_views
	FROM log GROUP BY DATE(time);
```

### Run jasons_analysis_project.py
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
Enter a number 1 through 3 to query information from the database or enter 4 to exit the project.