### Report on writing SuperPy

This project sure had its ups and downs.
I found it hard to get started, I felt overwhelmed and didn’t know where to start at all.
Eventually I started by trying to understand all the new aspects that we had to use, but haven’t worked with before. 
It was a lot and I also felt pretty demotivated by it all. 
I started writing code by creating the csv files and trying to read and adding and removing lines. This way I could write the buy_product() and sell_product() function and the corresponding functions to update the csv files.
By now I started having a little bit more of a vision on what I had to do and I dove into creating the charts of the inventory. The hard part here definitely was to also be able to display the inventory of dates in the past. Because this meant I had to extract the sold and expired products on certain dates and put them back into the inventory. And also remove bought products that were added later than the given date.
The calculation of profit and revenue on certain dates easier than I thought.

What I still haven’t really figured out is what the folder structure should look like. First I had all the functions within one helpers.py file, but I couldn’t find my way easily in it. So that’s when I decided to separate certain functions and put them into separate files. 
Also I still don’t see the use of coding test driven, it just doesn’t feel like an efficient way to code. But maybe I’m just not doing it right yet.

Overall I learned a lot by doing this project!