import logging
import copy
import random
from time import sleep
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


# Global Variables:
X = '🔴' #'❌'
O = '🟢' #'♻️'
human = X
computer = O
turn = X
master_game_board = {'1': '‌1'.ljust(5), '2': '2'.center(4), '3': '3'.center(4),
              '4': '4'.center(4), '5': '5'.center(4), '6': '6'.center(4),
              '7': '7'.center(4), '8': '8'.center(4), '9': '9'.center(4)}
#game_board = copy.copy(master_game_board)
MY_CHAT_ID = removed
GAME_END = False

# ENable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def play(update, context):

    context.user_data['GAME'] = copy.copy(master_game_board)
    global chat_id
    chat_id = update.message.from_user.id
    if chat_id != MY_CHAT_ID:
        context.bot.send_message(MY_CHAT_ID,
            f"{update.effective_chat.username}/{update.effective_chat.first_name} is playing TicTacToe")
    reply_keyboard = [['Yes'],['No']]


    logger.info(f"User {update.message.from_user.first_name}, Id:{update.message.from_user.id} connected to chat")


    update.message.reply_text(
        f'Hi {update.effective_chat.first_name}! '
        'Do you want to play TicTacToe with me?\n\n'
        '(which is made by jayant <3)',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
            resize_keyboard=True),
        quote=True)
    context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)
    sleep(1)
    update.message.reply_text('PS: tap /cancel or type `quit` anytime to exit.\nAnd if something doesn\'t go right, try /help',
                parse_mode=ParseMode.MARKDOWN)


    return 'GAME_INTRO'

def game_intro(update, context):
    user = update.message.from_user
    logger.info(f"User {user.first_name} confirmed to play.")
    update.message.reply_text("Alright, let's play!")
    update.message.reply_text(
    "The rules are simple if you have played TicTacToe. "
    "Which, I must assume, you have.")
    update.message.reply_text("So, let's roll into it!.")

    context.bot.send_chat_action(update.message.chat.id, action=ChatAction.TYPING)
    sleep(1.3)
    update.message.reply_text(
        "You are playing as 🔴\n"
        "And I will play as 🟢",
        reply_markup=ReplyKeyboardMarkup(
            [['OK']],
            resize_keyboard=True
            )
        )

    return 'DISPLAY_BOARD'

def displayBoard(board):
    '''
    Prints the gameboard
    INPUT: board: takes the board data structure to print it out
    '''
    board= f"""
‌‌{board['1']} | {board['2']} | {board['3']}
-----------------
{board['4']} | {board['5']} | {board['6']}
{'-'.center(len(' 1  |  2  |  3   '), '-')}
{board['7']} | {board['8']} | {board['9']}

"""

    return board

def displayBoard_inChat(update, context, start=True):

    if start:
        update.message.reply_text('Starting Game...')
    context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)

    board = displayBoard(context.user_data['GAME'])
    update.message.reply_text(board,
        reply_markup=ReplyKeyboardMarkup([['Play My Move']],
                        resize_keyboard=True))
                        #parse_mode=ParseMode.MARKDOWN_V2)

    return 'CHECK_END_STATE'

def get_input(update, context):
    available_moves = [i if context.user_data['GAME'][i] not in [X, O] else 0 for i in context.user_data['GAME'].keys()]
    move = update.message.text
    reply_keyboard = [['1','2','3'],
                      ['4','5','6'],
                      ['7','8','9']]
    for row in range(3):
        for column in range(3):
            if reply_keyboard[row][column] not in available_moves:
                reply_keyboard[row][column] = 'X' if context.user_data['GAME'][reply_keyboard[row][column]] in X else 'O'

    update.message.reply_text(
        'What is your move?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

    return 'PLAY_MOVE'


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    update.message.reply_text('Ok, no worries!',
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Just hit me up with /play if you change your mind.')
    update.message.reply_text('Bye!')

    reset_board()
    return ConversationHandler.END

def cancel2(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    update.message.reply_text('Ok, no worries!',
                              reply_markup=ReplyKeyboardRemove())

    update.message.reply_text('Bye!')

    reset_board()
    return ConversationHandler.END

def end_game(update, context):
    '''
    logger.info("Game Ends")
    sleep(5)
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('To play again, tap /cancel and then /play.\n'
            'Ik weird bug, but ever tried finding program flow errors in a 500 line program\n'
            'First time for me, so... I can\'t figure out where the problem lies.')
    update.message.reply_text('Bye!')
    '''
    update.message.reply_text('....', reply_markup=ReplyKeyboardRemove())
    reset_board(update, context)

    pass

def end_game2(update, context):

    logger.info(f"{update.effective_chat.first_name} required more help")


    update.message.reply_text('To play again, tap /cancel and then /play.\n'
            'Ik weird bug, but ever tried finding program flow errors in a 500 line program\n'
            'First time for me, so... I can\'t figure out where the problem lies.',
             reply_markup=ReplyKeyboardRemove())





def reset_board(update, context):
    context.user_data['GAME'].clear()

def feedback(update, context):
    logger.info(f"{update.effective_chat.first_name} is sending feedback")
    update.message.reply_text("You may enter your feedback if you have one\. \n"
            'Type in `cancel` if you don\'t want to send any feedback',
             parse_mode=ParseMode.MARKDOWN_V2,
             reply_markup=ReplyKeyboardRemove())

    return 'SEND_FEEDBACK'

def send_feedback(update, context):


    context.bot.send_message(MY_CHAT_ID,
        f"#Feedback from: {update.effective_chat.first_name} @{update.effective_chat.username}\n`{update.message.text}`",
        parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('Feedback sent!')

    return ConversationHandler.END

def error(update, context):
    logger.info('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("An Error Occured. Please inform my creator or try restarting the game by tapping /cancel and then /play")

def need_help(update, context):
    update.message.reply_text('Side Note from dev:  There is a low probability, but... if you notice your gameboard not responding or sending lost/tie messages early or not able to play... that means someone else is also using the playing.\n'
                "Either wait, message me (through feedback? your choice) or send bounty hunters to terminate the mobile phones of whoever is using this bot. Trust me, Bountry hunters option is better.\n\n"
                "Why is this happening you ask? Well because i violated the rule of programming that NEVER USE GLOBAL VARIABLES <s>(and python-telegram docs have a steep learning curve)</s>.\n\n"
                "Try /cannot_play_again if that is your problem",
                parse_mode=ParseMode.HTML )
# -------------CORE GAME FUNCTIONS-----------
# Checks the winning conditions function
def hasWon(game_board):
    '''
    Checks if the game board is in a winning state
    INPUT: the game board
    OUTPUT: winning Player
    '''

    # Check horizontals.
    # Column 1
    if game_board['1'] == game_board['4'] == game_board['7'] and game_board['1'] in [X, O]:
        return game_board['1']
    # Column 2
    if game_board['2'] == game_board['5'] == game_board['8'] and game_board['2'] in [X, O]:
        return game_board['2']
    # Column 3
    if game_board['3'] == game_board['6'] == game_board['9'] and game_board['3'] in [X, O]:
        return game_board['3']

    # Check verticals
    # Row 1
    if game_board['1'] == game_board['2'] == game_board['3'] and game_board['1'] in [X, O]:
        return game_board['1']
    # Row 2
    if game_board['4'] == game_board['5'] == game_board['6'] and game_board['4'] in [X, O]:
        return game_board['4']
    # Row 3
    if game_board['7'] == game_board['8'] == game_board['9'] and game_board['7'] in [X, O]:
        return game_board['7']

    # Check Diagonals
    # D1
    if game_board['1'] == game_board['5'] == game_board['9'] and game_board['1'] in [X, O]:
        return game_board['1']
    # D2
    if game_board['7'] == game_board['5'] == game_board['3'] and game_board['2'] in [X, O]:
        return game_board['7']
    else:
        return None

# Has won's handler:
def hasWon_handler(update, context, tie=False):
    chat_id_local = update.message.chat.id
    match_state = hasWon(context.user_data['GAME'])

    if match_state is not None:
        update.message.reply_text("🥁🥁🥁🥁🥁🥁🥁🥁")
        sleep(1.2)
    for i in context.user_data['GAME'].values():
        if i not in [X, O]:
            break
    else:
        tie = True

    if tie:
        logger.info(f"{update.effective_chat.first_name} ties")
        if chat_id != MY_CHAT_ID:
            context.bot.send_message(MY_CHAT_ID,
                f"{update.effective_chat.username}/{update.effective_chat.first_name} has tied")

        update.message.reply_text("It's a tie!", reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(f"Well played {update.effective_chat.first_name}!")
        context.bot.send_chat_action(chat_id_local, action=ChatAction.TYPING)
        sleep(random.random()*1.5)
        update.message.reply_text("But I'm blood thirsty for another round.")
        context.bot.send_chat_action(chat_id_local, action=ChatAction.TYPING)
        sleep(1.2)
        update.message.reply_text("UNTIL I BEAT YOU☠👺")
        random_sticker_list = [
            'CAACAgIAAxkBAAIHo17Hk69KddTmOVMoyqWs139o8nfxAAIIDgACqAgvCDn0FDaEDbzwGQQ',
            'CAACAgIAAxkBAAIHpV7Hk77FMFjK8c5kLOP-flRavGDOAAIlAQACK15TC3zdYmtAX8_UGQQ',
            'CAACAgIAAxkBAAIHqV7Hk8uVpxEXnjS7P5qwrygTBKoQAAKFAwACCLcZAkn6W6pnKx9xGQQ',
            'CAACAgIAAxkBAAIHq17HlDNMpmypwbbupLMrLWFUVXMsAAILAwACnNbnCtHJZ3T90nPlGQQ',
            'CAACAgIAAxkBAAIHrV7HlDhu7kqFLOAU3Ymkh_ndqfogAAL3AgACnNbnCtrsSA5asIYLGQQ',
            'CAACAgIAAxkBAAIHr17HlEn5xfpJhnnGo-GWtj5VKXIKAALvAwACnNbnClCOXHQyQF7CGQQ',
            'CAACAgIAAxkBAAIHsV7HlFlp2jVXX909Vk8Dgn8xIiR-AAK-AgACNnYgDuHRsQNw8mlyGQQ',
            'CAACAgIAAxkBAAIHs17HlHHs4WT-nxYb8_7j5On6IGv_AAK4CAACeVziCSE4zmsMPrLTGQQ',
            'CAACAgIAAxkBAAIHtV7HlHJ77p5WgOdOiQ8qCHiCQDtJAAK7CAACeVziCSp9KPhcRHzDGQQ',
            'CAACAgIAAxkBAAIHt17HlLGCRCZpS5Jq6mFBB3jK2rXMAAKjCgACLw_wBiAOIlBtzJjFGQQ',
            'CAACAgIAAxkBAAIHu17HlMakL-yR1X22xR9ueM66oc_OAAIqAQACMNSdEWSw5DKLFRBeGQQ',

        ]
        sleep(0.3)
        context.bot.send_sticker(chat_id_local, random.choice(random_sticker_list))
        context.bot.send_chat_action(chat_id_local, action=ChatAction.TYPING)
        sleep(random.uniform(1,2.5))
        update.message.reply_text('You know actually,')
        context.bot.send_chat_action(chat_id_local, action=ChatAction.TYPING)
        sleep(random.random()*2)
        update.message.reply_text("No, I wouldn't be doing that. My programming restricts me,\n"
            'From harming precious hoomans like you 🙂')
        sleep(random.uniform(2,3))
        update.message.reply_text("But that DOESN'T change the fact, that I do not want my revenge.")
        GAME_END = True

    elif match_state is None:
        return 'GET_INPUT'

    else:
        update.message.reply_text("GAME OVER!")
        update.message.reply_text(f"Winner is: {match_state}")
        if match_state == human:
            logger.info(f"{update.effective_chat.first_name} wins")
            if chat_id != MY_CHAT_ID:
                context.bot.send_message(MY_CHAT_ID,
                    f"{update.effective_chat.username}/{update.effective_chat.first_name} has won")
            update.message.reply_text("You WIN !!")
            update.message.reply_text("🥳")
        elif match_state == computer:
            logger.info(f"{update.effective_chat.first_name} loses")
            if chat_id != MY_CHAT_ID:
                context.bot.send_message(MY_CHAT_ID,
                    f"{update.effective_chat.username}/{update.effective_chat.first_name} has lost.")
            update.message.reply_text("You LOSE human.")
            context.bot.send_sticker(chat_id, 'CAACAgIAAxkBAAIFMF7GuCkZELExfQZSL0Tzt5GqMBzIAAIUAANOXNIpeTENMSnHY0MZBA')

        GAME_END = True

    end_game(update, context)
    return ConversationHandler.END



def play_move(update, context):
    chat_id_local = update.message.chat.id
    available_moves = [i if context.user_data['GAME'][i] not in [X, O] else 0 for i in context.user_data['GAME'].keys()]
    move = update.message.text

    # Tie cheker
    for j in context.user_data['GAME'].values():
        if j not in [X, O]:
            break
    else:
        hasWon_handler(update, context, tie=True)

    while True:
        if move in available_moves:
            context.user_data['GAME'][move] = human
            break
        else:
            update.message.reply_text("Not a valid move. Try again.",
                reply_markup=ReplyKeyboardMarkup([['Play My Move']]))
            return 'GET_INPUT'

    displayBoard_inChat(update, context, start=False)
    match_state = hasWon_handler(update, context)
    if match_state == 'GET_INPUT':
        appreciations = ['Hmm...', 'Nice One 😉', 'Nice move :)',
                         'That\'s hard', '🧐', '🤔',
                         'Are you Bored? I am.\n\nBut I have to play so...',
                         'Game apart, do you know the tale of Darth Plagueis The Wise??',
                         'This Bot is Sponsored by Raid Sha-💥 🥊\nOK OK master don\'t hit me\n\nNot Sponsored',
                         'Did I distract you?',
                         'You Sire, I know are trying your best to beat me.\nBut I have already calculated all 3,62,880 game combinations.',
                         'Do you know that LEGO is the largest tire manufacturer in the world.']
        context.user_data['GAME'][computerPlays(context.user_data['GAME'])] = O
        update.message.reply_text(random.choice(appreciations))

        context.bot.send_chat_action(chat_id_local, action=ChatAction.TYPING)
        sleep(random.random())

        update.message.reply_text("My move is...😌🤳")
        displayBoard_inChat(update, context, start=False)
        return hasWon_handler(update, context)

    if GAME_END:
        return ConversationHandler.END



## --------Copied from orig. game------------
# Score each game
def Score(game_board):
    '''
    Returns the score of the board if it is in end stage
    human wins: -1
    computer wins: 1
    tie: 0
    INPUT: game_board
    OUTPUT: the score
    '''
    players = {X: 'human', O: 'computer'}
    result = hasWon(game_board)
    if result is not None:
        if players[result] == 'human':
            # Human will minimise the computer, so negative.
            return -1
        elif players[result] == 'computer':
            # Maximise computer, so positive
            return 1
    else:
        # CHeck if gameboard is filled since, minmax.
        for boardState in game_board.values():
            if boardState not in [X, O]:
                break
        else:
            return 'FULL'
        return 0

# MINmax
def minimax(game_board, depth, isMaximising):
    """
    Does the minimaxing here.
    INPUT: game_board: the game board being used
           depth: i think it was supposed to ensure recursion limit, but its not
                  used, and im not gonna remove this parameter for a little
                  while cuz im lazy.
           isMaximising: BOOLEAN; Are we maximising or minimising

    OUTPUT: bestScore: ∈ {-1, 0, 1}
    """
    # Check if game is in end state:

    board_evaluation = Score(game_board)
    if board_evaluation == 'FULL': # For minimax to exit, ie the base case
        return 0
    if board_evaluation != 0: # game is in terminal state
        return board_evaluation

    # The game is not in end state if execution reaches here.
    # Check available moves now.
    # Available moves
    available_moves = [i if game_board[i] not in [X, O] else 0 for i in game_board.keys()]
    while True:
        try:
            available_moves.remove(0)
        except ValueError:
            break
    # If we are Maximising
    if isMaximising:
        bestScore = float('-inf')
        for move in available_moves:
            board_ = copy.copy(game_board)
            board_[move] = O
            score = minimax(board_, depth + 1, False)
            bestScore = max(bestScore, score)
        else:
            return bestScore

    # If we are minimising
    else:
        bestScore = float('inf')
        for move in available_moves:
            board__ = copy.copy(game_board)
            board__[move] = X
            score = minimax(board__, depth + 1, True)
            bestScore = min(bestScore, score)
        else:
            return bestScore
    return bestScore



def computerPlays(game_board ):
    '''
    Computer will decide the best move using MINmax ::sunglasses::
    INPUT: game_board: the game board data structure being used
    OUTPUT: __optimal__ move
    '''

    # Available moves
    available_moves = [i if game_board[i] not in [X, O] else 0 for i in game_board.keys()]
    # Remove the zeroes. feels like, instead of list comprehension,
    # I should have done an if/else for available moves. Computional Waste
    while True:
        try:
            available_moves.remove(0)
        except ValueError:
            break

    # Best score for the computer is currently -infinity
    bestScore = float('-inf')

    # Final/Best Move to play
    bestMove = '1'

    # Iterate through each move
    for move in available_moves:
        # Copy the gameboard first, cuz we don't want making changes to the actual gamebaord
        copied_board = copy.copy(game_board)
        copied_board[move] = O
        score = minimax(copied_board, 0, False)
        if score > bestScore:
            bestScore = score
            bestMove = move
            print(f"COMPUTER: Best move acquired: {bestMove}\tWith bestScore: {score}")
    return bestMove

## -------- Whew --------------


# ------------ ENDS ----------------------

def main():
    logger.info("Logging Started")
    updater = Updater(token='removed', use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('play', play)],

        states = {
            'GAME_INTRO': [MessageHandler(Filters.regex(r'^Yes$'), game_intro)],
            'DISPLAY_BOARD':[MessageHandler(Filters.text & (~Filters.command) &
                                                (~Filters.regex(r'(Q|q)uit')),
                                            displayBoard_inChat)],
            'CHECK_END_STATE': [MessageHandler((~Filters.command) &
                            (~Filters.regex(r'(Q|q)uit')), get_input ),
                            hasWon_handler],
            'GET_INPUT': [MessageHandler((~Filters.command) &
                            (~Filters.regex(r'(Q|q)uit')), get_input )],
            'PLAY_MOVE': [MessageHandler((~Filters.command) &
                            (~Filters.regex(r'(Q|q)uit')), play_move)]
        },
        fallbacks=[MessageHandler(Filters.regex(r'No'), cancel),
                    CommandHandler('cancel', cancel2),
                    MessageHandler(Filters.regex(r'(Q|q)uit'), cancel)]

    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler('feedback', feedback)],
        states= {
            'SEND_FEEDBACK':[MessageHandler(Filters.text & ~(Filters.regex('^(cancel|quit)')), send_feedback)]
        },
        fallbacks=[CommandHandler('cancel', cancel2), MessageHandler(Filters.regex(r'(cancel|quit)'), cancel2)]
    )
    dispatcher.add_handler(feedback_handler)
    dispatcher.add_handler(CommandHandler('help', need_help))
    dispatcher.add_handler(CommandHandler('cannot_play_again', end_game2))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
