def WebsiteRequest(WebsiteUrl):
    import urllib2
    from urllib2.request import Request, urlopen

    HtmlPage = None
    try:
        # TODO: GET TRUE URL
        WebsiteResponse = Request(WebsiteUrl, headers={'User-Agent': 'Mozilla/5.0'})
        HtmlPage = urlopen(WebsiteResponse).read().decode('utf-8')
        print(dir(HtmlPage))
        # print(HtmlPage.geturl())
    except Exception as e:
        print('Website fora do ar:',WebsiteUrl)
        # WebsiteRequest = Request(WebsiteUrl, headers={'User-Agent': 'Mozilla/5.0'})
    return HtmlPage

def FindCardNames(SiteType,DeckHtmlPage):
    from re import findall
    
    UnaccountedCards=["Island","Swamp","Mountain","Plains","Forest"]
    
    if(SiteType): #Other sites possible regex'es
        RegexToFindTheListOfCards=r"""Aqui voce insere o regex necessario para achar cada carta no teu site"""
    else:  #Ligamagic regex to find a card
        RegexToFindTheListOfCards=r"""class='deck-qty'>([1-9][0-9]*?)&.*?&card=(.*?)">"""
    
    ListOfCards=[list(i) for i in (list(set(findall(RegexToFindTheListOfCards,DeckHtmlPage))))] #Find all the cards
    ListOfCards=[[i[0],i[1],("https://www.ligamagic.com.br/?view=cards/card&card="+(i[1].replace(" ","%20")))] for i in ListOfCards]
    for i in UnaccountedCards: #Remove basic lands from the list of cards
        if i in [j[1] for j in ListOfCards]:
            del ListOfCards[[j[1] for j in ListOfCards].index(i)]
            
    #ListOfCards[i][0] = Card 'i' number of repetitions
    #ListOfCards[i][1] = Card 'i' name
    #ListOfCards[i][2] = Card 'i' website name
    #ListOfCards[i][3] = Card 'i' Id

    return ListOfCards

def FindCardId(CurrentPosition,ListOfCards,CurrentCardHtmlPage):
    from re import search
    from re import DOTALL

    GeneralCardIdRegex=r"""value='([0-9]+)'></div>.*?<div id='card-menu'>.*?<a href="[.]/[?]view=cards/card&card="""
    CurrentCardId=search(GeneralCardIdRegex,CurrentCardHtmlPage,DOTALL).group(0) # Find the Id of the Current Card
    ListOfCards[CurrentPosition].append(CurrentCardId)

def FindSiteNames(ListOfSites,CurrentCardHtmlPage):
    from re import findall

    ListOfTheSitesOfTheCurrentCard=[]
    ListOfRepeatedSitesOfTheCurrentCard=[list(i) for i in (findall(r"""<a href='b/[?]p=(.*?)' target='.*?'><img title="(.*?)" src='//www[.]lmcorp[.]com""", CurrentCardHtmlPage))]
    ListOfRepeatedNamesOfTheSitesOfTheCurrentCard=[i[1] for i in ListOfRepeatedSitesOfTheCurrentCard]
    ListOfNamesOfTheSitesOfTheCurrentCard=list(set(ListOfRepeatedNamesOfTheSitesOfTheCurrentCard))

    for i in ListOfNamesOfTheSitesOfTheCurrentCard:
        ListOfTheSitesOfTheCurrentCard.append([i,("https://www.ligamagic.com.br/b/?p="+(ListOfRepeatedSitesOfTheCurrentCard[ListOfRepeatedNamesOfTheSitesOfTheCurrentCard.index(i)][0]))])

    #ListOfTheSitesOfTheCurrentCard[i][0] = Site 'i' website address in respect to the Current card
    #ListOfTheSitesOfTheCurrentCard[i][1] = Site 'i' website name in respect to the Current card

    return ListOfTheSitesOfTheCurrentCard

def FindPricesValues(CurrentSiteAndCurrentCardHtml,NumberOfCopiesOfTheCurrentCard):
    from re import findall
    from re import DOTALL
    PoorSiteNormalPriceRegex=r"""<td class='hmin30 [brdt]*?'>([0-9]+?) unid[.]</td>\s*?<td class='itemPreco hmin30 [brdt]*?'>R[$] ([0-9]+?,[0-9]*?)</td>"""
    PoorSiteOnPromotionPriceRegex=r"""<td class='hmin30 [brdt]*?'>([0-9]+?) unid[.]</td>\s*?<td class='itemPreco hmin30 [brdt]*?' title='.*?<font color='.*?' style='.*?'>R[$] ([0-9]+?,[0-9]*?)</font>"""    
    RichSiteNormalPriceRegex=r"""<span class="product-price">([0-9]+?) unid[.]</span>\s*?</div>\s*?<div class=".*?<span class="product-price">R[$] ([0-9]+?,[0-9]*?)</span>"""
    RichSiteOnPromotionPriceRegex=r"""<span class="product-price">([0-9]+?) unid[.]</span>\s*?</div>\s*?<div class=".*?<span class="product-price">.*?<br/><font color='red'>R[$] ([0-9]+?,[0-9]*?)</font>"""    
    AllPriceRegexes=[PoorSiteNormalPriceRegex,PoorSiteOnPromotionPriceRegex,RichSiteNormalPriceRegex,RichSiteOnPromotionPriceRegex]

    UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards=[]
    for i in range(2):
        PricesOfCurrentSiteAndCurrentCardList=[list(k) for k in (findall(AllPriceRegexes[i],CurrentSiteAndCurrentCardHtml,DOTALL))]
        PricesOfCurrentSiteAndCurrentCardList=[[k[0],((k[1]).replace(",","."))] for k in PricesOfCurrentSiteAndCurrentCardList]
        #PricesOfCurrentSiteAndCurrentCardList[i][0]=Repetitions of the card 'i'
        #PricesOfCurrentSiteAndCurrentCardList[i][1]=Cost of the card 'i'
        for j in PricesOfCurrentSiteAndCurrentCardList:
            if(float(j[1])):
                for k in range(int(j[0])):
                    UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards.append(float(j[1]))
        
    if(UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards==[]):
        for i in range(2,4):
            PricesOfCurrentSiteAndCurrentCardList=[list(i) for i in (findall(AllPriceRegexes[i],CurrentSiteAndCurrentCardHtml,DOTALL))]
            PricesOfCurrentSiteAndCurrentCardList=[[i[0],((i[1]).replace(",","."))] for i in PricesOfCurrentSiteAndCurrentCardList]
            
            for j in PricesOfCurrentSiteAndCurrentCardList:
                if(float(j[1])):
                    for k in range(int(j[0])):
                        UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards.append(float(j[1]))

    UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards=(sorted(UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards))[:NumberOfCopiesOfTheCurrentCard]
    while((len(UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards))<NumberOfCopiesOfTheCurrentCard):
        UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards.append("1000000.00")
    return UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards
    

def FindShippingPrice(CurrentCardAndSiteUrl):
    # Pegar frete de um site (URL conhecido)
    url = CurrentCardAndSiteUrl
    caminhoBase1 = '/ajax/ecom/frete.php?id='
    cardSpecificID = '32035' #from button (not cardID)
    caminhoBase2 = '&cep=12215518&vTotal=10000&idEnd=-1'

    req = Request(url + caminhoBase1 + cardSpecificID + caminhoBase2, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read().decode('utf-8')

    print (page)


#PricesList[i] = Price in Site 'i'
#PricesList[i][j] = Price of the 'j' type of cards in site 'i'
#PricesList[i][j][k] = Price o the 'k'-th repetition of the 'j' type of card in site 'i'

#ShippingList[i] = Shippings in site 'i'
#ShippingList[i][0] = Base shipping cost in site 'i'
#ShippingList[i][1] = Assurance cost in site 'i'

def GeneralListFunction(WebsiteUrl,SiteType):
    from re import escape
    import os
    ValueOfUnavailableCards="1000000.00"
    BaseShipping="10.00"
    BaseAssurance="1000.00"
    PricesList=[]
    ShippingList=[]
    ListOfSites=[]
    ErrorSites=[]
    ListOfSitesAddresses=[]
    DeckHtmlPage = WebsiteRequest(WebsiteUrl) #List of Cards HTML Page

    ListOfCards=FindCardNames(0,DeckHtmlPage) #Find list of cards
    
    for i in range(len(ListOfCards)):
        print(str(i+1)+"/"+str(len(ListOfCards)))
        CurrentCardHtmlPage=WebsiteRequest(ListOfCards[i][2]) # Card 'i' HTML Page
        FindCardId(i,ListOfCards,CurrentCardHtmlPage) # Append the card Id to the 'ListOfCards[i]'
        ListOfTheSitesOfTheCurrentCard=FindSiteNames(ListOfSites,CurrentCardHtmlPage) # Append the List of the sites of the Current card
        for j in range(len(ListOfTheSitesOfTheCurrentCard)):
            print("\t"+str(j+1)+"/"+str(len(ListOfTheSitesOfTheCurrentCard)))

            if (ListOfTheSitesOfTheCurrentCard[j][0] != 'Goblin Factory'):
                continue

            if(not(ListOfTheSitesOfTheCurrentCard[j][1] in ListOfSites)):
                ListOfSites.append(ListOfTheSitesOfTheCurrentCard[j][0])
                ListOfSitesAddresses.append(ListOfTheSitesOfTheCurrentCard[j][1])
                PricesList.append([[ValueOfUnavailableCards for j in range(int(i[0]))] for i in ListOfCards])
                ShippingList.append([BaseShipping,BaseAssurance])
           
            if (ListOfTheSitesOfTheCurrentCard[j][0] not in ErrorSites):
                CurrentSiteAndCurrentCardHtml = WebsiteRequest(ListOfTheSitesOfTheCurrentCard[j][1])
                if (CurrentSiteAndCurrentCardHtml != None):
                    PricesList[ListOfSites.index(ListOfTheSitesOfTheCurrentCard[j][0])][i] = FindPricesValues(CurrentSiteAndCurrentCardHtml,int(ListOfCards[i][0]))
                else:
                    ErrorSites.append(ListOfTheSitesOfTheCurrentCard[j][0])
                    print('Blacklisting',ListOfTheSitesOfTheCurrentCard[j][0])
                    print('url was:',ListOfTheSitesOfTheCurrentCard[j][1])
            else:
                print('Blacklisted!!:', ListOfTheSitesOfTheCurrentCard[j][0])


    printf("THE END\n")



Webpage=input("Insira abaixo o endereço virtual do seu deck no site 'Ligamagic'\n")

All=(GeneralListFunction(Webpage,0))

# Developed in discord, waiting for new features coming in future commit from @E3-7

# Code working, but variables aren't present in this commit


