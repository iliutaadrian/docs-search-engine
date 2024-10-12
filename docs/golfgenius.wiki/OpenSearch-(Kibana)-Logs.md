### Important Mention

Everything that is about to be presented requires the presence `golfgenius-vpn` VPN setup (basically the same one that lets you connect to the staging DB) in order to be accessed.

### Easy Access

https://vpc-tms-logs-jsi42xzw45hjap55nq336bpjgu.us-east-1.es.amazonaws.com/_dashboards/app/data-explorer/discover/#?_a=(discover:(columns:!(_source),interval:auto,sort:!()),metadata:(indexPattern:bae2ad20-fa2e-11ec-9c28-a920980814d2,view:discover))&_q=(filters:!(),query:(language:kuery,query:''))&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))

### Introduction

OpenSearch is a tool we are using to analyse the logs that different levels of the infrastructure output in their internal processes. Each of the products in Golf Genius Software have their own OpenSearch setup, meaning you will basically need only the link above in order to access the logs related to TMS.

### TMS OpenSearch Categories

Moving forward, when opening the link, we can see that the logs are as mentioned above, grouped based on the layer of architecture they exist in, and the environment they exist in:

1. Production
  - prod-tms-alb-*
  - prod-tms-app-*
  - prod-tms-infra-*
  - prod-tms-waf-v1-*
2. Staging 1 (ggstest.com)
  - dev-tms-alb-*
  - dev-tms-app-*
  - dev-tms-infra-*
  - dev-tms-waf-*
3. Staging 2 (ggstest2.com)
  - dsg-tms-app-*
4. Staging 3 (dtg.ggstest.com)
  - dtg-tms-app-*
5. Others
  - core-tms-infra-*

As you can see above, there are basically 4 distinct levels of architecture which we can see:
1. ALB (Application Load Balancer)
2. APP (Application)
3. INFRA (Kubernetes Stuff)
4. WAF (Web Application Firewall)
5. CORE - not really relevant for us so we'll ignore it.

#### ALB layer

What the ALB layer does is basically sitting on top of the application, directing requests to each frontend pod. (and a whole other lot that is not really relevant for this wiki)

Some relevant information that can be extracted from here is:
1. backend_status_code
2. backend_processing_time
3. request
4. sent_bytes

This is usually the category you'd look into in case of a whole system slowdown/ repeated kills/ etc, when the offender is not obvious from the other categories.

#### APP layer

This is the category you'll be using in 90% of the cases.

These are the logs coming from inside the unicorn process, its associated workers and the nginx container living in the same pod. 

The first thing that must be mentioned here, is that the only logs that will actually be recorded in OpenSearch are the ones with the log level matching or higher than the Rails config log level.

More clearly, the log levels are, :debug, :info, :warn, :error, :fatal, and :unknown, ordered from 0 to 5. Depending on the log level you choose, all the levels below it will be ignored. In case you want to know more about log levels, please read [[this|https://guides.rubyonrails.org/debugging_rails_applications.html#log-levels]].

* Fun fact - this is why we dont simply use `puts` anymore, to make sure only the desired outputs actually appear in OpenSearch.

Some relevant information that can be extracted from here is:
1. Whatever log you chose to output for whatever use case you were testing.
2. request_uri
3. kubernetes.pod_id - this can be correlated with the errors from infra-ENV-alerts
4. kubernetes.pod_name - if the general worker is failing, look for worker_general, if the server is failing, look for frontend-nginx
4. params - not always present
5. private_ip

#### INFRA layer

Contains information about the way Kubernetes orchestrates the pods behind the scenes, upscaling and those shenanigans.

Not really relevant for devs in 99.99% of the cases.

#### WAF layer

As seen in the below photo, this category contains information about the front-line of our application architecture.

<img width="636" alt="Screenshot 2024-07-17 at 22 24 18" src="https://github.com/user-attachments/assets/5db2d951-d703-4c85-afb8-92aa4e083786">

WAF has a predefined set of regexp rules which allow / reject specific request URIs. The main reason for this is that there are a lot of bots/malicious traffic on the internet. WAF lives at the ALB level, more specifically, the requests reach WAF after going through the ALB, as WAF has full access to a decrypted request. Now, the request reaches ALB, and then WAF rejects the examples mentioned before, not allowing them to go to rest of the layers, thus increasing the stability of the system. More details about this can be found [[here|https://docs.google.com/document/d/1uQcV7qQrnq8lRa_mzoB9cP6BomstCR0UIVWWIYD2rrU/]].

The behaviour a client would see when trying to input a rule not allowed by WAF is a 403 status code in the response. In case this gets sent back to the dev team for investigation, the first thing that should be done is to identify through which of the rules (which we will talk about) did the request fail. In order to determine this, we should look at the next relevant set of information:
1. terminatingRuleId
2. terminatingRuleMatchDetails
3. terminatingRuleType

Looking at this kind of information, and looking at the WAF document should be enough to determine through which rule the request failed. From there, one should open up a discussion about whether this is an app issue, or a WAF edge case.

Some examples of terminatingRuleId values and their associated counts for the past 4 days are:

<img width="1187" alt="Screenshot 2024-07-18 at 14 54 08" src="https://github.com/user-attachments/assets/40fe71f8-44b0-47e1-ae3f-f451fb31d63e">


Let us look at an example of this (under the assumption that the request comes from a real client, not a bot):
 
https://www.golfgenius.com/test%20why%20no%20work

If you were to type this in the browser, you'd get a 403 error. Let us look in the WAF rules to see what kind of details we can gather:

<img width="1367" alt="Screenshot 2024-07-17 at 22 35 04" src="https://github.com/user-attachments/assets/2892516d-f298-4afa-b2cf-5dc58f13f29f">

Looking at the RuleId, we can see `Default_Action`. This means that:
1. the request went through all the rejections, and passed them
2. the request went through all the 'approval' rules, and did not match any of them, and therefore it was rejected.

The reason for the rejection is the existence of the symbol % used in the %20 syntax, symbolising a blank space.

The rejection is valid, as that is not an actual route in the application.

Let us now look at another example, that is functional this time around:

https://www.golfgenius.com/ggid/test%20why%20no%20work

If you were to do copy that in the browser, you'd get a status code of 200 (disregard the fact that the ggid is random).

You wouldn't see any log of this in WAF, the reason being that is was allowed to go through. The reason it was allowed to go through is that it matches one of the regexp expressions we were talking about before: `^/[a-zA-Z0-9_-]+/.*` - it starts with all letters (ggid), and then is continued with whatever symbols we want.



### How to search?

1. Select the category you'd like to search in:

<img width="331" alt="Screenshot 2024-07-17 at 22 41 01" src="https://github.com/user-attachments/assets/c600bb50-d8fe-4f01-8bfd-2e26a560352a">

2. Add the specific fields you want to look for (if you want to reduce the noise, you can also just look at the whole thing)

<img width="336" alt="Screenshot 2024-07-17 at 22 42 56" src="https://github.com/user-attachments/assets/a3e81153-0daa-44c3-bc6d-1aecd69b6595">

3. Add filters, set the date, and search for whatever you're looking for 

#### When searching, if you want exact matching, you have to add everything between double quotes.

<img width="1371" alt="Screenshot 2024-07-17 at 22 43 36" src="https://github.com/user-attachments/assets/999028aa-2b56-4ebd-be8a-ad2a8cae8891">

