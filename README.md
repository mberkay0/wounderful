

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
  * [Video of Project](#video-of-project)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Changelog](#changelog)
* [References](#references)




<!-- ABOUT THE PROJECT -->
## About The Project
<img src="/images/exanalyzer.png" alt="App image"/>

A wound healing assay is a laboratory technique used to study cell migration and cell–cell interaction. This is also called a scratch assay. This application does the analysis scratch assay.

### Built With
* [Bootstrap](https://getbootstrap.com)
* [Django](https://www.djangoproject.com/)
* [Plotly](https://plotly.com/)


### Video of Project
<img src="/images/analyze.gif"/>

<img src="/images/graphics.gif"/>



<!-- GETTING STARTED -->
## Getting Started

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

<img src="/images/download.png" alt="Download" width="441.5" height="130"/>

Check the labelled images

<img src="/images/exOut.png" alt="Labelled image" width="600" height="500"/>



## References

*[In vitro Wound Healing Assay](https://www.degruyter.com/view/journals/biomat/17/1-2/article-p79.xml)
*[Wikipedia-Wound Healing Assay](https://en.wikipedia.org/wiki/Wound_healing_assay)
*[U-Net](https://arxiv.org/pdf/1505.04597.pdf)
*[Label-free](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2880-8)



## Changelog:

### [15.09.2020]:
* Multiple dataset usage feature added and multiple analysis options added at the same time.
* Added a authentication system. 
* The display feature of labelled frames in the program has been added.
