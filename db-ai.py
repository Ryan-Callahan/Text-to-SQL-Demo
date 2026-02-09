import sqlite3
import os


fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

con = sqlite3.connect(getPath('db-ai-vending.sqlite'))
cursor = con.cursor()

vendingSetupPath = getPath('vending-setup.sql')
vendingDataSetupPath = getPath('vending-data-setup.sql')

with(open(vendingSetupPath) as vendingSetupFile, open(vendingDataSetupPath) as vendingDataSetupFile):
    vendingSetupScript = vendingSetupFile.read()
    vendingDataSetupScript = vendingDataSetupFile.read()

cursor.executescript(vendingSetupScript)
cursor.executescript(vendingDataSetupScript)


