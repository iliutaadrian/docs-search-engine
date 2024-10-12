## Details

Docs: [DEV-11: Run custom code on production](https://docs.google.com/document/d/1PIKW8pvM0LkpZrx3GF5lyKqRkfF7csDWLG7FmjSLP_U/edit?usp=sharing)

Spreadsheet: [Custom code (production console)](https://docs.google.com/spreadsheets/d/17rS_CY84tT081ePH7Z9GB7tPMB8Mkd8ZhEC6ujSEtYs/edit#gid=187945483)

The _Pull Request/Issue_ **must** contain clear screenshots before and after highlighting the changes, the number of affected customers/users, repro steps.

1. Screenshots should be done by the owner of the code
2. Number of affected users/customers should be determined by the owner of the code
3. If the code is part of a reversible migration, make sure that both up and down methods are properly defined
4. Repro steps should be documented, such that anyone that wants to verify the behavior before/after running the code should be able to do it

## Custom Code Console Template

**Problem**

**Solution**

**Test setup/repro steps**

**Code to run**

```ruby
Sharding::TenantManagement.switch_shard 123456
Foo.where(bar: 123456).destroy_all
```

**Before**

**After**

**Impact (minor/major)**

Customers affected: X

Users affected: Y


