# Adding a new Navigator option

Go to http://localhost:3000/admin/navigator_options.

You must provide the 2 required fields:
- Name
- Internal Id

You must add a new rule in the `app/lib/navigator_permission_checker.rb` file. If the `internal_id` is equal to `print_scorecards` then you must implement a `check_print_scorecards` method.

These steps will guarantee that the option is present in the Navigator and after that you can tweak it by editing the tags and the weight. A higher weight means the option will appear higher in the results.
