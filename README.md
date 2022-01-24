# Publicity Bot

<img src="https://img.shields.io/badge/python-v3-blue" alt="python-v3-blue">

While the management of special issues, workshop and conferences becomes more complex, automatic tools come to the rescue. This project includes a simple command line program to send email via Google. Suggestions and bug reports are always welcome. If you have any question, request or suggestion, please open a new ticket in the Issues with appropriate label.

## How to build it
Download latest release [here]() and make up the virtual environment.

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to use it
The application strongly requires a list of recipients, the email subject and the body. The list of carbon copy recipients is instead optional. These parameters must be stored within independent files as follow.

<p align="center">
  <img src="docs/emails-to-sample.png">
  <br>
  <em>Example of emails to</em>
  <br> <br>
  <img src="docs/emails-body-sample.png">
  <br>
  <em>Example of emails body</em>
</p>

Run then the application as follow.

```bash
python main.py \
    --host smtp.gmail.com \
    --port 465 \
    --from user@example.com \
    --to <PATH/OF/TO-FILE> \
    --cc <PATH/OF/CC-FILE> \
    --subject <PATH/OF/SUBJECT-FILE> \
    --body <PATH/OF/BODY-FILE>
```