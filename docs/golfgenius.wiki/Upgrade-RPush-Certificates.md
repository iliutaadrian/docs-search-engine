Step 1. Generate new certificates

Step 2. Add them to /certificates, commit and deploy

Step 3. Using the Rails console, find the corresponding RPush app and update the certificate

```
app = Rpush::Apns::App.all[3]
app.certificate = File.read("certificate/productionPhillySection.pem")
app.save
```

Step 4. Restart the RPush pod