# GoFish
> This project is a work in progress

## Purpose

The purpose of this project is to search Gapminder.org datasets for features of interest using simple filters:

1. feature pairs with a moderate to strong Pearson's correlation coefficient
2. additional filters TBD

## Overview

Gapminder.org offers a large number 'global facts' datasets, available for download (https://www.gapminder.org/data/). Most of these datasets include feature calculations for each country for a range of years. For example: the population of each country starting in 1800 and forecasted through to 2100.  

As a Data Analyst looking for correlations between any number of datasets in order to narrow my 'global facts' data exploration scope, and perhaps discover questions I had not yet considered, I was looking for a way to simply pile a bunch of CSV files together then programmatically create a Pearson correlation coefficients report on all feature pairs.

## How to Contribute

Feel free to submit issues and enhancement requests.

Please use the Udacity Git Commit Message Style Guide (https://udacity.github.io/git-styleguide/), and follow the "fork-and-pull" Git workflow:

1. Fork the repo on GitHub
1. Clone the project to your own computer
1. Commit changes to your own branch
1. Push your work back up to your fork
1. Submit a Pull request so that I can review your changes

Note: Please take care to merge the latest from "upstream" before making a pull request.

### Enhancement Ideas
GoFish is in it's first Phase of development. As it stands, it searches CSV files already existing in a local directory. Future Phases could include:

* general code improvement (improve performance, refactor, document, etc.)
* do not limit feature exploration to Gapminder.org data
* more feature filters
* data cleaning/trimming options with a data storage feature
* a user interface front-end


## GoFish Caveats
* Only CSV files are loaded
* all CSV files in a given directory are loaded
* The 'given directory' is hardcoded as **Data**
* All CSV file datasets are assumed to have the following structure:
 * Column 1: country (regardless of column header)
 * Column 2-n: 4-digit year
* Exception and error handling is not mature

## Gapminder Data Location
Downloads from <a href target="_blank" source="https://www.gapminder.org/data/">Gapminder</a>

> Note: Gapminder data is sometimes based on very rough estimates or extrapolations. All data, statistics and visuals presented here should be considered generalizations only. 
