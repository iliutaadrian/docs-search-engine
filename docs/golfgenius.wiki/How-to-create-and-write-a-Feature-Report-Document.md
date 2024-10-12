This guide will cover the process of creating a new Feature Report Document and guidelines for writing it.

# Creating a new Feature Report Document
## Step 1
Get the feature's SPEC document. Usually, you will find it on Jira in the "Spec" section.

<img width="972" alt="Screenshot 2022-11-17 at 17 05 54" src="https://user-images.githubusercontent.com/11840812/202482489-80d3ea8a-6631-496b-a7fe-7391b92d1355.png">


## Step 2
Find in what Google Drive folder is the Spec saved - refer to the image below.
<img width="1792" alt="Screenshot 2022-11-17 at 17 07 34" src="https://user-images.githubusercontent.com/11840812/202482941-cb38a6fa-eac1-41d6-b5cd-d10220a65e6c.png">

## Step 3
Go to that Google Drive folder.
Note: each release cycle has a new folder under AAAA-GGS > Development > Current Specs. E.g. R6/2022 has the folder "10.TMS 2022 / R6".
<img width="1740" alt="Screenshot 2022-11-17 at 17 10 12" src="https://user-images.githubusercontent.com/11840812/202484032-8bc5b0fc-b501-4578-a34a-2c523066c85f.png">

<img width="1464" alt="Screenshot 2022-11-17 at 17 13 19" src="https://user-images.githubusercontent.com/11840812/202484283-3010e775-010d-4512-84a4-e686664bb342.png">

## Step 4
After you've made sure you're in the correct folder, click on the "New" button > "Google Docs" > "From a Template", then click on "Create and Share".
<img width="1160" alt="Screenshot 2022-11-17 at 17 15 13" src="https://user-images.githubusercontent.com/11840812/202484828-9d46cc73-6a7c-4242-81d0-93387396110b.png">

## Step 5
Select the template marked in the image below. This will create a new report document.
<img width="1290" alt="Screenshot 2022-11-17 at 17 16 50" src="https://user-images.githubusercontent.com/11840812/202485224-c9727cfb-c1b9-4ff9-80ec-bd3aed676f36.png">

## Step 6
Congrats! Now you have a new report document that was created in the folder belonging to the corect release cycle.
<img width="1313" alt="Screenshot 2022-11-17 at 17 19 45" src="https://user-images.githubusercontent.com/11840812/202485894-8f68de9b-5cfd-4446-a994-3ac59dfa7c74.png">

# Writing a Feature Report Document

## Step 1
Change the name of the document: copy the spec document's name and change "SPEC" to "REPORT".
<img width="1314" alt="Screenshot 2022-11-17 at 17 27 13" src="https://user-images.githubusercontent.com/11840812/202487649-1e548dd9-6861-4dfa-b0c2-2229b89debe3.png">

## Step 2
Update the header data: add the manager's full name and dev's full name for "Person 1" and "Person 2", and write the Month and the Year for "Date".

<img width="1317" alt="Screenshot 2022-11-17 at 17 31 54" src="https://user-images.githubusercontent.com/11840812/202488763-6ce9ab39-1fd7-44b1-b19c-ed8b585588ec.png">

## Step 3
Copy the "Requested By", "Customers Affected", and "Appendix" from the spec document.
<img width="1278" alt="Screenshot 2022-11-17 at 17 33 11" src="https://user-images.githubusercontent.com/11840812/202489087-5187b3c5-831a-46c9-817b-9ec0411c75e0.png">

## Step 4
Remove the sections "Future Work" and "Technical Details" if necessary.
<img width="1285" alt="Screenshot 2022-11-17 at 17 36 21" src="https://user-images.githubusercontent.com/11840812/202489821-08b4c0b9-ec09-4bd5-8aaf-c159d0284eca.png">

## Step 5
Change the title of the report and remove the subtitle if necessary.
<img width="1332" alt="Screenshot 2022-11-17 at 17 37 30" src="https://user-images.githubusercontent.com/11840812/202490178-61c65a93-28dd-4831-a143-9a6d44f35a18.png">

## Step 6
Write a High Level Summary (could be copied from the spec if nothing changed for the feature since the spec was written).

<img width="1283" alt="Screenshot 2022-11-17 at 17 39 33" src="https://user-images.githubusercontent.com/11840812/202490757-cc0a00da-c591-4f78-b1a8-d07b0a7eece4.png">

## Step 7
Start writing the report. 
Some guidelines here:
* walk the reader through the whole feature and include all the use-cases possible
* try not to use technical terms (e.g., Hash, gem), but if you must, provide light explanations for them
* remember the report is the "story" of the feature, so try to have a well-defined structure:
> * give some background information (e.g., why was the feature requested, by who, what we had before this feature)
> * explain what was done, where were the changes made, and provide as much details as possible (e.g., if a new page is added, mention how to get to it, if a new input is added, mention the default values and possible validations)
> * think of all the use-cases and write a section for each of them (e.g., if a new data-field is added, have a section for each composer - report, page, spreadsheet)
> * use the **past tense or present** when writing, since the report is supposedly written after the feature is implemented (in spec we talk about the future - e.g., "we WILL add a new button", and in the report we talk about the past - e.g., "we HAVE added a new button")
* include as many screenshots as possible, ideally for each paragraph you should have a screenshot
> * use real-life examples for your screenshots - steer clear of events named "Test Event", or Tournaments named "Tournament1".
> * all the screenshots should have a name (e.g., the first SS from section 4.2. should be named "_Fig.4.2.1. what_the_image_represents_")
> * the images should be centered, and have a dark gray border of 1pt, and their Fig names should be centered and in italic (refer to the screenshots below)
> * quick commands: Cmd + i (apply italic), Cmd + Shift + E (align center), Cmd + Shift + L (align to left)

* mention the impact the feature has on existing functionalities (e.g., new types of payments that should also appear in the Transaction History)
* mention the hidden conditions (e.g., if a new system report is added that is visible only for the completed rounds, then that is something that we cannot communicate to the user, and we should log it in the report)
* add a "Future Work" section if there is something that needs to be revisited in a future iteration of the feature (e.g., the current feature supports only Gross Tournaments, and in the future we might want to support Net Tournaments as well)
* add a "Technical Details" section if there anything that would be considered too technical for the normal reader (e.g., a complex algorithm that needs a breakdown, or some specific triggers for an action)
* add a "Solved Issues" section if you found any bugs while developing the feature, and describe the bug and the fix


<img width="1302" alt="Screenshot 2022-11-18 at 13 09 54" src="https://user-images.githubusercontent.com/11840812/202692354-2ad23dc8-5d30-46b9-af36-7229636a2c54.png">
<img width="669" alt="Screenshot 2022-11-18 at 13 12 35" src="https://user-images.githubusercontent.com/11840812/202692515-cfdb6bd1-bd2a-465d-b588-a059e4740eaa.png">

