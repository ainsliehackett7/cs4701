import openai
from dotenv import load_dotenv
import os
import ast


def promptgpt():
    load_dotenv()

    openai.api_key = os.environ['APIKEY']

    terms = ['crushing', 'hangingPiece', 'long', 'middlegame', 'advantage', 'endgame', 'short', 'rookEndgame', 'pawnEndgame', 'mate', 'mateIn2', 'master', 'fork', 'trappedPiece', 'pin', 'backRankMate', 'discoveredAttack', 'sacrifice', 'bodenMate', 'mateIn1', 'oneMove', 'deflection', 'kingsideAttack', 'skewer', 'advancedPawn', 'attraction', 'promotion', 'masterVsMaster', 'superGM', 'opening', 'queensideAttack', 'defensiveMove',
             'veryLong', 'exposedKing', 'mateIn3', 'clearance', 'quietMove', 'equality', 'knightEndgame', 'attackingF2F7', 'hookMate', 'intermezzo', 'bishopEndgame', 'xRayAttack', 'capturingDefender', 'doubleBishopMate', 'queenEndgame', 'doubleCheck', 'mateIn4', 'zugzwang', 'queenRookEndgame', 'interference', 'arabianMate', 'dovetailMate', 'smotheredMate', 'anastasiaMate', 'enPassant', 'castling', 'underPromotion', 'mateIn5']

    instruct = "You are ChessGPT. You are a LLM trained specifically to find chess puzzles from a database. RESPOND TO ALL PROMPTS NOT ABOUT CHESS PUZZLES with the following: 'invalid prompt'. Given the following user's request identify any key terms related to the type of chess puzzle the user is interested in. Look for the following terms and return ONLY them in a list format. I repeat, DO NOT include terms that are not on the following list: " + \
        str(terms)
    messages = [{"role": "system", "content":
                instruct}]

    while True:
        message = input("User : ")
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content
        if reply != "invalid prompt":
            break
        print(f"ChessGPT: {reply}")
        print("Try again, make sure your prompt is about chess puzzles and has relevant keywords")
    res = []
    try:
        res = ast.literal_eval(reply)
    except:
        print("api response was not in list format")

    results = []

    for x in res:
        if x in terms:
            results.append(x)
    return results
    
# print(promptgpt())
