from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from os import walk
from json import dump
import time
myURLS=[]
path="./Input/"

def addComments(url,delay):
    while True:
        try:
            #Use this to crawl for hashtags
            #page=urllib.request.urlopen('http://lookbook.nu/search?page=' + str(num) + '&amp;q=%11' + style)

            #Use this to crawl for urls in the respective categories
            #web_page = 'http://lookbook.nu/explore/' + style + '?page=' + str(num)
            #rint (web_page)//usertext-body may-blank-within md-container , usertext-body may-blank-within md-container
            # Url, header and request delay
            # If we don't set an unique User Agent, Reddit will limit our requests per hour and eventually block them
            userAgent = ""

            hdr = {'User-Agent': userAgent}
            if delay < 2:
                delay = 2
            time.sleep(10)
            req = urllib.request.Request(url, headers={'User-agent': 'your bot 0.1'})
            #contents = urllib2.urlopen(request).read()
            page = urllib.request.urlopen(req)#headers = {'User-agent': 'your bot 0.1'}


        except HTTPError as e:
            print(e)
            #page = urllib.request.urlopen(url)
            print("Unable to raech " + url)


        try:
            if not page:
                print(url)
                break
            designCritique = {}
            question = {}
            feedbacks = []

            soup=BeautifulSoup(page, 'html.parser')
            #soup.
            mytags = soup.find_all("div", class_ ="usertext-body may-blank-within md-container ")
            #mytags = soup.find_all("h3", class_="bigger force_wrap")
            #print("len myatgs",len(mytags))
            if not mytags:
                print(url)
                return

            questionp= mytags[1].findAll("p",text=True)
            questionTExt=' '.join([i.getText() for i in questionp])


            dislike_score = soup.find_all( class_="score dislikes")
            unvoted_score = soup.find_all( class_="score unvoted")
            like_score =     soup.find_all( class_="score likes")

            question["text"]=questionTExt
            question["dislike_score"]=dislike_score[0]['title']
            question["unvoted_score"]=unvoted_score[0]['title']
            question["like_score"]=like_score[0]['title']
            designCritique["id"]=url
            designCritique["question"]=question
            designCritique["feedbacks"]=[]
            #print("q"+str(question)+"\n")
            #print(question)
            #exit()
            mytags=mytags[2:]
            dislike_score=dislike_score[1:]
            unvoted_score=unvoted_score[1:]
            like_score=like_score[1:]



            subtags=[]
            i=0
            for tag in mytags:
                feedback={}
                feedback["dislike_score"]=dislike_score[i]['title']
                feedback["unvoted_score"]=unvoted_score[i]['title']
                feedback["like_score"]=like_score[i]['title']
                i=i+1
                #print("tag"+str(tag))
                x=(tag.find("div", class_ ="md"))
                #print("div md",str(x))
                #print(x)
                if len(x)>1:
                   y=' '.join([y.getText() for y in x.findAll("p",text=True)])

                else:
                    y=x[0].find("p",text=True).getText()
                #print("from p", y)
                feedback['text']=y
                #print("feedback"+str(feedback))
                #print("\n\n\n")
                feedbacks.append(feedback)
            designCritique["feedbacks"]=feedbacks
            return (designCritique)
            break

        except Exception as e:
            print(e)
            print(url)
            break





if __name__ == "__main__":
    filenames = []
    for (dirpath, dirnames, files) in walk(path):
        #print(dirnames)
        filenames.extend(files)
    print(filenames)
    for file in filenames:
        if(file=='Final.txt'):
            designCritiques=[]
            with open(path+file) as filep:
                for line in filep:
                    line = line.strip()
                    designCritiques.append(addComments(line,2))
            with open("./Output/"+file,"w") as filep1:
                dump(designCritiques,filep1)

