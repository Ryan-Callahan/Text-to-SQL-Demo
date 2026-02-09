import sqlite3
import os
import json
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
 The very next question is the only thing I actually want a response for. Respond with only the appropriate sqlite query necessary to answer.
 """

crossDomainPrompt = """
 Each one of those above examples exists in a separate database for the purpose of creating a cross-domain prompt.
""" + defaultPrompt

strategies = {
    "zero-shot": vendingSetupScript + defaultPrompt,
    "single-domain": vendingSetupScript + single_domain_ex_1 + defaultPrompt,
    "single-domain-double-shot": vendingSetupScript + single_domain_ex_1 + single_domain_ex_2 + defaultPrompt,
    "single-domain-triple-shot": vendingSetupScript + single_domain_ex_1 + single_domain_ex_2 + single_domain_ex_3 + defaultPrompt,
    "cross-domain": vendingSetupScript + cross_domain_ex_1 + crossDomainPrompt,
    "cross-domain-double-shot": vendingSetupScript + cross_domain_ex_1 + cross_domain_ex_2 + crossDomainPrompt,
    "cross-domain-triple-shot": vendingSetupScript + cross_domain_ex_1 + cross_domain_ex_2 + cross_domain_ex_3 + crossDomainPrompt,
}

simpleQuestion = "Where can I find an apple?"
complexQuestion = "Where can I find the best snack for a type 1 diabetic experiencing a low?"

print("EXAMPLE 0 ZERO SHOT SIMPLE QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["zero-shot"] + simpleQuestion).output_text)

print("EXAMPLE 1 ZERO SHOT COMPLEX QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["zero-shot"] + complexQuestion).output_text)

print("EXAMPLE 2 SINGLE DOMAIN SIMPLE QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["single-domain"] + simpleQuestion).output_text)

print("EXAMPLE 3 SINGLE DOMAIN COMPLEX QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["single-domain"] + complexQuestion).output_text)

print("EXAMPLE 4 CROSS DOMAIN SIMPLE QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["cross-domain"] + simpleQuestion).output_text)

print("EXAMPLE 5 CROSS DOMAIN COMPLEX QUESTION:")
print(chat.responses.create(model="gpt-5.2", input=strategies["cross-domain"] + complexQuestion).output_text)
