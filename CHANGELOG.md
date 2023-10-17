# ChangeLog
This file will contain everything related to the changelog in the project.

format:

There's going to be big (###) date header, then smaller (####) text for the current time (PST/PDT, 12-hour format)

## Table of contents:
- [10/15/2023](#10152023)
- [10/16/2023](#10162023)

### 10/15/2023:
#### 10:20 PM:
Project created, nothing really done except some boilerplate,
next thing is just the main and disclaimer menus.
The Disclaimer menu should just contain a quick disclaimer that passes after ~3s (could change).
The main menu should just contain access to everything like level editor and game.

### 10/16/2023
#### 4:13 PM:
Changed ChangeLog.md to use 12-hour format because its better.
#### 9:22 PM:
Renamed ChangeLog.md -> CHANGELOG.md; 

Added requirements.txt (i forgot yesterday);

Added a disclaimer menu and worked on the main menu a little,
currently has some basic stuff that can be expanded on well.

Added many comments everywhere (should make it more readable? might remove some for obvious reasons)

Made the disclaimer menu skippable by pressing any button/clicking and making it fade in/fade out on start.

Really just worked on stuff to help us in the long run, one of the biggest things I am doing is naming schemes.
Everything should hopefully be named similar to this (atleast all pygame objs): TYPE_NameThing = blah blah;
This should allow for easily finding variables.
Things like ints and floats will not have names like that, because it would be too confusing/difficult to find them.

I wish I could do more but this is the most I will get done today.

Things to add:
- Actual game
  - By just going straight into coding it I should get a lot done assuming I have less hw and stuff.
  - Really the idea is just to code the player movement and the AI(? some kind of enemy probably)
  - It would also be great to code a level format so that I can create a level editor of some kind. (JSON? im not sure yet)
- Connecting game to play button
- More menu stuff
