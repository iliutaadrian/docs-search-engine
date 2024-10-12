Article on how score posting works https://github.com/golfgenius/golfgenius/wiki/How-score-posting-works-for-GHIN

## Setup

Before posting scores, a handicap network must be selected. Go to 

**Event Profile > Handicaps > Handicap Index Service / Score Posting**

<img width="600" alt="Screen Shot 2020-03-02 at 13 29 47" src="https://user-images.githubusercontent.com/16760229/75672784-22f5d580-5c8a-11ea-8ca3-c9ac45763d7b.png">

## Posting Scores

To access the score posting page, go to

**Rounds > Pairings & Scoring > Post scores to (handicap_network) / See Posting Results**

<img width="800" alt="Screen Shot 2020-03-02 at 13 37 54" src="https://user-images.githubusercontent.com/16760229/75673238-2d649f00-5c8b-11ea-9394-cee6eb9b7696.png">


The **Adj. Gross Score** on this page is calculated inside `player.esc_scores_for_posting`

## Backend

Scores are first calculated inside `player.esc_scores_for_posting` and then adjusted for the handicap network to which they are posted. 

Before posting to **WHS/GHIN**, scores go through `whs.adjusted_scores_for_posting` where WHS specific adjustments are applied.

Then, scores are posted to the specific handicap network:

**WHS/GHIN** - `ghin.postScore`

**Handicap Serve**r - `handicap_server#post_scores`

**GolfNet** - `golfnet.postScore`

## FAQ

**WHS Credentials** - http://admin-stage.hcp2020.com/ / superadmin@hcp2020.com / adminportal1894

**Equis** - Net Double Bogey or Equitable Stroke Control is a **WHS/GHIN** specific adjustment that limits the score for a hole to a specific limit value. This limit is calculated in the `equis` variable.

**NH** - No Handicap refers to golfers that don't yet have a Handicap Index. They are treated as having the maximum Handicap Index for their gender, 36.4 for men and 40.4 for women. When posting to WHS, NH players are considered as having a handicap of 54 (both genders).

**9-hole Scores** - 9-hole scores posted to GHIN can't be overwritten. To repost 9-hole scores, `player.last_handicap_unique_id` must be set to `nil`. This is because in GHIN they are either placed in the holding tank or are immediately combined with the existing 9-hole score in the holding tank to obtain the combined score.