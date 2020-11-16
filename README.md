
# Chen Bot

### About
This bot tries to emulate the way a certain user behaves on discord. The 355M gpt-2 model was retrained to predict the user's next message based on previous messages sent in a group chat. The bot is an interface between the trained gpt-2 model and discord.

### Installation (but why)
*Please note that python versions above 3.7 will **not** work due to the lack of support from tensorflow 1.15.2. It is therefore recommended to run all code in a virtual environment*

All dependencies are installed through `pip install -r requirements.txt`

The current model being used on my production version of the bot can be downloaded through this google drive link. 
Update: Please train your own model. I am currently working on better models.

Training your own model is trivial. Matt Woolf offers [this google collab](https://colab.research.google.com/drive/1qxcQ2A1nNjFudAGN_mcMOnvV9sF_PkEb) to retrain the gpt-2 model on your own data: 

Specific configurations for the discord bot can be found in the config.py file which are the hello command's output, the starting conversation loaded into the model (convo), the discord token for the bot and the admin ids.
