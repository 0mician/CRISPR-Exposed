# CRISPR-Exposed

Welcome to the code repository of the project CRISPR-Exposed. This project was developed as part of a class on Bioinformatics taught at KU Leuven (Fall 2015). 

# Overview

The goal of the project was to create a database of CRISPR elements, and offer services to query the information. The code has been organized in 4 components:

- configuration
- dataviz
- pipelines
- webapp

Here is a brief description of those components, which are the top level folders of the repository. Each component has its own README file with more details.

## configuration

In order to enhance the reproducibility of the analysis, and document the environment in which the application can be run, ansible configuration files are provided. We used a vagrant environment for the development phase of the project, which mimick the production environment.

## dataviz

There you can find the code and libraries needed to run the datavisualization locally. The visualization has been integrated to the web application, but the files there were used during the development phase.

## pipelines

Separated from the web application, you can find there the scripts that were used to fetch and process the data we used in this project. The web application folder has an import script that can be used to populate the database once the data has been gathered (see webapp/crispr_exposed/populate_db.py)

## webapp

Based on Django, the application code and assets can be found in the webapp folder. 
