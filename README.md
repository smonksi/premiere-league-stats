# premiere-league-stats

Refactored the code so that it can cater for:- 
 any of the drop down lists
 extract results to a .csv file. 
 
The code needs optimsation, e.g. wait times are currently guesses instead of event driven, better error handling when no data is returned, etc.

Possible features: -

    User input on command line to specify search and results (e.g 2019/20 season, Chelsea, England, Stat > 10);
    Ability to return a complete data set for a given player via online profile;
    Ability to pagingate through results where number of players found exceeds page limit of 20;
    Ability to define which fields should be returned from extracted data sets, with .csv file generated accordingly;
    Ability to write to your own database!