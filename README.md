# Python Server Log Plotting

This Python tool pulls user activity statistics from a MySQL database and plots it via Matplotlib.

## TL;DR:
* Install [**Miniconda** for **Windows 64-bit** with **Python 3.7.X**](https://conda.io/en/latest/miniconda.html)
* Create `servermonitor` MySQL table using the script snippet further below and fill the table with data
* Clone repository: `git clone https://github.com/Jynsaillar/python_server_log_plotting.git`
* cd into repository: `cd python_server_log_plotting`
* Create conda venv: `C:\Users\MyUser\Anaconda3\Scripts\conda env create -f environment.yml`
* Activate conda venv: `C:\Users\MyUser\Anaconda3\Scripts\conda env activate python_server_log_plotting`
* Create `cfg.json`: *See bottom of the page for sample cfg.json*
* Run program using `cfg.json`: `python main_plot.py -uc 1`

## Sample images

![Least users](
        https://github.com/Jynsaillar/python_server_log_plotting/blob/master/rz-least-per-hour-2019-01-30-to-2019-02-09.png
        "Least users online per hour"
      )
![Average users](
        https://github.com/Jynsaillar/python_server_log_plotting/blob/master/rz-avg-per-hour-2019-01-30-to-2019-02-09.png
        "Average users online per hour"
      )
![Most users](
        https://github.com/Jynsaillar/python_server_log_plotting/blob/master/rz-most-per-hour-2019-01-30-to-2019-02-09.png
        "Most users online per hour"
      )
      
## Getting Started

### On Windows:

* Download the [64-bit version of Anaconda containing Python 3.7.X](https://www.anaconda.com/distribution/) if you want  
the *full package of Anaconda* with the `Anaconda Navigator` GUI.
* Install Anaconda.

**OR**
* Download the [64-bit version of Miniconda containing Python 3.7.X](https://conda.io/en/latest/miniconda.html) if you only want to  
*install the minimal dependencies* centered around the command line tool `conda` (*suggested*).
* Install Miniconda.  
  
  
Next, clone the repository from the command line, for example in `C:\anaconda\`:  
* `cd C:\anaconda`  
* `git clone https://github.com/Jynsaillar/python_server_log_plotting.git`  

The folder structure should now look like `C:\anaconda\python_server_log_plotting`.  
Change your current directory to the repository folder with  
* `cd C:\anaconda\python_server_log_plotting`

In that folder, create a file called `cfg.json` to make it easier to launch the program with customizable parameters.  
A sample `cfg.json` can be found at the end of this page.  

#### With Anaconda Navigator:
* Open Anaconda Navigator
* On the left panel, switch from *Home* to *Environments*.
* In the center panel, click on *Import*.
* In the popup, enter a name for your new virtual environment and click on the folder icon to import the *environment.yml* contained in this repository.
* Wait until Anaconda has finished importing, then select your new virtual environment from the center panel.
* Now switch back to the *Home* tab in the left panel and open the editor of choice (for example, VS Code).
* Using the example of VS Code, open a terminal if it isn't open (*Terminal*->*New Terminal* from the top menu bar).
* Run the program with `python main_plot.py <parameters>`.
* To run the program by using the `cfg.json`,  
run `python main_plot.py --useconfig 1` or `python main_plot.py -uc 1`.  
* Otherwise, to use cmd parameters, take a look at the table further below and use, for example:  
`python main_plot.py --nightmode 1`  

#### With conda:
Assuming you are in `C:\anaconda\python_server_log_plotting` and your conda install directory is `C:\Users\MyUser\Anaconda3`:
* Open cmd and run `C:\Users\MyUser\Anaconda3\Scripts\conda env create -f environment.yml` to create the virtual environment.
Wait until that is finished, then verify that the new virtual environment was successfully created with `C:\Users\MyUser\Anaconda3\Scripts\conda list`.
* Activate the virtual environment with `C:\Users\MyUser\Anaconda3\Scripts\conda activate python_server_log_plotting`.
Your cmd path should now be prefixed with `python_server_log_plotting` to indicate that your current virtual environment was changed.
* Finally, run the program with parameters, for example: `python main_plot.py --useconfig 1`

### On Linux:
**[Will be updated once I've tested the Linux setup.]**  
The steps for UNIX-based OS' should be similar to the Windows setup, have a look at how the  
`conda` virtual environment setup differs from the Windows setup.  
Everything else should work just the same.  

## Prerequisites

* **Anaconda** or **Miniconda** with **Python 3.7.X** (64-bit)
* **MySQL** database
* **MySQL table** called `servermonitor`

## MySQL table creation

If the `servermonitor` table does not exist yet, use the following SQL to create it:
```sql
DROP TABLE IF EXISTS `ServerMonitor`;
CREATE TABLE `ServerMonitor` (
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `scrape_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp(),
  `user_count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Customization

### Valid input for JSON & command line argument types

Type         |Input
-------------|-----
`String`     |`'hello'`, `world`
`DateString` |`'1970-01-01 00:00'`
`GraphString`|`min`, `minimum`, `least`, `avg`, `average`, `max`, `maximum`, `most`
`Int`        |`<Any integer>`
`Bool`       |`0`, `1`, `n`, `y`, `no`, `yes`, `true`, `false`

### Via command line arguments
Argument          |Short  |Type         |Default           |Purpose
------------------|-------|:-------------:|:------------------:|-------
`--useconfig`     | `-uc` |`Bool`       |`False`           |Indicates whether to use cfg.json to load custom settings instead of command line args.
`--verbose`       | `-v`  |`Bool`       |`False`           |If set, the MySQL queries and their results will be printed to the console.
`--nightmode`     | `-nm` |`Bool`       |`False`           |Toggles the dark interface with bright graph colors.
`--intervalusers` | `-iu` |`Int`        |`20`              |Sets the tick spacing on the Y-axis by user count.
`--intervalhours` | `-ih` |`Int`        |`4`               |Sets the tick spacing on the X-axis by hours.
`--dbuser`        | `-dbu`|`String`     |`sa`              |Sets the database user for the MySQL connection.
`--dbpassword`    | `-dbp`|`String`     |`''`              |Sets the database user password for the MySQL connection.
`--dbhost`        | `-dbh`|`String`     |`127.0.0.1`       |Sets the database host address for the MySQL connection.
`--dbname`        | `-dbn`|`String`     |`log`             |Sets the target database for the MySQL connection.
`--datestringfrom`| `-dsf`|`DateString` |`1970-01-01 00:00`|Sets the start date from which the database data will be plotted.
`--datestringto`  | `-dst`|`DateString` |`1970-01-01 23:59`|Sets the end date until which the database data will be plotted.
`--graph`         | `-g`  |`GraphString`|`avg`             |Sets the user count criteria by which to display the graph, least users per hour, average users per hour or most users per hour are selectable.

### Via JSON config file (suggested method)

Excluding the `--useconfig` switch for obvious reasons, all of the command line parameters are valid JSON variables as well.
By passing `--useconfig 1` or `-uc 1` as parameter to `main_plot.py`, the program will try to load `cfg.json`.  
**The cfg.json file has to be created manually!**  
Only full argument names are valid entries for the `cfg.json`, so
```json
{
  "nightmode": true
}
```
will work, while
```json
{
  "nm": true
}
```
will not.

### cfg.json example file
```json
{
  "verbose": true,
  "nightmode": true,
  "intervalusers": 50,
  "intervalhours": 4,
  "dbuser": "sa",
  "dbpassword": "password",
  "dbhost": "127.0.0.1",
  "dbname": "log",
  "datestringfrom":"2019-01-30 00:00",
  "datestringto":"2019-02-09 21:00",
  "graph": "least"
}
```
