#https://modeldb.science/api/v1/papers
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
#from paperscraper.pdf import save_pdf
import requests, json

paperslist = requests.get("https://modeldb.science/api/v1/papers").json()


def downloadpaper(code, dest):
    try:
        pmid = requests.get("https://modeldb.science/api/v1/papers/" + paper).json()["pubmed_id"]["value"]
    except:
        return


    pmdata = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=" + pmid + "&format=json").json()["records"][0]
    if("pmcid" not in pmdata.keys()):
        return
    pmcid = pmdata["pmcid"]

    my_file = Path("papers/" + pmcid + ".pdf")
    if my_file.is_file():
        return

    #https://pmc.ncbi.nlm.nih.gov/tools/oai/
    fileadress = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=" + pmcid + "&format=pdf", allow_redirects=True).content
    data = BeautifulSoup(fileadress, "xml")
    ftpadress = data.find_all("link")
    if(len(ftpadress) > 0):
        ftpadress = ftpadress[0]["href"]
        print(pmcid)
    else:
        print("no pdf")
        return
    urllib.request.urlretrieve(ftpadress, "papers/" + pmcid + ".pdf")


for paper in paperslist:
    downloadpaper(paper, "papers/")
