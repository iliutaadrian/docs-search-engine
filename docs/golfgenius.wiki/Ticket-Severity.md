## Flow

After being inspected, issues are marked with the following `s/` labels that communicate their priority:

|Severity-4 (Minor)|Severity-3 (Most bugs)|Severity-2 (Urgent)|Severity-1 (911)|
|---|---|---|---|
|Issues that don’t directly impact product usability.|Incidents that impact product usability but don’t bring it to a halt or affect more obscure functions.|A feature is down for a large number of customers. Basic functionality is down for a small subset of customers.|Basic functionality is not usable for important customers.|
|Issues that do not impact the usage of the product|Issues that make the product harder to use but the customer is able to complete his goal|A feature is unusable for one or multiple customers|Important functionality is not usable|
|**Ex:** A logo is obscuring the last letter in a headline, some behavior needs clarification.|**Ex:** Slower-than-average load times, a player was included in the wrong division.|**Ex:** Can’t print reports with specific settings, 3/3/3 tournaments not scoring as expected.|**Ex:** A major customer can’t display leaderboards for a new round.|

When in doubt go with the higher Severity, better be safe than sorry. When assessing priority think of the following:

1. The nature and seriousness of the problem
2. The number of users affected by the problem
3. How quickly it needs to be attended
4. The possible reason that caused the problem
5. How soon can it be fixed

## Email templates

**Severity-4**

Thank you for reporting this issue. We believe this to be a minor/isolated bug with no direct impact on product functionality.

**Severity-3**

Thank you for reporting this issue. We believe this to be a bug that directly impacts product usability but doesn’t bring it to a halt.

**Severity-2**

Thank you for reporting this issue. We believe this to be a bug with a direct impact on important functionality. Given the severity, we consider it a high priority.

**Severity-1**

Thank you for reporting this issue. We believe this to be a bug with a direct impact on basic functionality. Given the severity, we consider it a top priority.
