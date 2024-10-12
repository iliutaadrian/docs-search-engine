Hello,

In this guide we will present a solution for enabling SSL in development. Very useful for testing production scenarios with different integrations, e.g., Golf Advisor, Golf Now,..

The desired goal is to navigate to [https://localhost:3000/](https://localhost:3000/) or [https://www.golfgenius.com/](https://www.golfgenius.com/) and be in our development environment.

Steps

1. Create your private key (any password will do, we remove it below)

      ```$ cd ~/.ssh```

      ```$ openssl genrsa -des3 -out server.orig.key 2048```

2. Remove the password
  
      ```$ openssl rsa -in server.orig.key -out server.key```

3. Generate the csr (Certificate signing request) (Details are important!)

      ```$ openssl req -new -key server.key -out server.csr```

      ### IMPORTANT
      MUST have **localhost.ssl** as the common name to keep browsers happy 

      (has to do with non internal domain names ... which sadly can be avoided with a domain name with a "." in the middle of it somewhere)

      Country Name (2 letter code) [AU]:

      ...

      Common Name: **localhost.ssl**

      ...

4. Generate self signed ssl certificate 

      ```$ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt```

5. Redirect port 443 to 3000 (This is the default setup I used, but you can redirect to what port you desire)

      ```echo "rdr pass inet proto tcp from any to any port 443 -> 127.0.0.1 port 3000" | sudo pfctl -ef -```

6. Redirect www.golfgenius.com to localhost (Optional, used if we want to call https://www.golfgenius.com)

      ```sudo vim etc/hosts/``` and add the following line ```127.0.0.1      www.golfgenius.com```

7. Start the server

      ```rvmsudo rails server -b 'ssl://127.0.0.1?key=/Users/:USRNAME/.ssh/server.key&cert=/Users/:USRNAME/.ssh/server.crt'```

      **Note:** Make sure you have the correct path to **.key** and **.crt**

8. The result

![No Image](https://user-images.githubusercontent.com/29229646/52261094-e80f5a00-2930-11e9-9227-ce9b950db403.png)


### Important
After development to stop the port redirecting (443 -> 3000), run the following command:
```sudo pfctl -F all -f /etc/pf.conf```


Refferences:
* https://gist.github.com/tadast/9932075
* https://salferrarello.com/mac-pfctl-port-forwarding/

