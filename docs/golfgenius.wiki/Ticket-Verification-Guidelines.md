## Intro
The ticket verification process is the last-to-final part of the Engineering Support process. Everybody on the bugs team can verify tickets to prepare them for the final review and merge phase.
The Guardians on duty each day are assigned the role of **Fixer** or **Verifier**. The **Fixer** focuses on solving new tickets while the **Verifier** reviews tickets that already have a fix proposed.

| | Fixer | Verifier |
|---|---|---|
|**Focus**|Implement new solutions|Review existing solutions|
|**Request**|Reviews from the Verifier|Changes from the Fixer|
|**Labels**|`needs-review`|`feedback-available`, `verified`|
|**Columns**|To do -> Solution available|Solution available -> Verified|

A Guardian can switch its role if necessary. For example, a **Verifier** can take the **Fixer** role if there are no more Issues marked for review (labeled `needs review`).
Roles are assigned directly in the [Watch Schedule](https://docs.google.com/spreadsheets/d/1CR96shZ0bAyviDydUjGgGxmg6iVXSanh1dNrQ28AbY8/edit?usp=sharing)

## Steps
**_Request a review > (Recieve feedback > Apply feedback) > Recieve the `verified` label_**

![Verification Flow Chart](https://user-images.githubusercontent.com/16760229/69150120-a6772680-0ae0-11ea-98ad-ff8924b1f60b.png)

## Requesting a review - Fixer
After implementing a solution (creating a Pull Request and adding it to the "Solution available" column), you must request a review from the **Verifier** on duty that day. Use GitHub’s "Reviewers" panel to do this. Mark the corresponding Issue with the `needs-review` label to let people know that you have implemented a fix ready for review. 

![Reviewers Panel](https://user-images.githubusercontent.com/16760229/69150131-ad9e3480-0ae0-11ea-8dd5-53a6cddc60f3.png)

## Verifying a solution - Verifier
As a **Verifier**, your duty is to review the Issues marked with `needs review`. Before reviewing a Pull Request, assign it to yourself and also request a review from yourself.

When verifying an issue, start by testing the functionality and especially the scenario mentioned in the Issue. If you are unsure about how about the correct behavior of a feature, you can always check the [Knowledge Base](http://docs.golfgenius.com/content) or the [Specs](https://drive.google.com/drive/u/2/folders/0BwpZoxRW--QlZUd5RnVsZ0lvVWM) for that feature.

Try to also cover all the scenarios affected by the solution. Use screenshots to document your tests. You can use this comment as an example of how a review should look like: [#31852](https://github.com/golfgenius/golfgenius/issues/31852#issuecomment-551076700)

Proceed then with reviewing the files changed. Inspect the code diff for possible smells or refactorization ideas.
If any issues or smells were found, request changes in the Review section of the Pull Request and mark it with the `feedback available` label. If the changes required are minor and you are confident about them, please implement and test them yourself instead of sending them back to the Fixer.

![Requesting changes](https://user-images.githubusercontent.com/16760229/69150157-c3135e80-0ae0-11ea-973f-7743bdce00de.png)

If there are no more changes to be made, mark the Issue with the `verified` label.

## Applying feedback - Fixer
Treat answering feedback as a priority over working on a new issue. It is important to be responsive to changes and suggestions. After applying the feedback, mark requests as completed and remove the `feedback-available` label from the Pull Request.