# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import pandas as pd
import os
from pathlib import Path
import re
import time
from ast import literal_eval
import pickle

APP_PATH = Path(__file__).resolve().parent.parent
all_freq = os.path.join(APP_PATH.as_posix(), 'base/data/all_frequencies.pkl')
all_freq_pkl = pd.read_pickle(all_freq)

inv_file = os.path.join(APP_PATH.as_posix(), 'base/data/inverse_file.txt')
inverse_file = open(inv_file, 'r', encoding = "utf-8").read().splitlines()
dict_file = {item.split('->')[0].strip():item.split('->')[1].strip() for item in inverse_file}

freq_file = os.path.join(APP_PATH.as_posix(), 'base/data/all_frequencies.txt')
frequencies_file = open(freq_file, 'r', encoding = "utf-8").read().splitlines()
dict_freq = {item.split('->')[0].strip():item.split('->')[1].strip() for item in frequencies_file}


@blueprint.route('/')
def index():

    return render_template('index.html', segment='index')

@blueprint.route('/inverse_file.html/<page>', methods=["GET", "POST"])
def inverse_file_fun(page):
    if request.method == 'GET':    
        start = int(page)*10-10
        end = int(page)*10
        current_page = inverse_file[start:end]
        return render_template('inverse_file.html', segment='inverse_file', current_page = current_page, page = int(page))

@blueprint.route('/search_inverse_file', methods=['GET', 'POST'])
def search_inverse_file():
    if request.method == 'GET':
        term = request.args['term']
        if term: 
            current_page = [term + ' -> '+ dict_file[term]]
            return render_template('inverse_file.html', segment='inverse_file', current_page = current_page)
        else:
            return redirect(url_for('home_blueprint.inverse_file_fun', page = '1', method="GET"))     

@blueprint.route('/all_frequencies.html/<page>', methods=["GET", "POST"])
def all_frequencies(page):
    if request.method == 'GET':    
        start = int(page)*10-10
        end = int(page)*10
        current_page = frequencies_file[start:end]
        print(current_page)
        return render_template('all_frequencies.html', segment='all_frequencies', current_page = current_page, page = int(page))

@blueprint.route('/search_freq_file', methods=['GET', 'POST'])
def search_freq_file():
    if request.method == 'GET':
        document = request.args['document']
        if document: 
            current_page = [document + ' -> '+ dict_freq[document]]
            return render_template('all_frequencies.html', segment='all_frequencies', current_page = current_page)
        else:
            print('not')
            return redirect(url_for('home_blueprint.all_frequencies', page = '1', method="GET"))    

@blueprint.route('/boolean_model_search', methods=['GET', 'POST'])
def boolean_model_search():
    if request.method == 'GET':
        query = request.args['query']
         
        msg = query_validation(query)
        if msg != True:
            return render_template('boolean_model.html', segment='booleam_model', msg = msg)
        else:
            query = query.replace('*', 'and').replace('+', 'or').replace('-', 'not')
            pertinent = evaluation(query, all_freq_pkl)
            
            return render_template('boolean_model.html', segment='booleam_model', pertinent = pertinent, query = query, lenPrt = len(pertinent))    

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  

# Query regex
def query_validation(query):
	if len(query) == 0:
		return 'Enter a query please'
	else:
		operator=["*","+"]
		opr_not="-"
		req=query.split()
		if(req[len(req)-1].lower()==opr_not):
			return 'The query must respect the rules'
		for i in range(0,len(req)-1):
			if req[i].lower()==opr_not and req[i+1] in operator:
				return 'The query must respect the rules'
		req=[r for r in req if r.lower()!= opr_not]
		if len(req)%2 == 0 :
			return 'The query must respect the rules'
		for i in range(1,len(req),2):
			if req[i].lower() not in operator:
				return 'The query must respect the rules'
		for i in range(0,len(req),2):
			if req[i].lower() in operator:
				return 'The query must respect the rules'
		return True

def evaluation(query, files):
    pertinent_docs = ""
    opr_par_not = 'not, (, )'
    not_position = []
    
    init_query = query.split()
    
    # keep traceability of not position
    for i in range(0, len(init_query)):
        if init_query[i].lower() in opr_par_not :
            not_position.append(i)
    
    # eliminate not operand
    init_query = [r for r in init_query if r.lower() not in opr_par_not]
    for key, row in files.items():
        req = [r for r in init_query]
        for j in range(0, len(init_query), 2):
            if req[j].lower() in [term for term in row]:
                req[j] = 1
            else:
                req[j] = 0
        for pos in not_position:
            req.insert(pos, opr_par_not)
        print(req)    
        current_query = ""
        for r in req:
            current_query += " " + str(r)
        result = eval(current_query)
        if(result == 1):
            pertinent_docs += str(key) + ", "
    return pertinent_docs