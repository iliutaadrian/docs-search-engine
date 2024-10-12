_work in progress_

# Overview

This section is structured as follows:

- The first line provides a basic definition for the term.
- The second line in each subsection describes where to find that information.

## Handicap Indexes

A universal value determined by past performance for a golfer's ability. This reflects how good a golfer is, eg. +2 pro (negative handicap), 16 amateur (positive handicap).

The handicap indexes can be imported or manually set in Golfers -> Event Roaster. Edit one of the golfers/members, then go to H.I. Summary section.

## Course Handicap

A course handicap is obtained by merging the handicap index with the course information. This value is defined as handicap index x slope rating / 113 + course rating - par.

The course ratings are shown in Round -> Handicap Analysis.

## Playing Handicap

The playing handicap takes the course handicap and adjusts it for the actual golf competition played. This can be a simple percentage of the course handicap or combinations of percentages (and/or sums, averages) when computing handicaps for pairs, foursomes etc.

This is specified in the Handicap Format in Round -> Tournaments -> Tournament Spec, and then computed in Round -> Handicap Analysis

## Handicap Allocation

The obtained playing handicap is then used to decide which holes get strokes reduction. Each hole should have a difficulty indicator (1-18). 1 - most difficult, 18 - least difficult. The value of the playing handicap is distributed 1-by-1 to the holes from the most difficult to the least difficult. This process is repeated until we remain with zero.

The allocation is shown on scorecards as dots and these dots are used to obtain the net score from the gross score. To view this, go to Round -> Display Leaderboard. Open an event leaderboard and expand a player's details.

# Debug

## Handicap Setup

## Handicap Settings

## Handicap Analysis