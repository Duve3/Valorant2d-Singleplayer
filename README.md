# Valorant2D - Singleplayer
A recreated version of V2D, designed with single player in mind.

**Disclaimer:**
This project is not ran by anyone/anything affilated with the videogame VALORANT or its creators, RIOT GAMES.
This is a fan based project which attempts to use completely original models/art.
If you would like to take this down, please contact me.

### Table of contents
- [How to run](#how-to-run)
- [Development](#development)
### How to run

Currently there is no running release version of Valorant2D - Singleplayer.
You can get "early access" by just running the raw code yourself.

### Development

This project uses python 3.11 with the following dependencies:
- pygame-ce (The actual renderer, this may be replaceable with pygame but it is unsupported)
- pygame-wrapper (A helper library to make some annoying pygame things easier)

You can either install the above dependencies or just run the following:
```cmd
pip install -r ./requirements.txt
```

The main entry point is the main.py file (in the src dir) but you may see random entry points scattered throughout for testing purposes.
