# premiere-league-stats

Refactored the code so that it can cater for: - 
-   any of the drop down lists
-   extract results to a .csv file. 
 
The code needs optimsation, e.g. 
-   wait times are currently guesses instead of event driven 
-   better error handling when no data is returned

Possible features: -

-   user input on command line to specify search and results (e.g 2019/20 season, Chelsea, England, Stat > 10);
-   ability to return a complete data set for a given player via online profile;
-   ability to pagingate through results where number of players found exceeds page limit of 20;
-   ability to define which fields should be returned from extracted data sets, with .csv file generated accordingly;
-   ability to write to your own database!

# New features 21 July 2023

Refactored the code so that it can cater for: - 
-   new layout of Premiere League website
-   more consistency and efficiency

Added new features or adjustments: -
-   .csv filenames generated automatically based on selection
-   print the current record set title to the .csv file (e.g. club name, position, nationality, season etc)
-   adjusted delay in 'get_result_table_by_class' to allow for for each new recordset to be retrieved and displayed

# New features 26 July 2023

Added new features or adjustments: -
- pagination enabled, if more results pages are available: -
  - the pagination next button is clicked
  - the results page is saved
  - until the pages run out and the pagination button is disabled
- refactored set_active_season: - 
  - current_season global 
  - active_season global 
  - add active_season to end of filename
  - directly set target season for search
# TODOs
- [ ]  cater for multiple season passes on same query type (e.g 'All CLubs' or 'All Positions' ) 
- [ ]  all code now requires refactoring!
- [ ]  improve error handling and validtation, especially for user inputs on command line

# New features 27 July 2023

Added new features or adjustments: -
-   basic refactoring in readiness for multiple season looping

# New features 28 July 2023

Added new features or adjustments: -
- refactored code, mainly to organise functions in logical groups
- added stat type capability (e.g. Appearances, Goals, Assists etc)
  - new function, set_active_stat()
  - changes filename to "Player [stat type] all [search type] [season].csv"
  - further refactoring incluing refined set_active_stat()
- added get_next_element() to find the following sibling by tag
- added new command line argument feature e.g.
  - python3 premiere_league_stats.py -s Appearances -y 2022/23 -p
  - python3 premiere_league_stats.py -s Assists -y 2003/04 -n
  - python3 premiere_league_stats.py -s Goals -y 2001/02 -p


# New features 30 July 2023

Added new features or adjustments: -
- error handling
- added error handling to set_active_season
  - if an invlaid season is requested, an error is printed
  - then set_active_season() defaults to current_season value
- added get_filter_button() 
  - find the filter button by filter name instead of current list value 

