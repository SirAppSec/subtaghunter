import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
import click
import csv
import yaml
import json
from loguru import logger

# Configuration as Global Variables
TAGS_TO_SEARCH = {
    "img": "src",
    "script": "src"
}
DEFAULT_SCHEME = "https"

def request_webpage(webpage:str) -> requests.Response:
    try:
        response:requests.Response = requests.get(webpage)
    except MissingSchema:
        logger.warning("No schema Identified adding schema and re-running request")
        webpage = DEFAULT_SCHEME +"://"+ webpage
        response = requests.get(webpage)
    return response
@click.command()
@click.argument('target_domains', type=str, nargs=-1)
@click.argument('webpages', type=str, nargs=-1)
@click.option('--output-format', default='yaml', help='Output format: csv, yaml, or json. Default is yaml.')
def search_domain(target_domains: str, webpages: tuple[str], output_format: str):
    """CLI tool to search for instances of a target domain within given webpages.
    Args:
    - target_domain: Domain to search for.
    - webpages: Webpages in which the domain will be searched.
    """
    print(r""" __       _    _____                               _            
/ _\_   _| |__/__   \__ _  __ _  /\  /\_   _ _ __ | |_ ___ _ __ 
\ \| | | | '_ \ / /\/ _` |/ _` |/ /_/ / | | | '_ \| __/ _ \ '__|
_\ \ |_| | |_) / / | (_| | (_| / __  /| |_| | | | | ||  __/ |   
\__/\__,_|_.__/\/   \__,_|\__, \/ /_/  \__,_|_| |_|\__\___|_|   
                          |___/                                 
""")
    results = []

    for webpage in webpages:
        response = request_webpage(webpage)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag, attribute in TAGS_TO_SEARCH.items():
            for found_tag in soup.find_all(tag):
                url = found_tag.get(attribute)
                if url and any(domain in url for domain in target_domains):
                    results.append({
                        "webpage": webpage,
                        "tag": tag,
                        "attribute": attribute,
                        "url": url
                    })
                    logger.debug(f"Found so far:")
                    logger.debug(results)

    if output_format == 'csv':
        _output_csv(results)
    elif output_format == 'json':
        _output_json(results)
    elif output_format == 'yaml':
        _output_yaml(results)
    else:
        click.echo("Invalid output format.")

def _output_csv(results: list[dict]):
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['webpage', 'tag', 'attribute', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

def _output_yaml(results: list[dict]):
    with open('output.yaml', 'w') as yamlfile:
        yaml.dump(results, yamlfile)

def _output_json(results: list[dict]):
    with open('output.json', 'w') as jsonfile:
        json.dump(results, jsonfile)

def main():
    search_domain()

if __name__ == "__main__":
    main()
