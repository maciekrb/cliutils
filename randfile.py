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

from __future__ import print_function
import argparse
import string
import random
from os import listdir
from os.path import isfile, join

def randomString(size=32, chars="uppercase,lowercase,digits"):
  """
  Creates a random string of specified size and type

  Args:
    size: (int) Desired length of generated string
    chars : (str) Desired types to use separated by "," : (uppercase, lowercase, digits)

  Returns: 
    Random generated string
  """
  opt = chars.split(",")
  use_chars = ""
  if 'uppercase' in opt:
    use_chars = use_chars + string.ascii_uppercase
  if 'lowercase' in opt:
    use_chars = use_chars + string.ascii_lowercase
  if 'digits' in opt:
    use_chars = use_chars + string.digits
  
  return ''.join(random.choice(use_chars) for x in range(size))

def mkfilename(ext="php"):
  return "%s.%s" % (randomString(size=5,chars='lowercase'),ext)

def create_file(ext):
  with open(mkfilename(ext=ext),'w') as fl:
   max_lines = random.randint(1,10)
   for i in range(0,max_lines):
     chunks = random.randint(1,5)
     print(" ".join([ randomString(size=6) for j in range(0,chunks) ]), file=fl)

def modify_file(fname):
  with open(fname,'r+') as fl:
    lns = fl.readlines()
    nlns = []
    for ln in lns:
      nlns.append(randomString(size=6)) if random.randint(0,1) else ln
    fl.seek(0)
    print(" ".join(nlns), file=fl)




if __name__ == "__main__":

  parser = argparse.ArgumentParser(description=""" 
   Creates / modifies files with random strings, useful for giving crash courses on
   Git or other version control systems.
    """)

  parser.add_argument("action", type=str, choices=['create','modify'], 
                      help=""" Action to perform. The \"create\" arg would create -n number of files in the
                      current directory. The \"modify\" action will randomly modify -n files in the current
                      dir. """)
  parser.add_argument("-n","--number",type=int, default=1, help="Number of files to randomly create / modify")
  parser.add_argument("-x","--extension",type=str, default="php",help="Extension for created files")

  args = parser.parse_args()

  if args.action == 'create':
    for i in range(0,args.number):
      create_file(args.extension)

  elif args.action == 'modify':
    files = [ f for f in listdir(".") if isfile(join(".",f)) ] 
    random.shuffle(files)
    for i in range(0,args.number):
      modify_file(files[i])
    

