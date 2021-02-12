## Agence Stark
_______________________________________________________

#### Collaborateurs : 

  - A Constant (https://github.com/AmosConstantjunior)
  - B Anthony (https://github.com/AnthonyBonfils3)
  - B Myriam (https://github.com/MyriamBou)
  - M Jean-Pierre (https://github.com/jpphi)
  - P Olivier (https://github.com/Olivier-Prince)
  - R Ludovic (https://github.com/Ludo-R)

_______________________________________________________
  
### How to use :

Clone the repositary with :

	git clone https://github.com/Ludo-R/brief-AGILE-chatBot

Actually you can use create_DB.py to add a dataset to MongoDB but it only work with Stackexchange dataset :

https://archive.org/download/stackexchange

If you want add another dataset from everywhere, you need to edit the target of query (actually "Title") and some other thing.

(This step specify you need to know install MongoDB)
More information here : https://docs.mongodb.com/manual/installation/

### Step 2-- Create bot

Create you'r Own BOT on https://discord.com/developers/applications
Select -> New Applications
Pick a name and select Create

Go in "Bot" Section and select : Add bot

Go in OAuth2 Section select "Bot" in the second columns, and below select Permission you want to give on you'r bot.

After copy the link appear 

And past it, select you'r server where you are Admin,and select GO

### Step 3-- Connect bot

Go back on https://discord.com/developers/applications
In "Bot" Section COPY the "Token"

Open stark.py

Past your token on the last line in :

	client.run('PAST YOUR TOKEN')

Run the apy

### ENJOY You'r new friend is Ready
 
