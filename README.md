cliutils
========

CLIUtils is a collection of command line utilities that make my life easier

csv2json
========

Converts CSV formatted lines, into JSON formatted lines. It takes JSON attribute names 
from the first row found in the CSV file, so a file formatted as follows :

    date,name,last_name,age,visits,hits
    12/1/2012,Peter,Parker,24,4,300
    12/1/2012,Clark,Kent,34,2,900

Would produce :
```json
    { 
      "date" : "12/1/2012", 
      "name" : "Peter", 
      "last_name" : "Parker",
      "age" : "24",
      "visits" : "4",
      "hits" : "300"
    }
    { 
      "date" : "12/1/2012", 
      "name" : "Clark", 
      "last_name" : "Kent",
      "age" : "34",
      "visits" : "2",
      "hits" : "900"
    }
```

By calling the following command line : 
```cli
  csv2json.py path/to/file.csv
```

Optional parameters allow to inject static attributes to every row, or group some of the fields
into objects: 
```cli
  csv2json.py -o site=visits,hits path/to/file.csv
```

```json

    { 
      "date" : "12/1/2012", 
      "name" : "Peter", 
      "last_name" : "Parker",
      "age" : "24",
      "site" : {
        "visits" : "4",
        "hits" : "300"
      }
    }
    { 
      "date" : "12/1/2012", 
      "name" : "Clark", 
      "last_name" : "Kent",
      "age" : "34",
      "site" : {
        "visits" : "2",
        "hits" : "900"
      }
    }
```
Similarly, switching -o argument for -l would group the parameters into an array instead of an object :
```cli
  csv2json.py -l site=visits,hits path/to/file.csv
```
```json

    { 
      "date" : "12/1/2012", 
      "name" : "Peter", 
      "last_name" : "Parker",
      "age" : "24",
      "site" : [ "4", "300" ]
    }
    { 
      "date" : "12/1/2012", 
      "name" : "Clark", 
      "last_name" : "Kent",
      "age" : "34",
      "site" : [ "2", "900"]
    }
```

randfile
========

randfile is a simple random file with random creating / modifying script. It is useful for workshops
that illustrate version control workflows.

By calling the following command line : 
```cli
  randfile.py create -n 3
```

The script will produce 3 random files with random content in the current directory.

In the other hand the line :
```cli
  randfile.py modify -n 3
```

will randomly modify 3 files in the current directory. The content inside of the files is
modified per line, and every line has a 50% chance of being modified.

Here is a sample of the produced files and data : 

```txt
--> ashnt.php
5POkWe gQJX1R
uljQjH 5FhznX KDqJML
UxFw9O
8NYBD3
YJfZi4
gSIEHu

--> bxjny.php
gYXs5M sW5wlO 6VsHF1 GEY6jq
OVGRbC 9AyZYz
Ngks3F
7X5aco SEecce XOb3HI WqBxsN
CWvidf ib77XY

--> opjeb.php
pLg4iI
7j1Pdm nCZOUW f21fLY
mZbkLf pOurrg
5P47k5
0ObJMR nu8yTH aLcHRY
rC5zYz Ykm7l5 wsHDCR 91Ppjl
kwhiwB rIgCZD ETQiEM CM3mnQ ZpHMJu
g23gXl

```

