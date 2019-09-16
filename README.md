# bugzilla-reports-tool

This tool will allow you to create a Quality dashboard for your product.
An exeample of this dashboard:

![alt text](https://github.com/RazTamir/bugzilla-reports-tool/blob/master/Screenshot%20from%202019-09-16%2017-07-19.png)

## Usage:
The quality dashboard is fully automated and the template Google Spreadsheet can be found here - https://docs.google.com/spreadsheets/d/1h62gN1fINImncOmLCVVTSVZJOrtjdLqik8gSTdVNYJw/edit?usp=sharing

1. Copy this template and add your team name in the titie --> <"YOUR TEAM NAME"> QE - Quality Dashboard

2. To enable interaction with Google spreadsheet, follow the steps in https://developers.google.com/sheets/api/quickstart/python
3. Please the google_api_secret.json under ~/.gapi/google_api_secret.json
4. Ensure you give 'Edit' permissions to the 'client' in this json file
5. install gspread (pip install gspread) from https://github.com/burnash/gspread on the machine that will execute the script
6. Under config.py you have few lines that needs your attention to be specific to your product - please follow the guidelines in comments under config.py



