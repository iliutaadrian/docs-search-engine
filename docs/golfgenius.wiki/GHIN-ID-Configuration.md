When filling in the GHIN identification information in TMS at the club level, we need 2 pieces of information:
* the association number
* the club number

The association number is the ID seen in GHIN for all clubs. Delaware is 102, Alabama is 19 and so on:

![unnamed](https://user-images.githubusercontent.com/16760229/77314021-32a29000-6d05-11ea-97a3-90e3a65baf15.png)

For the club number, there are 2 cases to deal with:

### Clubs that existed in the old GHIN system

Clubs that are migrated from old GHIN (GHP) will have a GHP ID; this ID concatenates the association number and the legacy club number. We need to fill in the legacy club number in TMS. For DuPont, this would be 3742. (blue box in the screenshot below)

<img width="1327" alt="Screen Shot 2020-02-25 at 1 30 15 PM" src="https://user-images.githubusercontent.com/16760229/77314024-333b2680-6d05-11ea-8ad7-f0dd40e6b3a7.png">

### New clubs

Clubs that are created in the new GHIN system will not have the GHP listed on their profile. In that case, you fill in the club number in TMS. See YOC Delaware below. (purple box)

<img width="1339" alt="Screen Shot 2020-02-25 at 1 33 22 PM" src="https://user-images.githubusercontent.com/16760229/77314027-346c5380-6d05-11ea-94cd-8f2840a5cb6f.png">

### Misc

In addition to all this, when creating a new association customer in TMS, we need to fill in an “association_number” field on the record with the association number from GHIN, e.g., 102 for Delaware. This can be done from the developer console. This is important for establishing eligibility criteria down the line.
