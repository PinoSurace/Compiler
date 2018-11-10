#!bin/sh



# This script can be used to automatically execute .popl files with main.py,

# output the results to .output files and then compare them with .expected files.

# In the output all different lines are shown, along with their line numbers.

# You may need to install ply globally to run the script (pip install ply).

# On Windows script can be run with "sh test.sh"



# Made by Sami Aalto. Use at your own risk.



# Directory of main.py relative to root

assignment_directory="02_syntax"



# Path relative to assignment_directory

# Default value assumes that public-examples is cloned to repository root

# Directory should contain .popl files and their expected output in .expected files

# (https://course-gitlab.tut.fi/tie-20306_2018-2019/public-examples/commits/master)

examples_directory="02_yacc"



# Move to main.py directory

cd $assignment_directory

IFS=



for filename in "$examples_directory"/*.popl

do

  # Note: for phase 1 change $base.expected -> $base.expected_output

  # For phase 1 may not work well with some foreign characters

  base=$(basename $filename .popl)

  expectedPath="$examples_directory/$base.expected"

  outputPath="$examples_directory/$base.output"

  echo "************************************"

  echo "$base (expected/output)"



  # Empty the file

  > $outputPath

  # Writes python prints to .output file

  echo $(python -u main.py -f $filename) >> $outputPath



  # Show different lines on console

  sdiff -l --strip-trailing-cr $expectedPath $outputPath | cat -n  | grep -v -e '($'

done