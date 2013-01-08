#!/usr/bin/env python -u
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Maciek Ruckgaber <maciekrb@gmail.com>
#

import argparse
import csv
import sys
from json import dumps as json_encode

class InvalidKeyValueFormat(Exception):
  pass

class KeyExistsInDictionary(Exception):
  pass

def parse_key_value_args(inserts):
  """ 
  Parses arguments that are formated in a key=value fashion 
  
  Args:
    - inserts: (list) list of key=value arguments

  Returns:
    - dict containing key : value pairs for given arguments

  Raises:
    - InvalidKeyValueFormat: when any of the arguments is not formated as key=value
  """
  if not inserts:
    return {}

  pinserts = {}
  for i in inserts:
    try:
      i.index('=')
      key,val = i.split('=')
      pinserts[key] = val
    except IndexError:
      raise InvalidKeyValueFormat(i)

  return pinserts

def add_to_dict(target,items,overwrite=False):
  """
  Adds the elements in the items dicto into the target dict following overwrite rule

  Args:
    - target: (dict) dictionary to which items will be added
    - items: (dict) dictionary with items to add to target
    - overwrite: (bool) if True, items can overwrite target keys, false by default

  Returns:
    - dict with items added/merged into target

  Raises:
    - KeyExistsInDictionary: when trying to overwrite an existing target key without
    the overwrite param set to True
  """
  for i,v in items.iteritems():
    if i in target and not overwrite:
      raise InvalidKeyValueFormat(i)

    target[i] = v
  return target

def to_type(val):
  """
  Attempts to convert val to a native type
  Returns:
    - val converted to given type if possible
  """
  try:
    val = int(val)
  except ValueError:
    try:
      val = float(val)
    except ValueError:
      bl = val.lower()
      if bl == 'true' or bl == 'false':
        val = bool(val)
  finally:
    return val

def group(row,objects,as_list=False):
  """
  Groups elements of row dictionary in groups specified by objects dict

  Args:
    - row: (dict) dict containing row data (key : value)
    - objects: (dict) dict containing grouped properties in the following
      format ::

        { "data" : ["name","last_name","age"] ... }

    - as_list: (bool) defines if group will be resolved as an object or list

  Returns: 
    - dict containg grouped properties as specified by objects dict
  """
  nrow = {}
  for rowkey,rowval in row.iteritems():
    if not objects:
      nrow[rowkey] = to_type(rowval)
    else:
      for obkey,obfields in objects.iteritems():
        if rowkey in obfields:
          if obkey not in nrow:
            nrow[obkey] = {} if not as_list else []

          if not as_list:
            nrow[obkey][rowkey] = to_type(rowval)
          else :
            nrow[obkey].append(to_type(rowval))

        else:
          nrow[rowkey] = to_type(rowval)

  return nrow

def parse_data(csvdata,delimiter,inserts={},overwrite=False,objects=None,lists=None):
  inserts = parse_key_value_args(inserts)
  objects = { k : v.split(',') for k,v in parse_key_value_args(objects).iteritems() }
  lists = { k : v.split(',') for k,v in parse_key_value_args(lists).iteritems() }
  csvreader = csv.DictReader(csvdata,delimiter=delimiter,quotechar='"')
  for row in csvreader:
    if inserts:
      row = add_to_dict(row,inserts,overwrite)
    if objects:
      row = group(row,objects)
    if lists:
      row = group(row,lists,as_list=True)
    
    print json_encode(row)

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description=""" 
    Converts CSV file into JSON by using first row in the file as attribute names.
    Additional arguments allow to insert or group columns into objects.
    """)
  parser.add_argument("file", nargs='?', type=argparse.FileType('r'), default = '-', 
                      help="File containing CSV data to be transformed into JSON")
  parser.add_argument("-d","--delim", default=",", help="Field delimiter char (default: ','")
  parser.add_argument("-i", metavar="field=value", action="append",
                      help="Insert a parameter with its value in every row, ex. -i field=value")
  parser.add_argument("-o", metavar="data=2,3,4", action="append",
                      help="Creates an object out of the given fields, ex. -o data=name,last_name,age")
  parser.add_argument("-l", metavar="data=2,3,4", action="append",
                      help="Same as -o but groups as an array instead of obj, ex. -l data=name,last_name,age")
  parser.add_argument("-x","--overwrite", action="store_true",
                      help="When specified -i options will overwrite existing keys when overlapping")
  parser.add_argument("-t","--types",help="Specify column data types as a colon separated list i.e int,bool,str")

  args = parser.parse_args()

  try:
    parse_data(
      args.file,
      delimiter=args.delim,
      inserts=args.i,
      overwrite=args.overwrite,
      objects=args.o,
      lists=args.l 
    )
  except InvalidKeyValueFormat,e:
    print "%s insert has to be formatted key=value" % e.message
    sys.exit(1)
  except KeyExistsInDictionary,e:
    print "-i %s overwrites existing attribute, add -x if you want that to happen" % e.message
    sys.exit(1)
  

