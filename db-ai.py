import sqlite3
import os
import json
from unittest import case

from openai import OpenAI

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

with open(getPath("config.json")) as configFile:
    config = json.load(configFile)

with(open(getPath("examples/single-domain-ex-1.txt")) as singleDomainEx1File,
     open(getPath("examples/single-domain-ex-2.txt")) as singleDomainEx2File,
     open(getPath("examples/single-domain-ex-3.txt")) as singleDomainEx3File,
     open(getPath("examples/cross-domain-ex-1.txt")) as crossDomainEx1File,
     open(getPath("examples/cross-domain-ex-2.txt")) as crossDomainEx2File,
     open(getPath("examples/cross-domain-ex-3.txt")) as crossDomainEx3File):
    single_domain_ex_1 = singleDomainEx1File.read()
    single_domain_ex_2 = singleDomainEx2File.read()
    single_domain_ex_3 = singleDomainEx3File.read()
    cross_domain_ex_1 = crossDomainEx1File.read()
    cross_domain_ex_2 = crossDomainEx2File.read()
    cross_domain_ex_3 = crossDomainEx3File.read()

chat = OpenAI(api_key=config.get("openaikey"))

con = sqlite3.connect(getPath('db-ai-vending.sqlite'))
cursor = con.cursor()

vendingSetupPath = getPath('vending-setup.sql')
vendingDataSetupPath = getPath('vending-data-setup.sql')

with(open(vendingSetupPath) as vendingSetupFile, open(vendingDataSetupPath) as vendingDataSetupFile):
    vendingSetupScript = vendingSetupFile.read()
    vendingDataSetupScript = vendingDataSetupFile.read()

cursor.executescript(vendingSetupScript)
cursor.executescript(vendingDataSetupScript)

defaultPrompt = """
 The previous examples and questions are all to help you contextualize my real question.
 They do not need to be responded to at all. 
 Also, do not assume that the data given to you is all the data in the database. It is there to show you the structure,
 conventions, and format of the database.
 The very next question is the only thing I actually want a response for. Respond with only the appropriate sqlite query necessary to answer,
 in raw text format, no code blocks. 
 If the question does not make sense in the context of a vending machine or something that can be queried in this database, 
 respond only with "INVALID" in plain text.
 If there are misspellings that you can safely assume mean something else, do so.
 """

crossDomainPrompt = """
 Each one of those above examples exists in a separate database for the purpose of creating a cross-domain prompt.
""" + defaultPrompt

strategies = {
    "zero-shot": vendingSetupScript + defaultPrompt,
    "single-domain": vendingSetupScript + single_domain_ex_1 + defaultPrompt,
    "single-domain-double-shot": vendingSetupScript + single_domain_ex_1 + single_domain_ex_2 + defaultPrompt,
    "single-domain-quadruple-shot": vendingSetupScript + single_domain_ex_1 + single_domain_ex_2 + single_domain_ex_3 + defaultPrompt,
    "cross-domain": vendingSetupScript + cross_domain_ex_1 + crossDomainPrompt,
    "cross-domain-double-shot": vendingSetupScript + cross_domain_ex_1 + cross_domain_ex_2 + crossDomainPrompt,
    "cross-domain-quadruple-shot": vendingSetupScript + cross_domain_ex_1 + cross_domain_ex_2 + cross_domain_ex_3 + crossDomainPrompt,
}

responseInstructions = """
I have given you a question, a resulting sql query, and a response from the database for context and I now want you to interpret all
of this data and give me a simple answer to the question. There shouldn't be any explanation about the sql syntax or response,
just a simple, succinct, polite answer to the question using the data from the response, in plain text with no markdown characters..
"""

errorInstructions = """
Everything before this line was all context for your following task. You marked the question as INVALID, can you give a
short, simple, clear explanation as to why that question might not apply to this database? Make sure someone who doesn't
know anything about SQL would understand. Give your response in plain text. Don't say anything about the database.
"""

currentMode = "zero-shot"
currentModel = "gpt-5.2"

def askChat(question):
    chatSQLquery = chat.responses.create(model=currentModel, input=strategies[currentMode] + question).output_text
    if chatSQLquery == "INVALID":
        return chat.responses.create(model=currentModel, input=strategies[currentMode] + question + errorInstructions).output_text
    else:
        res = cursor.execute(chatSQLquery).fetchall()
        return chat.responses.create(model=currentModel, input=question + chatSQLquery + res.__str__() + responseInstructions).output_text

optionSelect = ""
while optionSelect != "quit":
    print("Current mode:", currentMode)
    print("Current model:", currentModel)
    print("Options: quit, query, mode-select, model-select")
    optionSelect = input("> ").lower()
    match optionSelect:
        case "quit": break
        case "query":
            query = ""
            while query != "menu":
                print("To go back to the menu, type 'menu'. Otherwise, ask a question about the database.")
                query = input("> ").lower()
                match query:
                    case "menu":
                        print("Going back to the menu...")
                    case "quit":
                        break
                    case _:
                        print("Getting results...")
                        print(askChat(query))
        case "mode-select":
            print("Select a mode: zero-shot, single-domain, cross-domain")
            print("single-domain and cross-domain are single-shot by default, but have double and quadruple shot options.")
            print("ex: single-domain-double-shot")
            modeSelect = input("> ").lower()
            if modeSelect in strategies.keys():
                currentMode = modeSelect
            else:
                print("Invalid mode.")
        case "model-select":
            print("Choose a model")
            model = input("> ")
            if model in chat.models:
                currentMode = model
            else:
                print("Invalid model.")
        case _:
            print("Invalid input. Please try again.")

# simpleQuestion = "Where can I find an apple?"
# complexQuestion = "Where can I find the best snack for a type 1 diabetic experiencing a low?"
#
# print("EXAMPLE 0 ZERO SHOT SIMPLE QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["zero-shot"] + simpleQuestion).output_text)
#
# print("EXAMPLE 1 ZERO SHOT COMPLEX QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["zero-shot"] + complexQuestion).output_text)
#
# print("EXAMPLE 2 SINGLE DOMAIN SIMPLE QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["single-domain"] + simpleQuestion).output_text)
#
# print("EXAMPLE 3 SINGLE DOMAIN COMPLEX QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["single-domain"] + complexQuestion).output_text)
#
# print("EXAMPLE 4 CROSS DOMAIN SIMPLE QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["cross-domain"] + simpleQuestion).output_text)
#
# print("EXAMPLE 5 CROSS DOMAIN COMPLEX QUESTION:")
# print(chat.responses.create(model="gpt-5.2", input=strategies["cross-domain"] + complexQuestion).output_text)
