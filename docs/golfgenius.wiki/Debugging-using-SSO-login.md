Here are the different links used for SSO: https://docs.google.com/document/d/14--6QPW2hP37Cg2uxSAPi7AOzJihCy9y4gYSrxtbzTk/edit#heading=h.edtzv4eyozcn

The example below demonstrates the process for the PGA MembersFirst integration.

## Log in via SSO for LPGA (and others) using our general integration protocols

We can use SSO to log in as a certain player from an external provider. The SSO link is as follows:

`http://localhost:3000/sso_gg?memberNumber=` ? `&redirectURL=ggid%2F` ? `%2Fregister`

The `memberNumber` is the value of the memberNumber custom field in the Master Roster for that player. The
`redirectURL` is the GGID link for a portal or directory that you want to go to.

## Example

### 1. Member number

Found the `memberNumber` in the Master Roster: `bdfcba73-fc40-4402-8e4b-3f6f813ec5b8`

<img width="1014" alt="Screen Shot 2020-03-17 at 14 53 32" src="https://user-images.githubusercontent.com/16760229/76857935-1c0cbc80-685f-11ea-89cb-749d5eaedb35.png">


### 2. GGID

Found the Event GGID in Event Profile: `XEBYSG`

<img width="1104" alt="Screen Shot 2020-03-17 at 14 54 33" src="https://user-images.githubusercontent.com/16760229/76858012-3e9ed580-685f-11ea-9335-651b137e7213.png">


### 3. SSO link

Put the SSO link together:

`http://localhost:3000/sso_gg?memberNumber=` ? `&redirectURL=ggid%2F` ? `%2Fregister`

http://localhost:3000/sso_gg?memberNumber=bdfcba73-fc40-4402-8e4b-3f6f813ec5b8&redirectURL=ggid%2FXEBYSG%2Fregister

# Other SSO Scenarios
Documentation can be found at this link: [SSO Scenarios Doc](https://docs.google.com/document/d/1VhWzs3p3cJ9w3aOBCdyVFpGvLQlUVqcEsU4vTaZbb_M/edit#)