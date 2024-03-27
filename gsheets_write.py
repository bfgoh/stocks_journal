import gspread 
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as OAuthCredentials
import pandas as pd 
import configparser

class GspreadWriter:
    def __init__(self) -> None:
        self.config = self.read_config()
        
    def read_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config = config["GSPREAD"]
        return config 

    def authenticate_gspread(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = OAuthCredentials.from_authorized_user_file(filename=self.config["gcloud_auth_path"])
        gc = gspread.authorize(credentials)
        return gc



    def select_respective_gsheet(self):
        google_sheet = self.gspread_client.open_by_url(self.config["gsheet_url"]) 
        self.entry_sheet =  google_sheet.worksheet(self.config["entry_sheet"])
        
if __name__ == "__main__":
    g  = GspreadWriter() 