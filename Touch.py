import mwclient
import getopt
import sys
from KMSFunctions import login, saveLog, getValue

global onVM
onVM = False
global logMessages
logMessages = ""

def getArguments():
    # accept fromWiki, toWiki, protect, page, and category from cl
    try:
        opts,args = getopt.getopt(sys.argv[1:],"c:w:",["cat=","wiki="])
    except getopt.GetoptError:
        print("Could not parse arguments")
        sys.exit(2)

    wikiID = ""
    category = ""
    
    for opt,arg in opts:
        if opt == "-w" or opt == "--wiki":
            wikiID = arg
        if opt == "-c" or opt == "--cat":
            category = arg

    if not (wikiID and category):
        print("Need two arguments: wikiID and category. Specify with -w/--wiki <wikiID> and -c/--cat <category name>. Exiting")
        sys.exit(2)
    else:
        return wikiID, category

def touchPagesInCategory(site,category):
    global logMessages

    # null edit pages in the category
    query = "[[Category:" + category + "]]"
    for answer in site.ask(query):
       pagename = getValue(answer,'fulltext')
       print("touching " + pagename)
       logMessages = logMessages + "touching [[" + pagename + "]]<br/>"
       page = site.pages[pagename]
       page.touch()

def main(*args) -> None:
    # get details and login
    wikiID, category = getArguments()
    site = login(wikiID, onVM=onVM)
    touchPagesInCategory(site,category)    

    print("Saving log...")
    if category:
        saveLog(site,"Category talk:" + category,"Touch",logMessages)
    print("Script execution complete.")


if __name__ == '__main__':
    main()

# end
