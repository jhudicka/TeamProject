# Faceit CS2 Match Statistic Project
### Team members: Joey Hudicka and Ronald Liu Jr

## Project Overview
Our project idea is to create a per-user Counter-Strike 2 analysis tool that takes the input of a user’s SteamID and outputs a comprehensive analysis of their last 10 matches. The user would be able to see an overview of how their last 10 matches went – from what their most played map was, to what their most used weapon was, to their average headshot percentage. From there, users would be able to analyze a particular game and see the stats of themselves. Looking at match data within the Faceit app can be difficult at times - with long loading times and statistics being buried at the bottom of each user's profile - this project is meant to make the process at looking at your previous matches faster and easier!

## Home Page
![home page](/faceit/page1.png)
### How it works:
Our home page is designed to be a form where a user can search Faceit for any username they would like. The username that is typed into the field is then passed onto another page (/nicknames) where that username is used as a variable to search for all the players on Faceit that use that, or a similiar, nickname.


## Select a Player
![player select](/faceit/page2.png)
### How it works:
Using the Faceit API, we were able to request '/search/players' which would return a dictionary of all the players on Faceit that use that nickname, or a similar one. For each player, the dictionary would return the player's ID, the games they are registered on Faceit for, their skill level for each game, their avatar, region and more. We decided to have this page display each player's username and Player ID because on Faceit, your username is unique - no two players can have the same username. At the bottom of the page, there is a dropdown menu where you can select the player you want to analyze, or, you can click the 'Go Back' button to return to the home screen to search for another player. This could be useful if you've mispelled the player's username. Once the user has selected a username to analyze, it will then pass that information to the (/stats) page.

## Detailed Breakdown of Last 10 Matches
![match breakdown](/faceit/page3.png)
### How it works:
Using the Player_ID passed from the previous page, we were able to request 'players/{player_id}/games/cs2/stats' from the Faceit API which would return a dictionary of the stats of all the recent matches the player has played. We set the limit of matches to display to be 10. On this page, you can see the date the match was played, what map was played, the score of the match, along with detailed personalized statistics from the game as well. This can be helpful when you are about to play a Faceit match and you want to play a map that the other team is not comfortable on. By searching each player's name in our Faceit Helper app, you'll be able to see their statistics for their last 10 matches, what maps they do not perform the best on, and you can use that information to win more games!
