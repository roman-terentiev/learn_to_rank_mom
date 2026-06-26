# Project Overview

This project is an independent replication and adaptation of:

Poh, Daniel and Lim, Bryan and Zohren, Stefan and Roberts, Stephen, Building Cross-Sectional Systematic Strategies By Learning to Rank (December 12, 2020). The Journal of Financial Data Science Spring 2021, jfds.2021.1.060; DOI: https://doi.org/10.3905/jfds.2021.1.060 , Available at SSRN: https://ssrn.com/abstract=3751012 or http://dx.doi.org/10.2139/ssrn.3751012 

The objective is to study the methodology proposed in the original paper, reproduce its main ideas and results where possible, and develop a personal Python implementation.

This project should not be considered an exact reproduction of the original study. The implementation may differ because of:

- different datasets or data providers
- different sample periods or markets
- alternative assumptions and parameter choices
- transaction costs and execution constraints
- modifications to the original methodology
- additional robustness checks or extensions

# How to Run

1. Clone the repository:

    git clone https://github.com/roman-terentiev/learn_to_rank_mom

2. Install the required dependencies:

    pip install -r requirements.txt

3. Run the orchestrator:

    python main.py  

4. Results are stored in:

    runs/...

# Data

Provider: https://norgatedata.com/

Dataset: US Stocks Data

The raw market data used in this project are not included in this repository.

# Disclaimer

This repository is an independent research and educational project. It is not affiliated with or endorsed by the authors of the original paper. Any errors, interpretations, or modifications are my own.

The code and results are provided for research and educational purposes only and do not constitute financial or investment advice.