# Ethics Analyzer

## Description

This is a simple web application that analyzes a .csv or .xlsx file for ethical issues. For exapmle, it runs tests if the data has bias or fairness issues or there are other problems in the data like data leakage, overfitting, missing values etc.

## Technologies Used

In this project that tools that were used are:
    - python programing language
    - flask and scipy.stats libraries
    - docker and docker compose

## Prerequisites

    - docker and docker compose

## Instructions

1. clone this repository
 `git clone https://github.com/petrosagiakos/ethic_analyzer`

2. build application with `docker compose up --build` or `sudo docker compose up --build` on linux

3. run application with `docker compose start` or `sudo docker compose start` on linux

4. go to `http://localhost:8083/`

## Contributor

    - Sagiakos Petros inf2023185