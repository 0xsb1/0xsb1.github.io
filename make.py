import json, os
import urllib.parse
import hashlib
import re


filenames = os.listdir("data")

for filename in filenames:
    filename = "data/" + filename
    fp = open(filename)
    data  = json.load(fp)
    teach_name = " ".join(x.title()for x in filename.split(".")[-2].split("/")[-1].split("_")[1].split("-"))
    repo_name = filename.split(".")[-2].split("/")[-1].split("_")[1]
    print(teach_name)

    outfile = filename.split(".")[-2].split("_")[-1]+".html"

    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study Material</title>
    <link rel="stylesheet" href="assets/style.css">
    </head>
    <body> 
    <div class="container">
    <div class="header">Study Material<div class="teacher-name">"""+teach_name+"""</div></div>
    <div class="files">
    """
    urls = []
    print("Geneating HTML ...")
    for td in data['tbody']['tr'] :
        el = td['td']
        if '@class' in el[0]: continue
        if 'a' not in el[4]: continue
        # print(str(el[0]) + " | " + str(el[1]) + " | " + str(el[2]) + " | " + str(el[3]) )
        link = el[4]['a']['@href']
        ext = link.split(".")[-1]
        link =  "https://www.surendranathcollege.ac.in/new/" + link.replace(' ', '%20')
        saveas = str(el[2]) + "-" + str(el[3]) + "-" + hashlib.md5(link.encode()).hexdigest()[:4] + "." + ext
        saveas = ' '.join([i for i in saveas.split(" ") if i])
        saveas = saveas.replace(" ", "-")
        saveas = re.sub(r'-+', '-', saveas)
        saveas = saveas.replace("/", "")
        html += """<div class="file"><div class="box"><a href=\"https://raw.githubusercontent.com/0xsb1/"""+repo_name+"""/main/"""+saveas+"""\"><div class="module">"""+ str(el[2])+"""</div><div>"""+ str(el[3])+"""</div></div></a></div>"""
        urls.append([link, saveas])

    html += """</div></div></body></html>"""
    with open(outfile, "w+") as fp:
        fp.write(html)
    # print("Downloading files...")

    # for url in urls:
    #     print(url[0])
    #     print(url[1])
    #     print()
    #     os.system("curl -H \"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0\"  --progress-bar \""+url[0]+"\" -o \"files/"+url[1]+"\"")

    # print("Complete")
    print()