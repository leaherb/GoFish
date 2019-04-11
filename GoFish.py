# coding: utf-8

# Filename:  GoFish.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from os import listdir
from itertools import combinations


# ## Data Wrangling
# 1. Gather CSV files
# 2. Load CSV file data into dataframes.
# 3. Compile the dataframes into a dictionary. 
# 4. Inspect the data.

# Data Wrangling Functions 

def find_csv_files (path_to_dir):
    """Return: List of filenames with suffix in path_to_dir."""
    return [filename for filename in listdir(path_to_dir) if filename.endswith( suffix )] 


def csv_dir_to_df_dict(path_to_dir):
    """Return dictionary of dataframes loaded with csv files in path_to_dir."""
    result_dict = {}
    
    for filename in find_csv_files(path_to_dir):
        # Include path with filename 
        fullname = ("{}/{}").format(path_to_dir, filename)
        
        # dataframe name = filename, trimmed of suffix.
        dfname = filename.rsplit(suffix)[0]
        
        result_dict[dfname] = pd.read_csv(fullname)
        
    return result_dict


def print_df_preview(dfname, df):
    """Print the first & last several rows & columns of a dataframe."""
    print('\n{}\n{} {} :\n\n{}' \
          .format("="*50, dfname, \
                df.shape, \
                df[list(df.columns[0:3]) + list(df.columns[-3:])].iloc[[0,1,-2,-1]] \
               )) 
    
    
def print_dfdict_preview(df_dict):
    """Print preview of dataframes within a dictionary."""
    print('\nHead & Tail of DataFrame rows & columns:\n')
    [print_df_preview(dfname, df) for dfname, df in df_dict.items()]
    


## Load CSV into `datasets_di`, a dictionary of dataframes, 1 dataframe for each CSV file.

# Identify dataset by directory name, allow for more than 1
dataset_dir_list = ['Data']


# Create dictionary of dataframes
suffix = '.csv'
datasets_di = {}
for dataset_path_to_dir in dataset_dir_list:
    datasets_di.update(csv_dir_to_df_dict(dataset_path_to_dir))


# All data is now loaded into `datasets_di`.
# 
# Let's preview the loaded data ...

# Preview a few rows & columns of each dataframe. Include their shapes.
print_dfdict_preview(datasets_di)


# Clean the datasets to make it ready for analysis ...

# ### Data Cleaning
#
# Before data cleaning starts:
# * Create a dataframe called `meta_df` to itemize the dataframes.
# * Simplify dataframe names.
# 
# Then clean and trim as follows:
#
#  **Columns**
#  Each dataframe contains a row for each country, and a sequence of year
#  columns. Standardize the name of the country column to 'country' and 
#  index on it.
# 
#  **Zeros and NaN**
#  Zero values are assumed to be years in which a statistic for a 
#  country was not gathered. Zeros can skew the data when calculating 
#  aggregates. For this reason, reset zero values to NaN.
# 
#  **Countries**
#  Not all dataframes contain the same set of countries.  Avoid 
# attempting to draw correlation between country statistics when not all 
# countries have recorded statistics by trimming dataframes so they share 
# a common set of countries.
# 
#  **Years**: Not all dataframes contain the same range of years. 
#  Trim dataframes so they share a common range of years for consistent 
#  analysis.

# #### Metadata
# Create `meta_df` to itemize loaded datasets. 

# Initialize meta_df with dataframe names
meta_df = pd.DataFrame([dfname for dfname in datasets_di.keys()], \
                       columns=['dataframe'])


# Dataframes were named with CSV filenames, which are long and wordy. 
# Create shorter aliases in `meta_df`.  

# First, create an alias dictionary. Prompt user for each alias, offer a default ...
alias_di = {}

# For each df, prompt for alias, default = first word delimited by underscore
print('\nEnter alias for each dataframe (press enter to accept default):\n')
for dfname in datasets_di.keys():
    this_alias = '_'.join(dfname.split('_', 2)[:2])
    this_alias = input('{}: ({})'.format(dfname, this_alias)) or this_alias
    alias_di[dfname] = this_alias
    #print('"'+'\n"'.join(str(dfname)+'":"'+str(dfname).split("_")[0]+'",'))

print(alias_di)

# Map the dataframe aliases to `meta_df` dataframe names and index on it.

meta_df['statistic'] = meta_df['dataframe'].map(alias_di)
meta_df.set_index('statistic', inplace=True)
meta_df


# ***
# Now rename dataframes using the aliases ...

# List original dataframe names

dflist = list(datasets_di.keys())


# rename dataframes with their statistic name (mapped in meta_df)

for df in dflist:
    datasets_di[meta_df[meta_df['dataframe'] == df].index[0]] = datasets_di.pop(df)


# Verify new dataframe (statistic) names

list(datasets_di.keys())


# ***
# Data structures are ready. Start cleaning ...

# #### Columns - Rename and Index
# Standardize all dataframe Country columns to 'country', and make it the row index.

# function to rename/reindex
f = lambda df: (df.rename(columns={'geo':'country'}).set_index('country'))

for dfname in list(datasets_di.keys()):
    datasets_di[dfname] = f(datasets_di[dfname])


# Confirm all indexes are 'country' 
# TODO: add error handling procedures

print('Are all dataframe indexes named "country"?')
'country' == np.unique(list(map(lambda k: datasets_di[k].index.name, (k for k in datasets_di.keys()))))[0]


# Backup datasets_di before trimming
datasets_di_backup = datasets_di.copy()


# #### Zeros and NaN - Cleanup
# Any Zero values are assumed to be placeholders for missing data. 
# Since zero values can inadvertently skew aggregate calculations, 
# reset them to NaN (null).
# 
# Afterwards, make sure there are now no rows completely empty.

# Functions for Cleanup
def print_zeros(dfname, df):
    """Return False if no zeros, True of any are found. Print columns and rows with Zero values."""
    result = False
    zero_count = (df[df.columns]==0).any(axis=1).sum()
    if zero_count:
        print('\n{}\n{}:'.format('='*50, dfname))
        print('{}\n'.format(df[df.isin([0]).any(axis=1)]))
        result = True
    return result
            

def print_if_all_nulls(df_dict):
    """Return None. Print report, listing any dataframes that have rows containing only null values."""
    found = False
    for dfname, df in datasets_di.items():
        if pd.isnull(df).all(1).any():
            print('{} has row with all nulls.'.format(dfname))
            found = True
    if not found:
        print('No empty rows.')
    
    return None


# Print any Zero values ...
print('DataFrame Rows with Zero Values:')
[print_zeros(dfname, df) for dfname, df in datasets_di.items()];

# Translate all Zeros into NaNs ...
# Replace zeros with NaN, then drop any rows where all values are NaN. 
for dfname, df in datasets_di.items():
    datasets_di[dfname] = datasets_di[dfname].replace({0:np.nan, 0.0:np.nan})
    datasets_di[dfname] = datasets_di[dfname].dropna(how='all')


# Verify there are no empty rows.
print_if_all_nulls(datasets_di)


# TODO: more error handling here ... handle any non-empty rows.
# 
# Start trimming ...

# #### Countries - Trim
# Make sure dataframes share a common set of countries (inner join) by
# trimming any countries not shared by all dataframes.
#
# First, identify the countries to be trimmed and list them in `meta_df` for reference.
# Create list of common countries.
dflist = list(datasets_di.values())
common_countries_list = pd.concat(dflist, axis=1, join='inner').index

# Add uncommon countries (to be trimmed) to meta_df.
meta_df['excluded_countries'] = ""
for data_set, df in datasets_di.items():
    meta_df.loc[data_set]['excluded_countries'] = [x for x in df.index if x not in common_countries_list]
    
# View the countries to be excluded.
pd.set_option('display.max_colwidth', -1)
meta_df

# ***
# TODO: add functionality to verify with the analyst that the above 
# list is acceptable before trimming excluded countries.
# 
# Exclude non-common countries from dataframes.
for dfname, df in datasets_di.items():
    datasets_di[dfname] = df[df.index.isin(common_countries_list)]

# Verify dataframe row counts match (confirming the same number of countries).
[print(df.shape[0], dfname) for dfname, df in datasets_di.items()];


# TODO: more automated exception handling here, verify working with a uniform set of countries. 
# 
# Trim year columns ...

# #### Years - Trim
# Verify a consistent range of years by finding a common range of years and trimming the rest.

# Functions for Trimming

def get_year_metadata(dict):
    """Return dataframe containing range of years."""
    result_df = pd.DataFrame()
    for dfname, df in dict.items():
        result_df[dfname] = [df.columns[0], df.columns[-1]]
    result_df = result_df.transpose()   
    result_df.rename(columns = {0:'first_year',1:'last_year'}, inplace=True)
    result_df.index.names = ['data_set']
    return result_df


def trim_df_dict(df_dict, col_list):
    """Return dictionary of dataframes, trimmed of columns not in col_list."""
    result_dict = {}
    for dfname, df in df_dict.items():
        keep_columns = [col for col in df_dict[dfname].columns if col in col_list]
        result_dict[dfname] = df_dict[dfname][keep_columns]
        
    return result_dict


# Before trimming years, record the original year ranges to `meta_df` 
# for reference, and report the Common Year Range.
meta_df = pd.concat([meta_df, get_year_metadata(datasets_di)], axis=1)
meta_df[['first_year','last_year']]

# Find common range
first_year, last_year = (meta_df['first_year'].max(), meta_df['last_year'].min())

# Confirm range of years
print('Common Year Range: {} -> {}\n'.format(first_year, last_year))


# TODO: more exception handling here.
# 
# Trim the years outside the Common Year Range.
years_in_range = [str(y) for y in list(range(int(first_year),int(last_year)+1))]
datasets_di = trim_df_dict(datasets_di, years_in_range)

# At this point, dataframes should have the same shape (country rows 
# and year columns). Verify this ... (TODO: automate the verification)

# Confirm trimmed datasets. Each dataset should have same year columns.
[print('{} <-- {}'.format(df.shape, dfname)) for dfname, df in datasets_di.items()];


# ***
# Dataframes should now clean and trim. 

# ***
# ## Correlation Analysis

# *** 
# Use `datasets_di` for these set of questions, since its dataframes 
# have a consistent country list and range of years. 
# 
# Consider each dataset an individual 'factor'. 
# 
# TODO: make factor identification more flexible, such as multiple factors per dataset.

# #### Prepare the data
# Create two new structures:
# * `dataset_stats` - dictionary of dataframes, similar to the 
#   `datasets_di` dataframes but containing only the averages 
#   for each country. (Includes averages of factor statistics. 
#   TODO: drop if not needed.)

# Create dataset_stats (dictionary of dataframes of with country means)
dataset_stats = {}
for dfname, df in datasets_di.items():
    dataset_stats[dfname] = df.transpose() \
                            .describe().loc[['mean']] \
			    .transpose()

# Create 2D array, a row for each stat: 
#   [[statistic name, statistic mean name]]
stats_arr = np.array([(stat, stat+"_mean") for stat in meta_df.index])
stats_arr

# Find the correlation between every pair of factor statistics. First, create the pairings ...
# Create tuple pairs of all our statistic (dataframe) combinations.
stat_list = list(datasets_di.keys())
dataset_corrs = pd.DataFrame(columns=['size','this_stat','that_stat','r'])
combines = list(combinations(stat_list,2))

# Now calculate the correlaltion coefficients ('r') for each pair ...
# Compute correlation coefficients against each statistic pair.
for stat_tuple in combines:
    this_stat = stat_tuple[0] 
    that_stat = stat_tuple[1]
    this_mean = dataset_stats[this_stat]['mean']
    that_mean = dataset_stats[that_stat]['mean']
    
    correlation = this_mean.corr(that_mean)
    dataset_corrs = dataset_corrs.append({'size':'all', \
                                          'this_stat':this_stat, \
                                          'that_stat':that_stat,  \
                                          'r':correlation  \
                                          }, \
                                          ignore_index=True \
                                         )  
        

# Filter moderate-to-strong correlations.
dataset_corrs = dataset_corrs[abs(dataset_corrs['r']) > .4].sort_values(by=['r']).reset_index(drop=True)
print(dataset_corrs)


# Visualize the pairings with a graph
df = dataset_corrs[dataset_corrs['size'] == 'all']
x = df['r']
y = df['this_stat'].astype(str) + ' / ' + df['that_stat'].astype(str)
data = pd.concat([x,y], axis=1).set_index(0).rename_axis('this/that')
ax = data['r'].plot(kind='barh',fontsize=13, color='steelblue',figsize=(8,8));
ax.set_title("Statistic Correlations, Globally", fontsize=20, color='black')
ax.set_xlabel("Correlation Coefficients", fontsize=18, color='black')
ax.set_ylabel("Statistic Pairs", fontsize=18, color='black');
plt.show()

# ***
