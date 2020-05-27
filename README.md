# TicTacToe Bot in Telegram
This bot plays tictactoe in telegram. The code contained... is HIGHLY INEFFICIENT, PEP violater, repeated code. ~~and worst of all... USES GLOBAL VARIABLES THROUGHOUT THE PROGRAM.~~ (im in highschool) \
I fixed the global variable thingy.


----------------------------------------------


[TicTacToe-Telegram](https://github.com/RoguedBear/TicTacToeBot/blob/master/TicTacToe-Telegram.py) is the final version of this bot which is hopefully, bug-free. \
The only bug (or I'd rather say, a 'feature') that exists is, when you spam board move numbers together, instead of rejecting the extra moves, the bot proccesses them as if the moves were in a queue. \

Oh, and if 1+ people are using the bot simultaneously, a "lag" could be expected since the each user's requests are stored in a queue (as far as i can tell) and my program takes time to process (actually, takes time to send ~~heaps of~~ messages to) each user's move/data. 





<code>MY_CHAT_ID</code> is supposed to be the chat id where logging messages are recieved. \
<code>token</code> is removed in the github version, fill it with your own
