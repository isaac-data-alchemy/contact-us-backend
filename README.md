# Contact Submission API
This API manages form submissions from the company's "Contact Us" page. It collects submissions, saves them to the database, and forwards them to the company's email for further processing.

## Features
Collects form submissions from the "Contact Us" page.
Validates form data (e.g., email, phone number).
Stores submissions in the database for future reference.
Sends submission details to the company's email upon receipt.

## Models
### ContactSubmission
This model represents a single submission from the "Contact Us" form.

#### Fields
**name**: CharField User's name. (Max: 100 characters)

**email**: EmailField User's email. This serves as a natural key and must be unique.

**subject**: CharField Subject of the message. (Max: 200 characters; optional)

**phone_number**: CharField Validated phone number. Must include country code and be between 7–15 digits.

**message**: TextField User's message or inquiry.

**submitted_at**: DateTimeField Automatically records the timestamp when the form is submitted.

# How to Use
1. Database Setup
Run the migrations to create the necessary database tables:

bash
Copy code
`python manage.py makemigrations`
`python manage.py migrate`

2. API Usage Save a Submission
Form submissions are sent as JSON payloads and saved using the ContactSubmission model. 
### Example payload:

#### json
{
  "name": "John Doe",

  "email": "john.doe@example.com",

  "subject": "Inquiry about services",

  "phone_number": "+123456789",

  "message": "Can you provide more details about your pricing?"

}

### Retrieve Submission by Natural Key
Use the email field to fetch a specific submission programmatically:

### Export Data
Use Django's dumpdata command to export data using natural keys:

bash
Copy code
`python manage.py dumpdata app_name.ContactSubmission --natural-primary --indent 2 > submissions.json`

### Import Data
#### Load data back into the Database

bash
Copy code
`python manage.py loaddata submissions.json`

# Author
### @isaac-data-alchemy
For inquiries, contact **ejimoforisaac26@gmail.com**

License
This project is licensed under the MIT License. See the LICENSE file for details.

## Notes
**Ensure the email backend is properly configured before going live.**
**Secure your email credentials in the environment variables for production. most likely this will depend on the way you are deploying your service because you could end up exporting these variables directly into the environment but do not take my word for it okay. Do your own research**
