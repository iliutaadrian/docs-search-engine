# ClubEssential Integration Setup
To demonstrate how a Golf Genius event can be tied up to a Clubessential event to push pairings, the following accounts will be used:
* Golf Genius account: http://localhost:3000/admin/customers/13465 
* Clubessential account: http://support.grandkeyclub.com
> * username: dha22
> * password: DHAsandbox2022!

## Configuration
### On the Clubessential side
1. Access the Clubessential account URL and log in using the above credentials.

2. In the top menu, navigate to _**Golf > Tee Times Admin Dashboard**_:
<img width="1724" alt="Screenshot 2022-11-21 at 21 17 28" src="https://user-images.githubusercontent.com/93977970/203140718-ee1688b3-38f9-4769-bf78-c589b25d503b.png">
Then click on the 'Special Events' button and then choose the 'Add Event' option to create a special event:
<img width="1572" alt="Screenshot 2022-11-21 at 21 19 41" src="https://user-images.githubusercontent.com/93977970/203141444-5ded5b09-f262-429b-b9d4-c0442931efeb.png">
<img width="1728" alt="Screenshot 2022-11-28 at 13 36 34" src="https://user-images.githubusercontent.com/93977970/204268453-8613a6ac-1888-4c13-b890-170d2f443c4c.png">
The minimum required settings needed for creating the CE event are depicted in the below image:
<img width="1568" alt="Screenshot 2022-11-21 at 21 44 05" src="https://user-images.githubusercontent.com/93977970/203144931-9082b08d-a1d8-4ec8-abca-6cbdf2a408ba.png">

### On the Golf Genius side:
1. Go to http://localhost:3000/customers/13465/integrations, complete the following three fields using the CE credentials and click save:
<img width="1728" alt="Screenshot 2022-11-21 at 21 06 30" src="https://user-images.githubusercontent.com/93977970/203138846-066104cd-b0ba-4c67-a797-e319ee7a4af6.png">

2. Create an event. 
Set the name of the event. *Note that it should carry the same name as on Clubessential.
<img width="1571" alt="Screenshot 2022-11-21 at 21 47 06" src="https://user-images.githubusercontent.com/93977970/203145360-46df4f75-834d-4e90-8b5d-f3871f126bd8.png">
Import/enter details for around 8 players (2 pairings of 4 players). 
<img width="1576" alt="Screenshot 2022-11-21 at 21 51 08" src="https://user-images.githubusercontent.com/93977970/203146094-cf292769-ec04-430c-8342-81a93ded0b35.png">
Set the date of the event. *Note that it should be on the same date as on Clubessential.
<img width="1574" alt="Screenshot 2022-11-21 at 22 19 42" src="https://user-images.githubusercontent.com/93977970/203150932-6fd746fc-a1f4-4498-87eb-28b77c1f8c9e.png">
Create a course. *Note that it should carry the same name as on Clubessential.
<img width="1575" alt="Screenshot 2022-11-21 at 22 00 22" src="https://user-images.githubusercontent.com/93977970/203147600-4c7e789e-2dfb-43ef-a2e0-150227036357.png">
After clicking save, search for the course again in the list of courses. Select edit and map the course to the same course set for the CE event. Then click save again:
<img width="1574" alt="Screenshot 2022-11-21 at 22 03 45" src="https://user-images.githubusercontent.com/93977970/203148185-4bcf054a-d8e7-426f-85e2-e9979e5e49f9.png">

3. In the created event navigate to **_Calendar > Connect Round to Clubesential Calendar_** and connect the round to the CE event. Then click save:
<img width="1572" alt="Screenshot 2022-11-21 at 22 08 48" src="https://user-images.githubusercontent.com/93977970/203149354-5295fecf-0dca-4bb4-8b73-6321b2b19770.png">
<img width="1571" alt="Screenshot 2022-11-21 at 22 14 20" src="https://user-images.githubusercontent.com/93977970/203149965-2051c6ac-154e-4d4e-a307-b26af87e50b1.png">

## Pushing the pairings
On the GG side, create the pairings and set the necessary tees and courses (the course selected should be the newly created one), then push the pairings to Clubessential from the rounds menu. The result can be verified in Clubessential by navigating again to _**Golf > Tee Times Admin Dashboard**_ and selecting the date of the event in the calendar. 
 
