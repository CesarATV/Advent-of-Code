All Python and Jupyter Notebook files in this folder were executed with:

* Python version 3.8.10
* argparse version 1.1
* NumPy version 1.23.3 
* Matplotlib version 3.5.2
<br/><br/>

As mentioned in the README of the parent folder, the Python programs assume that there is a subfolder *puzzle_inputs* with files named *dayX.txt*, where *X* is the number of the puzzle. These files are read by default when executing the programs. All programs also can use other default example files (named *dayX_example.txt*) instead of the main defaults, by passing a single argument. If a second argument is given, this will be used as file path instead. 

Additionally, day15.py accepts an additional argument, *-e*, to specify that the given file path is an example file, as this day in particular changes some of the constant variables if the file is an example file.
<br /><br />

*data_visualizations.ipynb* shows some simple plots made from data from Day 17 and Day 18.

Besides the second part of Day 16, Day 18 and Day 23, all programs should give a solution (compute) in less than a minute on non-example files. The second part of day 16 very likely produces the solution in less than a minute, but the program takes longer to finish as it also checks very unlikely possibilities. The second part of Day 18 takes around two and a half minutes to compute. The execution time of these programs can be improved.

Some programs could receive some additional comments or better variable names.