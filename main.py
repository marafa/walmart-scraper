import requests
from bs4 import BeautifulSoup
import csv

def query_user():
    print("Enter the search here: ")
    # arrange the query in the right order to concatenate to url
    search_query = input().lower().split()
    full_query = ""
    for i in range(len(search_query)):
        full_query = full_query + "+" + search_query[i]
    full_query = full_query[1:]

    url = "https://www.walmart.com/search/?query=" + full_query

    r = requests.get(url)
    if(r.ok):
        csvfilename = full_query.replace("+", "")
        csvfilename += ".csv"
        return url
    else:
        print("Bad search. Check your search or try again")
        return

def get_page(url):
    try:
        response = requests.get(url);
        soup = BeautifulSoup(response.text, "lxml")

        return soup
    except:
        print("PRODUCT PAGE NOT FOUND")
        return


def get_details(soup):
    # titles
    # links to products
    # prices

    try:
        titles = soup.find_all("a", {"class" : "product-title-link"}) # list of all titles
        # titles[i]['title'] to get the content of the 'title' attribute
    except:
        titles = "No title found"

    try:
        links = soup.find_all("a", {"class" : "product-title-link"}) # need to prefix each link with "walmart.com/"
        # links[i]['href'] to get the content of the 'href' attribute
    except:
        links = "No link found"

    try:
        prices = soup.find_all("div", {"class" : "price-main-block"})
        # prices[i].text to get the price in text
    except:
        prices = "No price found"

    return titles, links, prices

def create_dictionary(details):
    # put the needed details from titles, links, and prices, into their own lists
    # titles    = details[0]
    # links     = details[1]
    # prices    = details[2]
    titlesList  = []
    linksList   = []
    pricesList  = []

    for title in details[0]:
        titlesList.append(title["title"])

    for link in details[1]:
        fullLink = "https://walmart.com" + link["href"]
        linksList.append(fullLink)

    for price in details[2]:
        pricesList.append(price.text)


    # print(len(titlesList))
    # print(len(linksList))
    # print(len(pricesList))

    # if((len(titlesList) == len(linksList)) and (len(titlesList) == len(pricesList))):
    #     equalListLength = len(titlesList)
    # else:
    #     print("Some or More list(s) is/are incorrect")

    #[titles:0, links:1, prices:2]
    detailsdict = {
        "title" : titlesList,
        "link" : linksList,
        "price" : pricesList,
        "length" : len(titlesList)
    }

    return detailsdict

def create_csv_file(detailsdict, newline = " "):
    with open("output.csv", "a") as csvfile:
        row = ["PRODUCT NAME", "PRODUCT LINK", "PRICE"]
        writer = csv.writer(csvfile)
        writer.writerow(row)
        for i in range(detailsdict["length"]):
            row = [detailsdict["title"][i], detailsdict["link"][i], detailsdict["price"][i]]
            writer.writerow(row)

def main():
    page = get_page(query_user())
    # page = get_page(url)
    details = get_details(page)
    create_csv_file(create_dictionary(details))

main()
