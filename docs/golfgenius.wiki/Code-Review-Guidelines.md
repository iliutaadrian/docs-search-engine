# Code Review Checklist

For any pull request over **20 lines** of code changes, the owner copies and pastes the following table in the pull request comments. Then walks through the list of items below and fills in each line as either OK (condition checked), TD (needs further discussion) or NA (Not Applicable).

**General**  
- [ ] Code has been fully tested on local system.  
- [ ] Code is not duplicated. There is no duplicated code that could be extracted into functions or classes.  
- [ ] English language is clear and does not contain typos - fill in as TD if you think the texts need further review.
- [ ] Translations
- [ ] If you created a new page (or a popup) - when opening it up, the first input should be automatically focused

**Automated Tests**  
- [ ] Having automated test coverage for new functionality.  
- [ ] Functions should have unit tests for all possible inputs and outputs.  
- [ ] Add Factory for all new models you are adding via migrations.

**Syntax Guidelines**  
- [ ] Variable names do not contain typos.  
- [ ] Variables defined globally are used globally.  
- [ ] Not using "and", "or" as conditionals.  
- [ ] Not using "x == 0 && 0 || 1" (instead of ternary operator).  
- [ ] Not adding any model callbacks: touch: true, no after_update, after_save, etc.  
- [ ] In DJs sometimes parameters in a hash get passed in as strings instead of symbols, e.g., options["id"] instead of options[:id] - use binding.pry to ensure the values get passed as you expect them [Sample Code](https://github.com/golfgenius/golfgenius/commit/dbf65a69b05678db6e2f9335233e94b9b516f69b)    

**Performance**  
- [ ] Not using .present? on relationship (instead, use .limit(1)).  
- [ ] Reviewed SQL logs. Cannot do further improvements.  
- [ ] Reviewed SQL logs. Used mass-insert libraries where needed: Upsert, AR-Import.  
- [ ] Using LDS if the same object can be loaded multiple times.  
- [ ] Counts, maximums, sums should be done in SQL if possible.  
- [ ] Code that is called often (e.g., navbar) is using caching.  
- [ ] Communication to external services is done in background.  

**Migrations**  
- [ ] New tables - follow the Sharding protocol when creating new tables.  
- [ ] Serialized columns are of type text.  
- [ ] New id columns are of type big int.  
- [ ] Enforce value uniqueness by adding uniqueness index.  
- [ ] Migrating existing data is done in background jobs.  
- [ ] Added corresponding database indexes for all searches.  
- [ ] No additional fields on large tables: leagues, rounds. For new fields, please use the VariableSettings model (together with examples found by searching code base for variable_settings_leaderboard_affiliations)  
- [ ] New fields, added in this release, have been propagated to other reports as needed.   
- [ ] Propagations: from leagues to rounds, cloning leagues and events.   
- [ ] Propagations: new tournament fields added in app/lib/league_round_fields.rb

**Security**  
- [ ] All controller actions use authorize! to guard against URL manipulation.  
- [ ] All controller actions require a user to be logged in if required.  
- [ ] SQL finders that are not linked to a previously authorized objects also use authorize!  
- [ ] We are not storing passwords or critical user information in clear text.  

**Concurrency**  
- [ ] Tested code with multiple people on same link in multiple browsers.  
- [ ] Potential concurrency problems are solved with advisory locking or other mechanisms.  
- [ ] Touch: true is not used or is used in such a way that does not generate deadlocks.  

**Browser**  
- [ ] All buttons are guarding against double clicking using disable_with.  
- [ ] JavaScript code tested (function and performance) on Internet Explorer.  
- [ ] UI elements have been tested on the last 2 versions of the following browsers: IE, Safari, Firefox, Chrome and iOS & Android mobile browsers. Use BrowserStack.com / coders@golfgenius.com / @rdmorePA 

**Printing**  
- [ ] Printing PDFs is using DelayedRenderController or a controller inherited from it.  

**Time Zone**  
- [ ] Code is working properly across multiple time zones.  

**Propagations**  
- [ ] Are there fields which require propagating from league profile to round profile?        
- [ ] Are there fields which require propagating when cloning leagues or events?  
- [ ] Are there fields which require propagating between the various tournament types: single, multi, linked, user scored?           

**Handicaps**  
- [ ] If code is dealing with handicaps, always test both negative and positive numbers. Golfers see "+4" and "4" as different numbers, and computers do not :). Use the HandicapUtilities concern when dealing with handicaps.  
- [ ] Use tournament handicaps as much as possible. They are reliable, test suite covered and we rarely receive questions that cannot be answered by looking at the Handicap Analysis.  
- [ ] Each event may be set to use different index types: 9 holes / 18 holes / both indexes. These need to be treated differently when displaying and sorting indexes. When 18 hole index is selected, text should say "Handicap Index". When 9 hole index is selected, text should say "9-Hole Handicap Index". When both are selected, text should say "18-Hole Handicap Index" and "9-Hole Handicap Index".  
- [ ] Only GHIN and GolfNet require unique ids for members. HandicapServer & Manual should never present a text field to be filled in at the member level.

**Member Guest Ordering & Genders**  
- [ ] Ordering of golfers in teams, tee sheets, foursomes is important! Confirm ordering by member then guest when displaying data.  
- [ ] [Genders should use the default gender or the majority gender](https://github.com/golfgenius/golfgenius/wiki/Genders-in-Golf-Genius)  

**Tees**  
- [ ] When dealing with tees being played on, confirm that we are looking and treating all types of tees: 18-hole tees, 9 hole tees, front or back and rotated tees.  
- [ ] Set up default tee if exactly one tee selected.  

**Scores**  
- [ ] Each round may use 9 hole totals, 18 hole totals or hole by hole scoring. Test if impact.  
- [ ] Each round may use scramble, alt shot or regular play. Test if impact.  
- [ ] Each round may be set to play in twosomes, threesomes, foursomes, fivesomes and sixsomes. Test this if it has any impact, especially when looking at printed materials.  

**Spreadsheets**  
- [ ] When dealing with spreadsheets, column names may contain characters like “,‘. Confirm all extra characters are ignored when matching to internal fields.  

**Navigator**  
- [ ] New links added in the menus should be included in the Navigator as well [Learn More](https://github.com/golfgenius/golfgenius/wiki/Navigator).  

**API**  
- [ ] Does this function have any impact on mobile phones and mobile APIs? If yes, is the change backward compatible? If no, make it backward compatible and expire previous API users as necessary (AppVersion model).  

**Terminology**  
- [ ] Terminology is different across the different golf regions: US & Canada / UK / EGA. Is this a function that will be used worldwide and what implications does this have?  

**Release Planning**  
- [ ] Functionality could be released to a subset of the customer base or admin only if we are looking to receive more feedback from specific customers before pushing forward. This is currently done by adding checkpoints on a per customer level.  

**External Dependencies**  
- [ ] Don't load popup content in an iframe unless you have to.  And if you do, be sure to disable the intercom widget for that popup (if the layout doesn't already exclude it).  
- [ ] PGA of Canada is using custom code hosted by our app to display their rankings on the homepage. Confirm that any changes to HTTPS, serving static assets, do not affect them.  
- [ ] If you use a new gem or library, check the license. WE SHOULD NOT USE GPL licensed libraries or gems. Ask Alex and Flavia if the license is not MIT.  
