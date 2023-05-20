## SECTION 1 : APOLLO
## Alerts on Potential Pandemic Outbreaks in Singapore

<img src="Miscellaneous\ApolloApp.jpg"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY 
Singapore is a small and open country with a high population density, at 7,688 persons per sq km in 2022, according to the Department of Statistics Singapore (Department of Statistics, 2023). In addition, before the implementation of border restrictions due to COVID-19, Singapore had cleared 217 million travellers through its checkpoints in 2019 (Immigration and Checkpoints Authority, 2020). This makes Singapore highly susceptible to disease transmissions whenever a global pandemic outbreak occurs. 

Studies have indicated that social distancing measures and border restrictions are effective intervention methods to prevent the spread of infectious disease, such as COVID-19 (Haug et al., 2020). Considering the adverse effects of infectious diseases to a nation’s economy (Gallup, 2020) and quality of life (Mouratidis, 2021), it is critical for Singapore to ensure that there are sufficient infection control and prevention measures to protect the safety and well-being of the nation. 

While there are platforms, such as HealthMap (Clark et al. 2008), that monitor the outbreak of diseases via press releases globally, they are usually not catered specifically to Singapore’s context. Thus, relying on such platforms usually requires a lot of manpower to look through all news articles to sieve out information that are relevant to Singapore. 

As such, with reference to the adverse effects of the recent COVID-19 pandemic and the previous SARS outbreak on Singapore, there is a necessity to develop an intelligent system to monitor high risk disease outbreaks in countries that are likely to impact Singapore significantly. In addition, similar functions of this intelligent system may also be extended for use by other countries, or extended to other topics that concern Singapore’s national security.


---

## SECTION 3 : PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Ng Bo Yan | A0160005B | System Architecture, Information Extraction, Machine Learning Modelling | e0052887@nus.edu.sg |
| Low Pei Jing | A0131313B | Topic Classification, Web scraping, Business Analyst (Label data & interview) | e1111871@u.nus.edu |
| Nur Insyirah Binte Mahzan | A0115982Y | NER Modelling, Knowledge Scraping, Front-end Development | E1112628@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[![Apollo Business Case & Demo](http://img.youtube.com/vi/GVTjBN4OXPE/0.jpg)](https://youtu.be/GVTjBN4OXPE "Apollo Business Case & Demo")

[![Apollo System Design](http://img.youtube.com/vi/KDVBMAMmQi4/0.jpg)](https://youtu.be/KDVBMAMmQi4 "Apollo System Design")

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`


### 1.1 Install Dependencies

1. This is designed using python 3.8, using other version may not work
2. Go to SystemCode Folder
        
        cd SystemCode

3. Install packages
    
        python -m pip install -r requirements.txt

4. Install Spacy package

        python -m spacy download en_core_web_sm

### 1.2 Running Backend (Article & Feature Extraction)

Backend Script is called *MainBackEndProcessing.py*. Run this script to start. Offline mode is available as the tool rely on google news to query news article, and user will get blocked if too many query within short period of time.

 - Run test mode (test dataset used to develop the tool) 
   Note: Test mode will not write data to db

        python MainBackEndProcessing.py -M test
 
 - Run production mode (live, using today article). Use -D to run on specific day of articles

        python MainBackEndProcessing.py -M prod
        # TO run on specific day
        python MainBackEndProcessing.py -M prod -D 2023-04-11


 - Run demo mode (using 11 April 2023 dataset)
    - Online Mode 

            python MainBackEndProcessing.py -M prod 

    - Offline Mode

            python MainBackEndProcessing.py -M prod -O

The final output is input into database under folder "SystemCode\KnowledgeBase\ApolloDM.db" and its snapshot is located at "\output" 
In production system, production mode will be run daily using cron job to populate daily data

### 1.3 Starting the Web Application

Run *app.py* script


        python app.py

Web is served on http://127.0.0.1:8050/



---
## SECTION 6 : PROJECT REPORT 

`Refer to project report at Github Folder: ProjectReport`


---


## SECTION 7 : Miscellaneous

1. ASEANStatsData.csv - Data used to populate travellors network graph