from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        q="name = 'praqma.customers'",
        pageSize=100, fields="nextPageToken, files(id, mimeType, name, parents, permissions)").execute()
    items = results.get('files', [])

    base_permissions = []
    for base_permission in items[0]['permissions']:
        base_permissions.append(base_permission['displayName'])
    
    for permission in sorted(base_permissions):
        print(" - {0}".format(permission))

    results = service.files().list(
        q="'0BwzcaooBNQZQMXJXcjk1dzhJdUE' in parents",
        pageSize=1000, fields="nextPageToken, files(id, mimeType, name, parents, permissions)").execute()
    items = results.get('files', [])

    if not items:
        print('No folders found.')
    else:
        files_with_extra_permissions = []
        
        for item in items:
            fileitem = {
                'id': item['id'],
                'name': item['name'],
                'filetype': item['mimeType'],
                'otherPermissions': []
            }
            for permission in item['permissions']:
                if permission['displayName'] not in base_permissions:
                    otherPermission = {
                        'type': permission['type'],
                        'displayname': permission['displayName']
                    }
                    fileitem['otherPermissions'].append(otherPermission)
            if fileitem['otherPermissions']:
                files_with_extra_permissions.append(fileitem)

        print('Files with unique permissions:')
        for item in files_with_extra_permissions:
            print("File: {0} ({1})".format(item['name'], item['filetype']))
            for permission in item['otherPermissions']:
                print(" - {0}".format(permission['displayname']))
    

if __name__ == '__main__':
    main()