squat-machine
-----------------

# Disclaimer
- This has not been marginally tested
- This was initially put together between 0000 and 0200 on a sunday night, after about 4 hours of sleep
- The docker stuff is untested, but using the env vars via ConfigArgsParse should make it function a bit easier. You'll 
probably need to update [docker-compose.yaml](./docker-compose.yaml)

# WtF?
A little selenium script (python3) for automated tipping on an interval.

# Requirements:
- Python3
- Selenium Server: [project page](https://docs.seleniumhq.org/download/)
- ChromeDriver: [project page](https://sites.google.com/a/chromium.org/chromedriver/getting-started)
- (Optionally) Docker and DockerCompose

# Build the docker image
- `chmod +x ./build.sh`
- `./build.sh`

# Setup
- `python 3 -m venv venv`
- `source ./venv/bin/activate`
- `pip install wheel`
- `pip install -r requirements`

# Running
- `python3 app.py --help`
- `enjoy`

# FAQ
- Q: Why should I use my username/password? How do I know you're not stealing it?
    
    read the source
    
- Q: What are the CLI options?
    
    `python3 app.py --help`

- Q: Really? An entire ubuntu 16 image for the dockerfile?
    
    Yep, deal with it.
    
- Q: How do I pass the needed cli options to the app when using docker-compose?

    Use the env var overrides
    
- Q: What is this for?

    Figure it out, it's right there IN THE SOURCE. :)

# Notes
- There are a bunch of edge cases I don't feel like testing (and general things), like:
    - What happens when you fuck up the `--token-limit` and go broke
    - What happens when you're banned by a mod because you're being a dick with this script, or just a dick in general
    - If there should be cli options for various timeouts, i.e. when the chat/tip/etc won't connect
    - A useful part for the uuid_str to play, just have a nudging feeling that NOT having a uuid for each run is a bad 
    idea...
    - What to do when you pass stupid values for the cli options, i.e. bad browser, unreachable selenium grid hub, etc
    - What to do if the host is offline. See the note about the Hammer of Ban
    - Lot's of others I haven't thought of yet, and don't really want to 