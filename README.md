# OSUWebScraping

OSUWebScraping is a project by Ahmed Guled and Jared Alonzo as part of their Research Experience for Undergraduates in Spring 2025 under the supervision of Dr. Monique Ross and Ph.D. candidate Camila Olivero Araya. The goal is to identify faculty at The Ohio State University who use computing in their fields. The project collects faculty data through web scraping and visualizes it with a heat map to show where computing is being used across disciplines.

## Project Overview

### Web Scraping
- Extracts faculty names, titles, emails, and department affiliations.
- Searches for computing-related keywords in faculty profiles.

### Data Visualization
- Generates a heat map to display faculty engagement in computing across departments.

## Repository Structure

```bash
OSUWebScraping/
│── TechDirectories/                # CSV files of faculty interested in computing (by department)
│── TechInterestedWebScrapingScripts/ # Python scripts for scraping faculty with computing interests
│── WebScrapingScripts/             # General web scraping scripts for faculty directories
│── <CSV files>                      # Raw faculty directory data from various departments
│── README.md                        # Project documentation
```

## Requirements

To run the web scraping scripts, install the following Python libraries:

```bash
pip install requests beautifulsoup4 pandas/
````

## How to use

1. Run a scraping script - each script is designed for a specific department and will generate a CSV file with faculty information. Run a script like this:

```bash
python TechInterestedWebScrapingScripts/scrape_department.py
```

2. Check the output - the scraped data is saved in TechDirectories/ as a CSV file.

3. Analyze results - the heat map visualization (in progress) will use these CSV files to show faculty engagement in computing.
