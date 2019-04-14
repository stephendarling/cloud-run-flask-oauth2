# OAuth2 Authentication with Cloud Run
This sample project creates an authenticated Flask API service for Cloud Run on GCP and demonstrates
how to access it securely via an OAuth2 access token. This project uses Python 3, but the REST concepts can be applied to any other language/framework supporting HTTP REST requests. 

The process we're demonstrating here is the ability for a service account to authenticate to the Cloud Run endpoint via a `service_account.json` file. In a production system this should not be stored locally, but for simplicity sake you'll want to have a local copy of the proper service account's credential json file (e.g. the one downloaded from the GCP console).

**NOTE** The below steps are assumed to be performed on a machine running the gcloud CLI with the following roles:
* Cloud Run Admin
* Storage Admin

# Install local dependencies
```sh
# Install pip requirements
pip3 install -r requirements.txt
# Update gcloud to include Beta Cloud Run commands
gcloud components update
```

## Set initial variables
We'll use a few local variables in our steps below. This will make the below steps cut-and-paste:
```sh
# Project Id of the GCP project you'll be using this with
export PROJECT_ID=<your-gcp-project-id>
# What you want to name the service (e.g. cloud-run-flask-oauth2)
export SERVICE_NAME=<name-you-want-to-give-your-service>
# Relative path of your service account credentials file
export CREDS=<relative-path-of-credential-file>
# Service account email address that will have access to this resource
export SERVICE_ACCOUNT_EMAIL=<your-service-account-email-address>
```

## Build the service
Send the current project to Google Cloud Build, builds the container image against the `Dockerfile` and tags it with `$PROJECT_ID/$SERVICE_NAME`:
```sh
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
```

## Create the service
Create the service on Cloud Run from the tagged image that was pushed to GCR in the previous step:
```sh
gcloud beta run deploy $SERVICE_NAME --image gcr.io/$PROJECT_ID/$SERVICE_NAME --region us-central1 --quiet
```

## Get service URL
This value was printed to the command prompt after the previous step, but in case you missed it, we're looking for the `status['address']['hostname']` value from this new service:
```sh
gcloud beta run services describe $SERVICE_NAME --region us-central1
```
**NOTE** This should look something like `https://<my-service-name>-<random-characters>.a.run.app`

## Grant service account invoke access to the new service
At the time of authoring the below `gcloud` command was throwing an internal error. If this doesn't work:
```sh
gcloud beta run services add-iam-policy-binding $SERVICE_NAME \
    --member $SERVICE_ACCOUNT_EMAIL \
    --role="roles/run.invoker" \
    --region="us-central1"
```
Do this:
* Log into the Cloud Run console
* Click the checkmark next to this service in the console until the permissions pane appears on the right
* Click the "ADD MEMBER" button
* Enter your service account email address
* Add the role "Cloud Run/Invoker"

## Set local variable for service URL
Now that the service has been created, we'll set this as an environment variable to keep this code portable:
```sh
export CLOUD_RUN_SERVICE_URL=<my-service-url-from-previous-step>
```

## Run the sample request
At this point you should be all set to run the `sample_request.py` file:
```sh
python3 sample_request.py
```
If all worked, you should see something like this as a resonse in your terminal:
```json
{
  "status_code": 200,
  "response": {
    "message": "Hello World from authenticated Cloud Run!"
  }
}
```
If you saw this response, congratulations! You've been able to authenticate to your Cloud Run service. Please feel free to adapt the code in `utilities.py` to suit your needs when authenticating via OAuth2 from a non-gcp resource. 

## Additional resources
I put this project together tying information from the resources below. Please refer to them for any gaps I may have missed:
* [Official documentation](https://cloud.google.com/run/)
* [Cloud Run gcloud reference](https://cloud.google.com/sdk/gcloud/reference/beta/run/)
* [Google Identity - Generating JWTs](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#jwt-auth)
* [Google OpenID Connect](https://developers.google.com/identity/protocols/OpenIDConnect)