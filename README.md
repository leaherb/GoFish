# GoFish

## Purpose

Gapminder.org offers a large number 'global facts' datasets, available for download (https://www.gapminder.org/data/). Most of these datasets include feature calculations for each country for a range of years. For example: the population of each country starting in 1800 and forecasted through to 2100.  

As a Data Analyst looking for correlations between any number of datasets in order to narrow my 'global facts' data exploration scope, and perhaps discover questions I had not yet considered, I was looking for a way to simply pile a bunch of CSV files together then programmatically create a Pearson correlation coefficients report on all feature pairs.

GoFish is a Python program that creates a report of Pearson correlation coefficients on each feature pairing found in available Gapminder.org CSV downloads.

## Possible Future Enhancements

## Caveats
* Only CSV files are loaded as target datasets
* GoFish attempts to load all CSV files in a given directory
* The 'given directory' is hardcoded as **Data**
* Some hardcoding is present that makes this utility workable only with the **Example Dataset Source** files (below) 
* All CSV file datasets are assumed to have the following structure:
 * Column 1: country (regardless of column header)
 * Column 2-n: 4-digit year
* Exception and error handling is not yet included

## Example Dataset Source
Downloads from <a href target="_blank" source="https://www.gapminder.org/data/">Gapminder</a>

> Note: Gapminder data is sometimes based on very rough estimates or extrapolations. All data, statistics and visuals presented here should be considered generalizations only. 

#### Population
* Description: Total population
* Download: population_total.csv 

#### Income
* Description: Gross domestic product per person adjusted for differences in purchasing power (in international dollars, fixed 2011 prices, PPP based on 2011 ICP).
* Download: income_per_person_gdppercapita_ppp_inflation_adjusted.csv

#### Life expectancy (years)
* Description: The average number of years a newborn child would live if current mortality patterns were to stay the same.
* Download: life_expectancy_years.csv

#### Water, overall access (%)
* Description: The percentage of people using at least asic water services. This indicator encompasses both people using basic water services as well as those using safely managed water services. Basic drinking water services is defined as drinking water from an improved source, provided collection time is not more than 30 minutes for a round trip. Improved water sources include piped water, borholes or tubewells, protected dug wells, protected springs, and packaged or delivered water.
* Download: at_least_basic_water_source_overall_access_percent.csv
