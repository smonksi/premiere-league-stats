# premiere-league-stats

Refactored the code so that it can cater for:- 
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

# refactoring 21 July 2023

Refactored the code so that it can cater for:- 
-   new layout of Premiere League website
-   more consistency and efficiency
-   .csv filenames generated automatically based on selection
-   print the current record set title to the .csv file (e.g. club name, position, nationality, season etc)