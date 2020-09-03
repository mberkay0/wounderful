

<br />
<p align="center">

  <h3 align="center">Wounderful Web Application</h3>

  <p align="center">
    An awesome scratch analysis software!
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)




<!-- ABOUT THE PROJECT -->
## About The Project
<img src="/images/exanalyzer.png" alt="App image"/>

A wound healing assay is a laboratory technique used to study cell migration and cell–cell interaction. This is also called a scratch assay. This application does the analysis the scratch assay.

### Built With
* [Bootstrap](https://getbootstrap.com)
* [Django](https://www.djangoproject.com/)




<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


### Installation


1. Clone the repo
```sh
git clone https://github.com/mberkay0/wounderful.git
```
2. Check if you have a virtual env 
```sh
virtualenv --version
```
3. If (not Installed) 
```sh
pip install virtualenv
```
4. Now create a virtual env in cd wounderful/
```sh
virtualenv venv
```
5. Activate a venv 
```sh
~/venv/Scripts/activate
```
6. Then download a python modules
```sh
pip install -r requirements.txt
```
7. Ok we cool now start a project
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
```sh
python manage.py runserver
```
<!-- USAGE EXAMPLES -->
## Usage

Add a wound healing data-set 

<img src="/images/uploadfiles.png" alt="upload images"/>

Run a script

<img src="/images/run.png" alt="Run the script"/>

Check analysis 

<img src="/images/analysis.png" alt="Analysis"/>

And download a labelled images 

<img src="/images/download.png" alt="Download"/>

Check the labelled images

<img src="/images/exOut.png" alt="Labelled image" style="width:300px;height:400px;"/>




