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

TODO
----
- Enforce types (integers, floats or bools) to be preserved instead of returning strings
