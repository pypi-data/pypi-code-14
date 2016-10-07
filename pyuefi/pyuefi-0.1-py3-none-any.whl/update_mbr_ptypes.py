"""
Retrieve the web page at http://www.win.tue.nl/~aeb/partitions/partition_types-1.html
Then scrape through the HTML (using Beautiful Soup)
Update the partition_types_mbr.json file with the scraped data

Looks like the first <dl> tag has all the useful information, with each entry being in
its own <dt><b>...</b></dt> structure, so it should be pretty simple to grab the
interesting stuff with a regular expression.
"""
raise NotImplementedError
