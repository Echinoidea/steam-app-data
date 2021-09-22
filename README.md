# steam-app-data
This is a work-in-progress project.

get-data.py - A Python script which gets the first 'n' titles from the Steam store page, using the BeautifulSoup library to get the app ID from the HTML elements for each Steam title. These app IDs are then passed into the SteamSpy API which returns a JSON object containing all the information on a provided app (title, developer, publisher, positive review count, etc.). This is repeated 'n' times and then is finally written to a single JSON file containing a list of each JSON object returned from SteamSpy.

I made this script to gather multiple large samples of Steam apps with different parameters to later analyze.

My initial goal was to determine whether independently published games (developer and publisher are the same) perform better or worse than dependently pubished games (developer and publisher are not the same). In the future, I hope to use this tool to gather more data with various qualities to answer other statistical questions about Steam.

SteamAppDataR contains histograms and an R script that parses the Steam data JSON files into dataframes to be used in R analysis. I haven't done much work on the R analysis yet, however.
