_[work in progress]_

This guide highlights the technical details behind the tournament scoring logic and provides some guidance to be able to investigate common scoring issues. 

# Overview

## Data Structures
> _This section includes information only on the structures used for the most common tournament formats._

To better understand how a tournament is structured, we could easily group the models into 2 main categories as follows:
* Tournament Settings
* Tournament Results


### Tournament Settings

#### _**Tournaments2::Spec**_
  * Definition of a tournament as specified by the user through the Tournaments Page, i.e. the tournament settings
  * Either single-round or multi-round tournament
#### _**Tournaments2::Event**_
  * Instance of a _Tournaments2::Spec_
  * Generated through the spec mapping process (`SpecMap V2`) after creating or editing the tournament settings
#### **_Tournaments2::AdditionalSettings_**
  * Extension of a `Tournaments2::Spec`
  * Avoids introducing new fields on the above models

Usually, tournaments are defined as a `Tournaments2::Spec` + `Tournaments2::Event`, but the structure slightly differs depending on their type. The most common tournament structures are included below.

<img width="1326" alt="Screenshot 2024-07-15 at 13 28 40" src="https://github.com/user-attachments/assets/0462e0dd-b7f5-4448-8a05-fff8ab44f722">

### Tournament Results
#### _**Tournaments2::ResultScope**_
  * Stores data relevant to the groups/players that played against each other
  * Based on who the tournament is played against (_vs. Field, vs. Flight, vs. Player, etc._)

_❗ Leaderboard results are computed within each result scope_

#### _**Tournaments2::NewAggregate**_
  * Stores data relevant to scoring/results of players who played together
  * Based on the scored entity (_Player vs., Pair vs., Team vs., etc_)
 
In the context of Multi-Round Tournaments, we also have the concept of over and under-aggregates that allow us to track the correspondent aggregate at the round level. The over-to-under relationship is mapped using the `Tournaments2::AggregateRelationship` model and accessed using `v2_children` or the `get_under_aggregates` method.

_❗ Each line on the leaderboard corresponds to an aggregate_

_❗ When past rounds data is visible on the leaderboard, the score in each past round column corresponds to an under aggregate_
 
#### _**Tournaments2::NewNet**_
  * Stores data relevant to each player in the tournament
  * Handicaps, hole-by-hole scores, handicap strokes by hole are stored at this level

_❗ Visible on the leaderboard when expanding the details of an aggregate_ 
#### _**Tournaments2::NewResult**_
  * Stores data on the results of a tournament from an aggregate perspective
  * Usually there is a single result record for each aggregate and the data corresponds (_ranks, scores, points, etc._)
  * There are a few cases where an aggregate has multiple result records (_most popular - for Nassau, results are computed individually for Front 9/ Back 9/ All 18_)

#### _**Tournaments2::NewMatch**_
* Stored data of the results of a match
* Match status and statuses by hole are stored at this level

_❗ Match records are created in both directions, i.e. a match for P1 vs. P2 and a match for P2 vs. P1_

## Scoring Process
### Scoring Job Scheduling
A rescore must be triggered whenever scores or tournament settings are outdated (`invalidate_leaderboard_scores` or `invalidate_leaderboard`). When the round is completed the job is scheduled the next time someone clicks on _Display Leaderboard_, while for in-progress rounds we try to schedule it right away (`queue_if_not_queued`).

<img width="1405" alt="Screenshot 2024-07-15 at 16 00 34" src="https://github.com/user-attachments/assets/dc53e8a3-6be5-451c-b033-b0dde10b2f4b">

  
### Scoring Engines
### Leaderboard Caching

> _Leaderboards on the manager side/portal always reflect the most recent state, i.e. no round index is used in cached keys unless the tournament is configured explicitly to use snapshots_

To better understand how round-by-round caching works, let’s use as an example a tournament over 4 rounds with the first 3 rounds scored:

* Round 1 - In Progress
  * A rescore is triggered for each score entered
    * _R1 JSON cache reflects the current leaderboard state_

* Round 1 - Completed
  * Final rescore is triggered
    * _R1 JSON cache reflects the current leaderboard state_
  * R1 cache gets updated **only** if a manual rescore is triggered or tournament settings are changes

* Round 2 - In Progress
  * A rescore is triggered for each score entered
    * _R2 JSON cache reflects the current leaderboard state_
    * _R1 JSON cache reflects R1 final state_

* Round 2 - Completed
  * Final rescore is triggered
    * _R2 JSON cache reflects the current leaderboard state_
    * _R1 JSON cache reflects R1 final state_
  * R2 cache gets updated only if a manual rescore is triggered or tournament settings are changes

* Round 3 - In Progress
  * A rescore is triggered for each score entered
    * _R3 JSON cache reflects the current leaderboard state_
    * _R2 JSON cache reflects R2 final state_
    * _R1 JSON cache reflects R1 final state_

* Tournament Settings Updated
  * A rescore is triggered for each round to propagate the settings
    * _R3, R2, R1 JSON cache reflects the current leaderboard state_

* Round 3 - Completed
  * Final rescore is triggered
    * _R3 JSON cache reflects the current leaderboard state_
    * _R2, R1 JSON cache reflects the leaderboard state right after tournament settings were updated_
  * R3 cache gets updated only if a manual rescore is triggered or tournament settings are changes


# What to investigate
