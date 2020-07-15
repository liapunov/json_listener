# json_listener
An idea for a "free" API2API web app that takes registrants from a form and register them on other applications.

## purpose and scope
The idea is to be able to connect different applications in use in a SOHO environment (like the one I am working in) without the necessity to pay for services like Zapier or similar.
The project has a simple structure:
- A web application listens to one or more services through JSON webhook. The web app can be registered on a cloud service such as GCP
- as soon as a meaningful packet arrives, the web server transform the incoming JSON in a common form dictionary, then calls the appropriate translators to prepare the JSON files that need to be dispatched
- finally, the web application signs in and uses the API of the registered services.

## status
At of May 5, the only services that this application serves are CognitoForms - on the input side - and Zoom webinar, on the output side.
This allows a paying registrant for an event to also be automatically registered on the appropriate zoom webinar.
The zoom webinar has an identifier that needs to be inserted in the Cognito Forms.
## To Do Next
- The registration should allow for multiple registrants on a single form.
- Integration with Google sheets, as the repository for all of our event attendants is there
- More robust testing
- Integration with Mailchimp
