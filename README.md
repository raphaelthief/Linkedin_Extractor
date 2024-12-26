# Linkedin Extractor

![Main](https://github.com/raphaelthief/Linkedin_Extractor/blob/main/Pic/main.JPG "Main")

## Overview

This Python script is designed to automate the extraction of employee profiles from LinkedIn-like webpages and to generate potential email addresses based on the extracted names. The tool is primarily intended for mass attack simulations or phishing campaigns where you can create bulk email addresses by guessing employees' email formats. It can also be used to generate identifiers from employee data for brute force attacks on poorly configured APIs or login pages.

**Note : This tool is for educational purposes only and should not be used for malicious activities.**



## Features

- **Extract LinkedIn profile data** : Extracts employee profile information from LinkedIn-like webpages, including names, LinkedIn profile links, job titles, and mutual connections.
- **Convert names to emails** : Automatically converts extracted names into email addresses based on common email formats, with support for multiple formats (e.g., first.last@example.com, n.first@example.com, etc.).
- **Support for bulk email generation** : Automatically generates emails for mass phishing campaigns or brute-force login attempts on poorly configured APIs and login pages.
- **Profile filtering** : Filters out invalid or incomplete profile names and ensures proper formatting before generating emails.


## Exemple usage

- Target the company by visiting its LinkedIn page along with its employees

![Main](https://github.com/raphaelthief/Linkedin_Extractor/blob/main/Pic/1.JPG "Main")

- Extract the page's source code (load as many profiles as you wish by scrolling down the page)

![Main](https://github.com/raphaelthief/Linkedin_Extractor/blob/main/Pic/2.JPG "Main")

- Run the script by specifying the saved file

![Main](https://github.com/raphaelthief/Linkedin_Extractor/blob/main/Pic/3.JPG "Main")




## Installation

To run this tool, you need to install the required dependencies. You can install them using `pip`:

```bash
pip install -r requirements.txt
```


## Supported email formats

- nom.prenom : last.first@domain.com
- n.prenom : first.first_initial@domain.com
- n.p : first_initial.last_initial@domain.com
- nom.p : last.first_initial@domain.com
- prenom.nom : first.last@domain.com
- p.nom : first_initial.last@domain.com
- p.n : first_initial.last_initial@domain.com
- prenom.n : first.last_initial@domain.com
- prenom : first@domain.com
- nom : last@domain.com



## Example Usage

1. Extract LinkedIn profiles and show all data

```
python extractor.py --file profiles.html --show-all
```

2. Show only names

```
python extractor.py --file profiles.html --names
```

3. Convert extracted names to emails

```
python extractor.py --file profiles.html --convert nom.prenom@example.com
```



## Example Output

For ```--show-all```

```yaml
Name: John Doe
LinkedIn Profile: https://www.linkedin.com/in/john-doe
Title: Software Engineer at TechCorp
Common Relation: Jane Smith

----------------------------------------

Name: Jane Smith
LinkedIn Profile: https://www.linkedin.com/in/jane-smith
Title: Data Scientist at DataTech
Common Relation: John Doe

----------------------------------------
```

For ```--names```

```yaml
John Doe
Jane Smith
```

For ```--convert nom.prenom@example.com```

```graphsql
doe.john@example.com
smith.jane@example.com
```

For ```--convert n.prenom@example.com```

```graphsql
d.john@example.com
s.jane@example.com
```

For ```--convert prenom.n@example.com```

```graphsql
john.d@example.com
jane.s@example.com
```

For ```--convert nom@example.com```

```graphsql
doe@example.com
smith@example.com
```

**etc ...**



## Disclaimer
The creator of this tool does not condone illegal activities or attacks. It is essential to only use this tool for authorized testing, educational purposes, or ethical hacking endeavors in compliance with applicable laws and regulations.
