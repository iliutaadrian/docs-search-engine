This is a section were you can write details about recurring bugs to have the details at hand so we don't waste time.

# 1. BUG TITLE

SHORT BUG DESCRIPTION

FIX:
```ruby
```

- LINK-TO-JIRA-ISSUE

# 2.[PGA Sections] Duplicate Invoice

SHORT BUG DESCRIPTION

Occasionally, when making a payment/registration that involves PGA Invoice reporting, under the PGA status column it will be stated that the invoice already exists on their side. On our side there is only one PgaInvoiceResponse that has the status set as failed. This should not be happening because the invoice we are reporting is a new one.

FIX:
The temporary fix for this is manually marking the invoice as sucessfully reported to PGA. This can be done by running the following console commands:
```ruby
h_find(InvoiceEntry, <invoice_entry_id>)
PgaInvoiceResponse.where(invoice_entry_id: <invoice_entry_id>).update_all(
    pga_invoice_id: "<pga_invoice_id>",
    message: "PGA of America Invoice ID <pga_invoice_id>",
    success: true
)
```

- LINK-TO-JIRA-ISSUE: https://golfgenius.atlassian.net/browse/TM-7539
