# steam-app-data

get-data.py - A Python script which gets the first 'n' titles from the Steam store page, using the BeautifulSoup library to get the app ID from the HTML elements for each Steam title. These app IDs are then passed into the SteamSpy API which returns a JSON object containing all the information on a provided app (title, developer, publisher, positive review count, etc.). This is repeated 'n' times and then is finally written to a single JSON file containing a list of each JSON object returned from SteamSpy.
