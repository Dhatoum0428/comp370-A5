import pandas as pd 
import argparse
import os

main_path = "/home/dhatoum/projects/Assignments/comp370-A5/"

df = pd.read_csv(main_path + "data/2024_incidents.csv")

print(df.head())
