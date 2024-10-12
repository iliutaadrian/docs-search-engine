Based on the following issue: https://github.com/golfgenius/golfgenius/issues/31333

We have a procedure that gives us the ability to fix Season Points (which are based on Member Cards) for **PPGA** (customer **19589**).

Methods used:

`Migrate.fix_pga_member_cards_by_email`

`Migrate.fix_extra_mcs_by_email` (as of July 26, 2019 the code is only available in _develop_. Will be available in master after R4/2019)
