drunken-dangerzone
==================

Some old programs from when I was a CS Major

rock_paper_scissors
-------------------

A _slightly_ smart Rock-Paper-Scissors AI that uses previous player moves to determine what hand to play.

Sunspots
--------

A program that averages the daily sunspot data (can't exactly remember where the data is from) for each month (written to `MONTHS.txt`) and then smoothes that data with the preceeding and following six months (written to `SMOOTH.txt`).

Includes some sample data (`dailysunspots.txt`) which contains over 70,000 records as well a smaller sample (first 22 lines of `dailysunspots.txt`) for quicker results<sup>1</sup> (`fewsunspots.txt`).

Calculates the full `dailysunspots.txt` in less than a second on OS X and Ubuntu.

1. It runs VERY slowly when running on a friends Windows computer, thus `fewsunspots.txt`. IIRC (was a number of months ago), the speed issue was related to some issues with Python Disk I/O on Windows systems (which is hit pretty heavily in the data_strip_gen method). If it's an issue with my code (which seems to work fine on *nix systems), send me a Pull Request.
