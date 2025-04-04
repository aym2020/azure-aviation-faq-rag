#!/bin/bash
cd /home/site/wwwroot
streamlit run app/streamlit_app.py --server.port=8000 --server.enableCORS=false