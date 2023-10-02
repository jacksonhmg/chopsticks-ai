# chopsticks-ai
I built an AI to play chopsticks online. I knew nothing about a lot of the things in here before I started. I'll break down the project progression and the parts that make this project.

What's contained in this project:
- Q-learning algorithm using Temporal Difference learning
- OpenAI's Gym infrastructure to help train the model
- Flask and Connexion to link my Python model backend with my JavaScript frontend
- (Old original version): Pygame to play against the model locally
- A few other things but those are the main

The progression of this project:
- Originally just wanted to make the most simple AI I could, to play against
- Just started with figuring out how to represent player vs player
- Figured out Pygame and how to render
- Started implementing OpenAI's Gym infrastructure with custom chopstick agent
- Then spent a lot of time implementing AI vs AI
  - Ran into many usual machine learning problems: E.g. only solving for local optimal policy
- Spent A LOT OF TIME addressing that ^
- Eventually decided it would be better to train it a bit myself (player vs AI) but that also I wanted to play against it anyway
- Now, two AI's train against a random agent, train against each other, then train against me

- THEN, I DECIDED FUCK IT. Let's just take the current terrible model and its weights, upload it onto the web, and let any actual person train it by playing against it.
- So that's what I did :)
- Implemented Flask and Connexion to set up connection between python backend and javascript frontend
- Got everything working nice and smoothly
- Deployed on Heroku :)

So there! That's how I implemented a shitty Chopstick Q-learning agent and made it public to play against
