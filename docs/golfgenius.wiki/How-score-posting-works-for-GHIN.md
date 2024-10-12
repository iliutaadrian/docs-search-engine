## 1. Getting the Adjusted Gross Score

The Adjusted Gross Score is calculated in _whs.rb#adjusted_scores_for_posting_.

It receives as params: player and max par (optional parameter).

The logic takes into account all the conditions for score computations, such as: if incomplete scores are allowed, any additional strokes, etc.

Nothing to do here, just call this method for each player and it will return the scores for each side.

`scores_hash = {`
* `“all”: [<contains the adjusted gross score (total) and other related data>],`
* `“front”: [<contains the adjusted gross score for front9 and other related data>],`
* `“back”: [<contains the adjusted gross score for back9 and other related data>]`
`}`

## 2. Score posting methods

For posting and updating the scores in GHIN2020, we use 5 api methods:
* Post_total_score
* Post_9_hole_score
* Post_hole_by_hole_score
* Update_score
* Update_hbh_score

Depending on the types of posting the system allows, you’ll have different methods.

### 2.1 Post_total_score

This type of score posting is done when the scoring method is 18-hole totals (set in Round profile)



This will post the adjusted gross score

### 2.2  Post_9_hole_score

This type of score posting is done when the scoring method is 9-hole totals.

The 2 scores will be in the scores_hash (see point 1), in “front” and “back”.


### 2.3  Post_hole_by_hole_score

This type of score posting is done when the scoring method is HBH.

You’ll find the score for each hole in the scores_hash (see point 1), in “hole_nums” (on the “all” side)

**2.3.1 Posting HBH scores in relation to CRS**

For posting to GHIN2020, we allow posting HBH scores only if the course is imported from CRS/CRD (Course Rating System/Course Rating Directory) and all the data is in sync.

Checking if data is in sync (TMS vs CRS): 
* we compare the tee data in TMS with the tee data of the course from CRS
* We consider that data to be fully matching if the slope, rating, pars and handicaps match - “all”
* We consider the data to be partially matching if the rating and the slope match - “partial”
* Otherwise, no match - “none”

For that, we have the following conditions:

* If the course and played tee are imported from CRS and all data matches => post HBH score
* If the course and played tee are imported from CRS and data matches partially => add up the scores from all the holes and post total score
* If the course and played tee are imported from CRS and no data matches => add up the scores from all the holes and post total score as manual (explained in the next section)
* If the course is from CRS, but the tee is not (i.e. the course was imported from CRS, but the played tee is a manual tee, added from TMS) => add up the scores from all the holes and post total score as manual (explained in the next section)
* If the course is NOT from CRS => add up the scores from all the holes and post total score as manual (explained in the next section)

Posting HBH scores fails:

* If posting the HBH scores returns an error, we fallback to posting the total score.
* If the second posting also fails, only then we consider the whole posting failed.

**2.3.2 Manual Scores**

For GHIN2020, it’s important if the posted score is “manual” or not - a manual score will not be used for the PCC computation.

A score is marked as manual if the course/tee is:
1. not in sync with CRS (i.e. tee in TMS should have at least the same slope and rating as tee in CRS).
2. Not imported from CRS in the first place.

If this aspect is important to the new system, then the conditions above should be considered.

If not, then a normal HBH score posting should be done, without all those extra checks.


### 2.4 Update_score and Update_hbh_score

The player model has an attribute - “last_handicap_unique_id” - that holds the id of the score posting.

With this attribute, we check if we should post a new score for the player or update an existing one.

The update api methods receive the last_handicap_unique_id as a parameter (for finding the score).

