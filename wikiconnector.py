import requests
import webbrowser
import urllib.parse



def wiki_get_proverbs():
    morePages = True
    apiProverbs = 'https://pl.wiktionary.org/w/api.php?'
    cmcontinue = str()
    proverbs = list()
    apiParams = {
        'format' : 'json',
        'action' : 'query',
        'list' : 'categorymembers',
        'cmtitle' : 'Category:Polskie_przysłowia',
        'cmprop' : 'title',
        'cmlimit' : 'max'
    }
    while morePages is True:
        try:
            query = requests.get(apiProverbs + cmcontinue, apiParams)
            query = query.json()
        except requests.exceptions.ConnectionError:
            connectionError = None
            break
        for entry in query['query']['categorymembers']:
            if (entry['ns'] == 0):
                proverbs.append(entry['title'])
        try:
            cmcontinue = query['continue']['cmcontinue']
            cmcontinue = '&cmcontinue=' + cmcontinue
        except KeyError:
            morePages = False
    if (len(proverbs) > 0):
        return proverbs
    elif (connectionError):
        return connectionError


def wiki_proverb_info(proverb):
    wikiLink = 'https://pl.wiktionary.org/wiki/'
    proverb = urllib.parse.quote(proverb)
    webbrowser.open_new_tab(wikiLink + proverb)
