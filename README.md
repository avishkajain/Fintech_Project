# Finance Tracker Backend

## Overview

A Python-based backend system to manage financial transactions with CRUD operations, analytics, role-based access, and ML-based spending insights.

## Features

* Add, view, update, delete transactions
* Filter by category and type
* Summary (income, expense, balance)
* Role-based access (admin, analyst, viewer)
* ML-based spending analysis

## Tech Stack

* Flask
* SQLite
* Python

## Run

pip install flask
python app.py

## APIs

POST /transactions
GET /transactions
PUT /transactions/{id}
DELETE /transactions/{id}
GET /summary

## ML Logic

Basic spending pattern detection using average expense.
