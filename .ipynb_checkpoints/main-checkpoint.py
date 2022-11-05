#!/usr/bin/env python
# coding: utf-8

import os
import sys, fitz
from bs4 import BeautifulSoup
import re
import json
import argparse


def get_arguments(argv):
    parser = argparse.ArgumentParser(description='PyBib')
    # Simulation settings
    parser.add_argument('-i', '--input_folder', default="")
    parser.add_argument('-n', '--name', default="")
    args = parser.parse_args(argv)

    return args

def extract_title(html_text):
    soup = BeautifulSoup(html_text)
    spans = soup.find_all('span',style=True)
    usedFontSize = []
    for span in spans:
        styleTag = span['style']
        fontSize = re.findall("font-size:(\d+)",styleTag)
        usedFontSize.append(int(fontSize[0]))
        
    max_font = max(usedFontSize)
    
    title_text = []
    for span in spans:
        #print span['style']
        styleTag = span['style']
        fontSize = re.findall("font-size:(\d+)",styleTag)
        if int(fontSize[0]) == max_font:
            title_text.append(span.text)
    
    return ''.join(title_text).strip()


# Try to load the notebook in the traget directory
if __name__ == '__main__':
    # Configuration
    args = get_arguments(sys.argv[1:])

    input_folder = args.input_folder
    name = args.name

    print("Your input folder is " + input_folder)

    if input_folder == "":
        print("Input folder cannot be empty")

    if not input_folder.endswith("\\"):
        input_folder += "\\"

    output_folder = '\\'.join(input_folder.split("\\")[:-3])

    local_dir =  '\\'.join(input_folder.split("\\")[-3:])

    print("Your input folder is " + output_folder)

    if name == "":
        input_folder.split("\\")[-1]

    print("Your output name is " + name)

    if(os.path.isfile(output_folder+"/" + name+".ipynb")):
        with open(output_folder+"/" + name+".ipynb", 'r') as f:
            res = json.load(f)
        cell_id = res['cells'][-1]['id'] + 1
    else:
        res = { "cells": [], 
           "metadata": {
              "kernelspec": {
               "display_name": "Python 3 (ipykernel)",
               "language": "python",
               "name": "python3"
               },
              "language_info": {
               "codemirror_mode": {
                "name": "ipython",
                "version": 3
               },
               "file_extension": ".py",
               "mimetype": "text/x-python",
               "name": "python",
               "nbconvert_exporter": "python",
               "pygments_lexer": "ipython3",
               "version": "3.8.8"
              }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        cell_id = 0
    for paper in os.listdir(input_folder):
        doc = fitz.open(input_folder + paper)
        html_text = ''
        for page in doc:
            html_text += page.get_text('html')
        title = extract_title(html_text)
        local_link = local_dir.replace(" ", "%20") + paper.replace(" ", "%20")
        if local_link not in res:
            remote_link = "https://scholar.google.com/scholar?q="+title.replace(" ", "%20")

            one_cell = {
               "cell_type": "markdown",
               "id": str(cell_id),
               "metadata": {},
               "source": [
                "### "+title+"\n",
                 "[PDF]("+local_link+")" +"\n",
                 "<a href=\""+remote_link+"\">Google Scholar</a>"
               ]
              }
            cell_id+=1
            empty_cell = {
                "cell_type": "markdown",
               "id": str(cell_id),
               "metadata": {},
               "source": [
                " "
               ]
            }
            cell_id+=1
            res['cells'].append(one_cell)
            res['cells'].append(empty_cell)

    with open(output_folder+"/" + name+".ipynb", 'w') as f:
        json.dump(res, f)







# In[ ]:




