#!/bin/bash
python3 -m uvicorn api:app --reload &
streamlit run app_web.py
