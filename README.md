This repository contains the programmed solutions made for [Advent of Code](https://adventofcode.com/about). Advent of Code is an Advent calendar of programming puzzles, offering 25 puzzles per year, one for each Advent-calendar day. 

The puzzles, accompanied by amusing Christmas stories, are divided into two parts, of which the second part is usually a more complex version of the first. The puzzles tend to grow in difficulty from day 1 to day 25.
<br/><br/>

The puzzles are solved taking input files found on the Advent of Code website. Each puzzle also provides examples, which can be useful to test the programmed solutions. The input files, both the example and the main puzzle files, are not published in this repository, as the creator of Advent of Code asks to not share them. They can easily be found on the Advent of Code website.
<br/><br/>

Currently, the solutions in this repository are for some of the puzzles from the Advent calendars of 2015, 2021, 2022 and 2023, programmed in C++, Rust, Python and Go, respectively. The programs look for files named *dayX.txt*, where *X* is the number of the puzzle. These files are either in a subfolder *puzzle_inputs*, or, for the case of Go, in the same folder as the programs. These files are read by default when executing the programs. All programs also can use other default example files (named *dayX_example.txt*) instead of the main defaults, by passing a single argument. If a second argument is given, it will be used as file path instead.

Some files contain comments explaining how the implemented solution works. Very straightforward puzzles answers often miss many comments. In most cases the comments do not explain the instructions of the puzzles, as they can be found on Advent of Code website.