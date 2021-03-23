#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2021 Ali Morakabi <alimkb@gmail.com>
#  https://github.com/alimkb
from flask import Flask, render_template, request, redirect, url_for
import http.client, json, random



app = Flask(__name__)
apiKey = 'NZWKFR9-3PG4S2G-QMH7T1D-AFN8Y60' # replace with your API Key


def status():
	conn = http.client.HTTPSConnection("api.nowpayments.io")
	payload = ''
	headers = {}
	conn.request("GET", "/v1/status", payload, headers)
	res = conn.getresponse()
	data = res.read()
	msg = json.loads(data.decode("utf-8"))
	return msg['message']


def estimated(amount,currency_from, currency_to):
	conn = http.client.HTTPSConnection("api.nowpayments.io")
	payload = ''
	headers = {
	  'x-api-key': apiKey
	}
	conn.request("GET", f"/v1/estimate?amount={amount}&currency_from={currency_from}&currency_to={currency_to}", payload, headers)
	res = conn.getresponse()
	data = res.read()
	msg = json.loads(data.decode("utf-8"))
	return msg
	

def payment(amount, currency_from, currency_to, orderId, email):
	conn = http.client.HTTPSConnection("api.nowpayments.io")
	payload = json.dumps({
	  "price_amount": amount ,
	  "price_currency": currency_from ,
	  "pay_currency": currency_to,
	  "ipn_callback_url": "https://nowpayments.io",
	  "order_id": orderId,
	  "order_description": "Transfer made by : "+ email
	})
	headers = {
	  'x-api-key': apiKey ,
	  'Content-Type': 'application/json'
	}
	conn.request("POST", "/v1/payment", payload, headers)
	res = conn.getresponse()
	data = res.read()
	msg = json.loads(data.decode("utf-8"))
	return msg
	

def payStatus(paymentId):
	conn = http.client.HTTPSConnection("api.nowpayments.io")
	payload = ''
	headers = {
	  'x-api-key': apiKey
	}
	conn.request("GET", f"/v1/payment/{paymentId}", payload, headers)
	res = conn.getresponse()
	data = res.read()
	msg = json.loads(data.decode("utf-8"))
	return msg
	
	
	
@app.route('/', methods=['POST', 'GET'] )
def index():
	message =''
	if status() != 'OK':
		message = 'Unable to verify your payment.'
	
	return render_template('start.html', message = message)



@app.route('/confirm', methods= ['POST','GET'] )
def confirm():
	formData = ''
	if request.method == 'POST':
		
		email = request.form.get('email')
		currency_from = request.form.get('currency_from')
		amount = request.form.get('amount')
		currency_to = 'usdttrc20'
		formData = estimated(amount,currency_from, currency_to)
		
		return render_template('confirm.html', formData = formData , email = email)
		
	
	return render_template('confirm.html', formData = formData)



@app.route('/transfer', methods= ['POST','GET'] )
def transfer():
	formData = ''
	if request.method == 'POST':
		email = request.form.get('email')
		currency_from = request.form.get('currency_from')
		amount = request.form.get('amount')
		currency_to = 'usdttrc20'
		formData = payment(amount, currency_from, currency_to, random.randrange(100000, 1000000, 2), email)
		return render_template('transfer.html', formData = formData, email = email)

	return render_template('transfer.html', formData = formData)


@app.route('/final', methods= ['POST','GET'] )
def final():
	formData = ''
	if request.method == 'POST':
		email = request.form.get('email')
		paymentId = request.form.get('payment_id')
		formData = payStatus(paymentId)
		return render_template('final.html', formData = formData)
	
	return render_template('final.html', formdata = formData)



    
if __name__ == '__main__':
	app.run(debug=True)
