## Code

Example ticket [[bugs] Not a Bug - Remove my Stripe Account from an account](https://github.com/golfgenius/golfgenius/issues/33984#)

Code template:

```ruby
Sharding::TenantManagement.switch_shard(6172234676346848260)
CustomerStripeAccount.find(6172234676346848260).destroy
InvoiceSummary.where(customer_stripe_account_id: 6172234676346848260).update_all(customer_stripe_account_id: nil)
League.where(customer_stripe_account_id: 6172234676346848260).update_all(customer_stripe_account_id: nil)
```

## FAQ

* After removing a Stripe account that is set as a Payment Gateway, another Stripe account must be set in its place
* ...