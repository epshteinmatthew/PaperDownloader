import asyncio
import urllib

import aiohttp
from bs4 import BeautifulSoup
import urllib
import requests

# Fetch the list of papers
paperslist = requests.get("https://modeldb.science/api/v1/papers").json()
linkslist = []
idlist = []

async def download_paper(session, code, dest):
    try:
        # Fetch paper details
        async with session.get(f"https://modeldb.science/api/v1/papers/{code}") as response:
            paper_details = await response.json()
            pmid = paper_details["pubmed_id"]["value"]
    except Exception as e:
        #print(f"Error fetching paper details for {code}: {e}")
        return

    # Convert PubMed ID to PMCID
    async with session.get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={pmid}&format=json") as response:
        pmdata = await response.json()
        if "pmcid" not in pmdata["records"][0]:
            #print(f"No PMCID found for PMID {pmid}")
            return
        pmcid = pmdata["records"][0]["pmcid"]

    # Fetch the PDF link
    async with session.get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}&format=pdf") as response:
        file_address = await response.text()
        data = BeautifulSoup(file_address, "xml")
        ftp_address = data.find_all("link")
        if not ftp_address:
            #print(f"No PDF found for PMCID {pmcid}")
            return
        ftp_address = ftp_address[0]["href"]
        linkslist.append(ftp_address)
        idlist.append(pmcid)
        print(len(linkslist))



async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [download_paper(session, paper, "papers/") for paper in paperslist[20000:40000]]
        await asyncio.gather(*tasks)
    for i in range(len(linkslist)):
        urllib.request.urlretrieve(linkslist[i], "papers/" + idlist[i] + ".pdf")
        print(i)

# Run the async main function
asyncio.run(main())