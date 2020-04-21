# List permissions for Praqma.io gdrive

Based on the Google API [Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python). Follow the guide to get a credentials.json file. The run the python script with
```
python3 list_permissions.py
```
This will open a browser and start the OAuth2 login process. Log in using your praqma.io account and approve the permissions needed by the script. This step will generate a `token.pickle` file.

To reset your access to the Google API on praqma.io, just delete the `token.pickle` file.

NOTE: Never commit your credentials.json or token.pickle files. They have been added to .gitignore for your convenience, but contain secrets, that should never be committed!