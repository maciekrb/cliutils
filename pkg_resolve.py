#!/usr/bin/env python
"""
USAGE:
  pkg_resolve /path/to_resolve_file /path/to_diff_file

This program takes the input taken from a diff file, and resolves the package 
descriptions based on a resolve pkg diff files into a format that is pasteable
into a report (tab separated text is often good enough).

The main objective is to automate boring report generation for projects where package 
or key like terms need to be resolved to something else (read explanation or extra something)
"""

import sys

def parse_diff_line(line):
  """
  Parses a diff line and returns a tuple with (new, old) package version
  """
  line = line.rstrip()
  try:
    line.index("|") # older version exists
    parts = [ s.strip() for s in line.split("|") ]
  except ValueError:
    try: 
      cidx = line.index("<") # No older version
      e = line[0:cidx].rstrip()
      parts = [e,None]
    except ValueError:
      try: 
        cidx = line.index(">") # No new version
        e = line[cidx+2:].lstrip()
        parts = [None,e]
      except ValueError:
        return None
  return parts

def dictify(fname,sep):
  """
  maps the given file to a dictionary, by using the part before the separator
  as the dictionary key and the rest as the value
  """
  file_map = {}
  for line in fname:
    line = line.strip()
    if line: 
      line.index(sep) # confirm separator exists or throw a ValueError
      key, val = line.split(sep)
      file_map[key.strip()] = val.strip()

  return file_map

def resolve_description(pkg_name, pkg_map):
  vpart = pkg_name.rindex("-") # last dash should precede version part
  name = pkg_name[0:vpart] 
  return pkg_map.get(name,"**UNRESOLVED**") 

def generate_report(infile,pkg_map):
  for line in infile:
    parts = parse_diff_line(line)
    if parts == None:
      print "I dont known what should I do with this line : %s" % line
      sys.exit(1)

    try:
      pkg_desc = resolve_description(parts[0],pkg_map)
    except AttributeError:
      pkg_desc = resolve_description(parts[1],pkg_map)
    finally:
      print "%s\t%s\t%s" % (parts[1] if parts[1] else "--", parts[0] if parts[0] else "--", pkg_desc)

if __name__ == '__main__':
  if not len(sys.argv) > 1:
    print __doc__
    sys.exit(1)
  map_fname = sys.argv[1]
  pkg_fname = sys.argv[2]

  try:
    mapfile = open(map_fname,'r')
  except IOError:
    print "You must specify a valid map file to use as package reference"
    print __doc__
    sys.exit(1)

  try:
    infile = open(pkg_fname,'r')
  except IOError:
    print "You must specify a valid package diff file to parse"
    print __doc__
    sys.exit(1)

  try:
    #@TODO: make proper CLI args for this
    sep = ";"
    pkg_map = dictify(mapfile,sep)
    mapfile.close()
  except ValueError:
    print "Not all lines in the map file are separated by %s" % sep
    sys.exit(1)
  
  report = generate_report(infile,pkg_map)
  print report
  infile.close()

