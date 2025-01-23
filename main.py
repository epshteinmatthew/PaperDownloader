#https://modeldb.science/api/v1/papers
import requests, json

paperslist = requests.get("https://modeldb.science/api/v1/papers").json()


def downloadpaper(code, dest):
    pmid = requests.get("https://modeldb.science/api/v1/papers/" + paper).json()["pubmed_id"]["value"]
    pmdata = requests.get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=" + pmid + "&format=json").json()["records"][0]
    if("pmcid" not in pmdata.keys()):
        return
    pmcid = pmdata["pmcid"]
    print(pmcid)
    #403! need to get around this somehow
    #https://pmc.ncbi.nlm.nih.gov/tools/oai/
    filedata = requests.get("https://pmc.ncbi.nlm.nih.gov/articles/" + pmcid + "/pdf/", allow_redirects=True)
    open(dest+"/"+pmcid, 'wb').write(filedata.content)

for paper in paperslist:
    downloadpaper(paper, "papers")
