We use the `CanCan::AuthorizationNotPerformed` helper to detect when a page is missing authorization and report this to developers. Most pages should check if the current user has the necessary permission to access their resources, but there are exceptions such as Portal Widgets or APIs.

Ideally, we want a page to abide by the **Principle of least privilege**, meaning a user on the page must be able to access only the information and resources that are necessary for its legitimate purpose.

## Levels of permissions
1. Not logged in
2. Regular User
3. Event Manager
4. Customer Manager
5. Admin

### Level 5 - Admin
Actions that affect multiple customers or are highly destructive in nature, should be restricted to Admin users.

Use: `is_admin? `or `user.try(:admin?)`

### Level 4 - Customer Manager
Actions that affect multiple events, should only be available to Customer Managers or higher.

Use: `can?(:manage, customer) && !user.is_tour_manager?`

### Level 3 - Event Manager
Users can also have Manager access to certain Events.

Use: `can?(:manage, league)`

### Level 2 - Regular User
Regular users can edit resources added by them previously, such as registration entries.

Use: `authorize :visit, page`

`can?(:visit, page)`

### Level 1 - Not logged in
This applies to a small subset of pages, usually Portal Pages (public) or APIs (authorization based on key) 