#WebsiteUrl - link, SiteUrl - bool needs resolving, Cookie - opt cookie header
def WebsiteRequest(WebsiteUrl,SiteUrl=0, Cookie=''):
    import urllib
    from urllib.request import Request, urlopen

    HtmlPage = None
    RealUrl= None
    try:
        # ToDo: GET TRUE URL
        WebsiteResponse = Request(WebsiteUrl, headers={'User-Agent': 'Mozilla/5.0', 'Cookie': Cookie})
        WebsiteOpen=urlopen(WebsiteResponse)
        if(SiteUrl):
            RealUrl=((WebsiteOpen.geturl()).split("/?"))[0]
        HtmlPage = WebsiteOpen.read().decode('utf-8')
    except Exception:
        print('Website fora do ar:',WebsiteUrl)
        # WebsiteRequest = Request(WebsiteUrl, headers={'User-Agent': 'Mozilla/5.0'})
    return [HtmlPage,RealUrl]

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

    CartId = CurrentSiteAndCurrentCardHtml.split("ajax/cardsearch.php?idLoja=")[1].split("'",1)[0]

    return [UnorderedAndWithoutTheCorrectNumberOfCardsListOfPricesOfCards,CartId]
    
def FindBestShippingForSite(SiteAddress, BaseShippingRegex, Cookie):
    from re import findall
    print("Card Address: "+SiteAddress+"\n\n")
    CurrentCartShippingCostsHtml=WebsiteRequest(SiteAddress,0,Cookie)[0]
    if CurrentCartShippingCostsHtml == None:
        return ([1000000.00,-2], [[0,0]])
    print(CurrentCartShippingCostsHtml)
    BaseShipping=[list(j) for j in findall(BaseShippingRegex,CurrentCartShippingCostsHtml)]
    BestShippingPosition=[1000000.00,-1]
    for i in range(len(BaseShipping)):
        print("BaseShipping["+str(i)+"]: "+str(BaseShipping[i]))
        # Ignoring 'frete gratis'
        if (BaseShipping[i][0] == ''):
            BaseShipping[i][0] = '0'
        if (BaseShipping[i][1] == ''):
            BaseShipping[i][1] = '0'
        if((float(BaseShipping[i][0])-float(BaseShipping[i][1])) and (float(BaseShipping[i][0])<BestShippingPosition[0])):
            BestShippingPosition=[float(BaseShipping[i][0]),i]
            print("yep")
    return (BestShippingPosition, BaseShipping)

def BuySubCardAndRetrieveItsCookie(WebsiteUrl, SubCard):
    UrlBaseName=['/ajax/ecom/carrinho.php?t=1&id=','&q=1']
    BuyReqAddress=WebsiteUrl.split('/ajax',1)[0]+UrlBaseName[0]+SubCard+UrlBaseName[1]

    print('WebsiteUrl:', WebsiteUrl)
    print('SubCard:', SubCard)

    print('Requesting coookieeee:', BuyReqAddress)
    CookieHtmlRes=WebsiteRequest(BuyReqAddress)[0]

    print('Cookie/HTML', CookieHtmlRes)

    CookieValue = CookieHtmlRes.split("value='",1)[1].split("'",1)[0]
    Cookie = 'carrinhoEcom=' + CookieValue

    return Cookie

def FindShippingPrice(ListOfSitesAddresses,ListOfCartsIds, SubCardList):
    UrlBaseName=['/ajax/ecom/frete.php?id=','&cep=69945000&vTotal=100&idEnd=-1']
    ListOfCartAddresses=[ ListOfSitesAddresses[i]+UrlBaseName[0]+ListOfCartsIds[i]+UrlBaseName[1] for i in range(len(ListOfSitesAddresses))]
    ShippingList=[]

    BaseShippingRegex=r"""v='(.*?)' s='(.*?)' """

    #Nos sites de forma geral, quando temos "v='x'", x eh o valor total do frete e "s='y'" eh o valor do seguro
    #CurrentCardId=search(GeneralCardIdRegex,CurrentCardHtmlPage,DOTALL).group(0) # Find the Id of the Current Card

    #Problema pois alguns dos sites precisam que voce compre algo para poder acessar o carrinho e ver o valor do frete e do seguro

    Cookie = ''

    for ind in range(len(ListOfCartAddresses)):
        SiteAddress = ListOfCartAddresses[ind]
        BestShippingPosition, BaseShipping = FindBestShippingForSite(SiteAddress, BaseShippingRegex, Cookie)
        if(BestShippingPosition[1]==-1): #Site requer cookie
            Cookie = BuySubCardAndRetrieveItsCookie(ListOfCartAddresses[ind], SubCardList[ind])
            print('Retrieved Cookie:',Cookie);
            BestShippingPosition, BaseShipping = FindBestShippingForSite(SiteAddress, BaseShippingRegex, Cookie)
        elif BestShippingPosition[1] == -2: #Site fora do ar
            ShippingList.append([1000000.00, 1000000.00])
            continue
        
        print("BestShippingPosition[1]: "+str(BestShippingPosition[1])+"; BaseShipping[Do que eu mostri agr a pouco][0]: "+str(BaseShipping[(BestShippingPosition[1])][0])+"; BaseShipping[Do que eu mostri agr a pouco][0]: "+str(BaseShipping[(BestShippingPosition[1])][1]))
        BestShipping=[( float(BaseShipping[(BestShippingPosition[1])][0])-float(BaseShipping[(BestShippingPosition[1])][1])),(1.00 + (float(BaseShipping[(BestShippingPosition[1])][1])/100))]    
        ShippingList.append(BestShipping)

    return ShippingList

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
    ListOfCartsIds=[]
    ErrorSites=[]
    ListOfSitesAddresses=[]
    SubCardList=[]
    DeckHtmlPage = WebsiteRequest(WebsiteUrl,0)[0] #List of Cards HTML Page

    ListOfCards=FindCardNames(0,DeckHtmlPage) #Find list of cards
    tobreak=0
    for i in range(len(ListOfCards)):
    #for i in range(1):
        if(tobreak):
            break
        print(str(i+1)+"/"+str(len(ListOfCards)))
        CurrentCardHtmlPage=WebsiteRequest(ListOfCards[i][2],0)[0] # Card 'i' HTML Page
        FindCardId(i,ListOfCards,CurrentCardHtmlPage) # Append the card Id to the 'ListOfCards[i]'
        ListOfTheSitesOfTheCurrentCard=FindSiteNames(ListOfSites,CurrentCardHtmlPage) # Append the List of the sites of the Current card
        for j in range(len(ListOfTheSitesOfTheCurrentCard)):
            # if(not ListOfTheSitesOfTheCurrentCard[j][0].startswith('DeckMasterGames')):
            #     print('Pulei',ListOfTheSitesOfTheCurrentCard[j][0])
            #     continue
            # tobreak=1
            # print('AAAAAAAAAAAAAAAAAA',ListOfTheSitesOfTheCurrentCard[j][1] )
            print("\t"+str(j+1)+"/"+str(len(ListOfTheSitesOfTheCurrentCard)))
            IsANewSite=0
            if(not(ListOfTheSitesOfTheCurrentCard[j][0] in ListOfSites)):
                IsANewSite=1
           
            if (ListOfTheSitesOfTheCurrentCard[j][0] not in ErrorSites):
                
                CurrentSiteAndCurrentCardHtmlAndRealUrl = WebsiteRequest(ListOfTheSitesOfTheCurrentCard[j][1],IsANewSite)
                CurrentSiteAndCurrentCardHtml = CurrentSiteAndCurrentCardHtmlAndRealUrl[0]
                if (CurrentSiteAndCurrentCardHtml != None):
                    if(IsANewSite):
                        SubCardList.append(ListOfTheSitesOfTheCurrentCard[j][1].split('/?p=e',1)[1])
                        ListOfSites.append(ListOfTheSitesOfTheCurrentCard[j][0])
                        PricesList.append([[ValueOfUnavailableCards for j in range(int(i[0]))] for i in ListOfCards])
                        ShippingList.append([BaseShipping,BaseAssurance])
                        print("Card: "+ListOfCards[i][1]+"; Site: "+ListOfSites[-1]+"\n")
                        PriceAndCartId=FindPricesValues(CurrentSiteAndCurrentCardHtml,int(ListOfCards[i][0]))
                        PricesList[-1][i]=PriceAndCartId[0]
                        print(PricesList[-1][i])
                        ListOfSitesAddresses.append((CurrentSiteAndCurrentCardHtmlAndRealUrl[1].split("/?",1))[0])
                        ListOfCartsIds.append(PriceAndCartId[1])
                        print(ListOfSites[-1]+" // "+ListOfSitesAddresses[-1]+" // "+ListOfCartsIds[-1]+"\n")
                    else:    
                        PricesList[ListOfSites.index(ListOfTheSitesOfTheCurrentCard[j][0])][i] = FindPricesValues(CurrentSiteAndCurrentCardHtml,int(ListOfCards[i][0]))[0]

                else:
                    ErrorSites.append(ListOfTheSitesOfTheCurrentCard[j][0])
                    print('Blacklisting',ListOfTheSitesOfTheCurrentCard[j][0])
                    print('url was:',ListOfTheSitesOfTheCurrentCard[j][1])
            else:
                print('Blacklisted!!:', ListOfTheSitesOfTheCurrentCard[j][0])
            # break
    with open('outAddrSa.txt', 'w') as f:
        f.write(str(ListOfSitesAddresses))
    with open('outAddrCi.txt', 'w') as f:
        f.write(str(ListOfCartsIds))
    with open('outSCL.txt', 'w') as f:
        f.write(str(ListOfCartsIds))

    # ListOfSitesAddresses=['https://elderdragonbrasil.com.br', 'https://www.letscollect.com.br', 'https://www.reinomagic.com.br', 'https://www.houseofcardstcg.com.br', 'https://www.neowalkers.com', 'https://www.mulligangames.com.br', 'https://www.ligamagic.com.br', 'https://www.ligamagic.com.br', 'https://www.mtgcardsgames.com.br', 'https://goblinfactory.com.br', 'https://www.vampirextcg.com.br', 'https://www.cardsofparadise.com.br', 'https://lojagrimorium.com.br', 'https://www.lojailusoes.com.br', 'https://www.ligamagic.com.br', 'https://www.tokenlandiacards.com.br', 'https://lojabloodmoon.com.br', 'https://www.manavaibr.com.br', 'https://www.kinoenecards.com.br', 'https://www.lojacavernadodragao.com.br', 'https://www.tcgeek.com.br', 'https://umtg.com.br', 'https://www.cardtutor.com.br', 'https://www.cardcastle.com.br', 'https://www.chucktcg.com.br', 'https://www.spellcastgames.com.br', 'https://www.chq.com.br', 'https://www.medievalcards.com', 'https://playersstoptcg.com', 'https://www.hivejogos.com.br', 'https://www.magicclubtcg.com.br', 'https://www.mineralgames.com.br', 'https://pharaohshoptcg.com.br', 'https://loadorcast.com', 'https://www.ligamagic.com.br', 'https://www.ligamagic.com.br', 'https://www.bazardebagda.com.br', 'https://www.magicbembarato.com.br', 'https://www.worldcardgames.com.br', 'https://www.playgroundgames.com.br', 'https://www.under3.com.br', 'https://www.konklavecards.com', 'https://www.mtgbrasil.com.br', 'https://www.magicstorebrasil.com.br', 'https://magicdomain.com.br', 'https://www.treasurecards.com.br', 'https://www.joguemagic.com.br', 'https://www.cardshall.com.br', 'https://www.miragemhobby.com.br', 'https://www.gideonspalace.com.br', 'https://www.flowstore.com.br', 'https://www.pigamescard.com', 'https://www.insidegamestore.com', 'https://www.padrinhocs.com.br', 'https://www.overrun.com.br', 'https://territoriocardgames.com.br', 'https://www.epicgame.com.br', 'https://www.pugames.com.br', 'https://www.nerdzcards.com.br', 'https://www.xplace.com.br', 'https://www.cardsoutlet.com.br']
    # ListOfCartsIds=['7362', '33351', '43303', '63802', '129419', '32645', '127399', '180886', '15760', '108628', '384', '26393', '34713', '58734', '45050', '47012', '61540', '48121', '859', '112710', '153688', '75923', '117638', '142433', '61249', '32448', '29521', '81837', '57673', '156276', '30155', '9781', '155555', '75744', '200600', '109333', '56925', '26414', '159647', '84075', '172866', '34598', '88876', '52667', '90095', '45334', '22834', '97306', '62881', '110925', '82238', '71287', '82842', '93441', '25716', '64459', '461', '95560', '150020', '32035', '92229']
    print(len(ListOfSitesAddresses), len(ListOfCartsIds))
    ShippingList=FindShippingPrice(ListOfSitesAddresses,ListOfCartsIds, SubCardList)
    print("THE END\n")


Webpage=input("Insira abaixo o endereço virtual do seu deck no site 'Ligamagic'\n")

GeneralListFunction(Webpage,0)

# Developed in discord, waiting for new features coming in future commit from @E3-7

# Code working, but variables aren't present in this commit
