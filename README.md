# kniebeugen-folter
_mehr kniebeugen folter!_

# WtF?
A little selenium script (python3) for automated kniebeugen folter (google translate ftw...).

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

    Run `docker-compose run --service-ports kniebeugen_folter:latest <args here>` instead of good-ole `docker-compose up
    `

# Notes
- There are a bunch of edge cases I don't feel like testing (and general things), like:
    - What happens when you fuck up the `--token-limit` and go broke
    - What happens when you're banned by a mod because you're being a dick with this script, or just a dick in general
    - If there should be cli options for various timeouts, i.e. when the chat/tip/etc won't connect
    - A useful part for the uuid_str to play, just have a nudging feeling that NOT having a uuid for each run is a bad 
    idea...
    - What to do when you pass stupid values for the cli options, i.e. bad browser, unreachable selenium grid hub, etc
    - Lot's of others I haven't thought of yet, and don't really want to 