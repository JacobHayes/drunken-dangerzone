drunken-dangerzone
==================

Some old programs from when I was a CS Major

Game of Life
============

Module and implementation of the Game of Life.

User has the choice to play a Random grid or search Still Lifes. In both modes, the user provides the number of columns and rows as well as how many live cells to place. In Random mode, cells are randomly placed and Life goes on. In Still Life mode, all possible fields of the designated size/cell count are created and checked for a still life. For example on a 5x5 grid with 5 live cells, 53,130 combinations will be checked (5x5c5 -> 25c5), 36 of which will be still lifes.

Minesweeper
-----------

Simple Minesweeper module (Minesweeper.py) and accompaining implementation (Main.py). The module uses a bit of an abstraction on the typical row/column layout and instead uses cell count (left->right, top->bottom), which allows for a bit cleaner code (I think) and for the player, a quicker lookup that reads like poetry.

It's likely the module's method documentation is not all correct (instructor's vision vs my implementation).

Rock-Paper-Scissors
-------------------

A _slightly_ smart Rock-Paper-Scissors AI that uses previous player moves to determine what hand to play.

Sunspots
--------

A program that averages the daily sunspot data (can't exactly remember where the data is from) for each month (written to `MONTHS.txt`) and then smoothes that data with the preceeding and following six months (written to `SMOOTH.txt`).

Includes some sample data (`dailysunspots.txt`) which contains over 70,000 records as well a smaller sample (first 22 lines of `dailysunspots.txt`) for quicker results<sup>1</sup> (`fewsunspots.txt`).

Calculates the full `dailysunspots.txt` in less than a second on OS X and Ubuntu.

1. It runs VERY slowly when running on a friends Windows computer, thus `fewsunspots.txt`. IIRC (was a number of months ago), the speed issue was related to some issues with Python Disk I/O on Windows systems (which is hit pretty heavily in the data_strip_gen method). If it's an issue with my code (which seems to work fine on *nix systems), send me a Pull Request.
