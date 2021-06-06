import requests
from bs4 import BeautifulSoup
import pandas

page_nomax = 3
scrapped_info = []
oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

for page_no in range(page_nomax):
    req = requests.get(oyo_url, headers = header)

    content = req.content
    soup = BeautifulSoup(content,"html.parser")

    all_hotels = soup.find_all("div",{"class":"oyo-row oyo-row--no-spacing hotelCardListing"})

    for hotel in all_hotels:

        hotel_dict = {}
        amenitylist = []

        hotel_dict["name"] = hotel.find("h3",{"class":"listingHotelDescription__hotelName d-textEllipsis"}).text
        hotel_dict["address"] = hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict["price"] = hotel.find("span",{"class":"listingPrice__finalPrice"}).text
        #####################################RATING##################################################
        try :
            hotel_dict["raring"] = hotel.find("span",{"class":"is-fontBold hotelRating__rating hotelRating__rating--verygood hotelRating__rating--clickable"}).text
        except AttributeError:
            pass
        #-------------------------------------**********---------------------------------------------#

        #####################################AMENTIES#################################################
        parant_amenty_element = hotel.find("div",{"class":"amenityWrapper"})
        for amenty_element in parant_amenty_element.find_all("div",{"class":"amenityWrapper__amenity"}):
            try:
                amenitylist.append(amenty_element.find("span",{"class":"d-body-sm d-textEllipsis"}).text.strip())
            except:
                amenitylist.append(amenty_element.find("span",{"class":"d-body-sm"}).text.strip())
        hotel_dict["amenties"] = ", ".join(amenitylist[:-1])
        #-------------------------------------*************------------------------------------------#

        scrapped_info.append(hotel_dict)

dataframe = pandas.DataFrame(scrapped_info)
dataframe.to_csv("oyo.csv")
