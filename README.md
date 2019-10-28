# bugzilla-reports-tool

This tool will allow you to create a Quality dashboard for your product and send (weekly or whenever you want) reports with bug status.
The quality dashboard is fully automated and the template Google Spreadsheet can be found here - https://docs.google.com/spreadsheets/d/1Y0m8XHuqXZsI7-QwHWxUBpJv6URq2yf3AMUmNR3WON4/edit?usp=sharing

## Quality dashboard
An exeample of this dashboard:

![alt text](https://github.com/RazTamir/bugzilla-reports-tool/blob/master/pics/Screenshot%20from%202019-09-16%2017-07-19.png)

### Usage:

1. Copy this template and add your team name in the titie --> <"YOUR TEAM NAME"> QE - Quality Dashboard

2. To enable interaction with Google spreadsheet, follow the steps in https://developers.google.com/sheets/api/quickstart/python and after steps in here https://gspread.readthedocs.io/en/latest/oauth2.html#oauth-credentials (until step 6). 
Name the Json from step 3 as 'google_api_secret.json'
3. Creeate .gapi directory under root with: $ mkdir /root/.gapi
5. place the google_api_secret.json under ~/.gapi/google_api_secret.json
6. Ensure you give 'Edit' permissions in your copied spreadsheet, to the 'client' in this json file
7. install the following on the machine that will execute the script:
   - gspread (pip install gspread) from https://github.com/burnash/gspread 
   - python-bugzilla (pip install python-bugzilla) from https://github.com/python-bugzilla/python-bugzilla 
   - oauth2client (pip install oauth2client) from https://github.com/googleapis/oauth2client
8. Under config.py you have few lines that needs your attention to be specific to your product - please follow the guidelines in comments under config.py
9. Under personal_config.py add your relevant information so the tool will be able to access
10. Execute with: $ python release_readiness_criteria.py

## QE Tracking dashboard
An exeample of this dashboard:

![alt text](https://github.com/RazTamir/bugzilla-reports-tool/blob/master/pics/Screenshot%20from%202019-10-28%2012-46-50.png)
### Usage:
Same steps as above whith changing the script you execute in step 8 to tracking_dashboard.py


## Bugzilla reports
TODO

