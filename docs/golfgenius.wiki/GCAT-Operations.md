# Merging players

Sometimes, user records get mixed due to user errors. For example, we may have two records:

```
Member 1, User 1
Member 2, User 2
```

The user logs in on Golf ID with user 2. Member 2 was created in mistake and is not used (check payments). In order to move Member 1 to use User 2, steps are:

```
# calculate user1, user2, member1, member2
member2.destroy
user1.members.update_all(user_id: user2.id, email: user2.email, updated_at: Time.now)
Registrationv2.where(user_id: user1.id).update_all(user_id: user2.id)
MemberCard.where(user_id: user1.id).update_all(user_id: user2.id)
UserCustomerAccess.create(user_id: user1.id, customer_id: 18589, access_type: "league-member")
```


