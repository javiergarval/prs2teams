# Webhook Handler for Bitbucket and Microsoft Teams

This project is a Flask server that listens for webhooks from Bitbucket Cloud and sends notifications to Microsoft Teams
when a new pull request is created.

## Requirements

Python 3.6 or higher

Flask

Requests

Environment Setup

## Clone the repository

```bash
git clone git@github.com:javiergarval/prs2teams.git
cd prs2teams
```

## Install dependencies

Ensure you have Python and pip installed, then execute:

```bash
pip install Flask requests
```

## Supervisor Configuration

To ensure that the Flask server runs continuously and restarts in case of failures, we use Supervisor.

#### Install Supervisor

```bash
sudo apt-get install supervisor
```

### Create a configuration file for Supervisor

Save the following content in /etc/supervisor/conf.d/prs2teams.conf:

```makefile
[program:prs2teams]
command=python /path/app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/prs2teams.err.log
stdout_logfile=/var/log/prs2teams.out.log
environment=PYTHONUNBUFFERED=1
user=user
```

Make sure to replace /path/to/your/project/app.py with the actual path to your app.py file and username with your
username in the system.

### Reload and manage Supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start prs2teams
```

## Running the Server

The Flask server is already configured to run via Supervisor. If you need to run it manually for testing, you can do so
with:

```bash
python app.py
```

## Endpoint

The Flask server is set to listen on port 4000 and only accept POST requests at the endpoint:

```
http://<your-IP-address-or-domain>:4000/webhooks/pull-requests/create
```