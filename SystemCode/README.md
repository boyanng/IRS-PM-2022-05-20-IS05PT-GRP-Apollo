# Apollo

TODO:  Add description for Appolo

## 1. Getting Started

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

The final output is input into database under folder "KnowledgeBase\ApolloDM.db" and its snapshot is located at "\output" 


### 1.3 Starting the Web Application

Run *app.py* script


        python app.py

Web is served on http://127.0.0.1:8050/
