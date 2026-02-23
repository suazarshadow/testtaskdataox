from lxml import html
import re

class Parser:
    def parse_listing_page(self, html_page: str):
        tree = html.fromstring(html_page)

        links = tree.xpath('//a[@class="link product-card horizontal"]')
        not_sold_links = []

        for link in links:
            sold_badge = link.xpath('.//span[contains(@class,"common-badge alpha medium") and contains(.,"Авто продано")]')
            if sold_badge:
                continue  

            href = link.get("href")
            not_sold_links.append(href)
        return not_sold_links

    def parse_all_info(self, html_page: str):
        tree = html.fromstring(html_page)
        
        title_element = tree.xpath('//h1[contains(@class,"titleL")]')
        title = None
        if title_element:
            title = title_element[0].text_content().replace("<!--[-->","").replace("<!--]-->","").strip()
        
        price_element = tree.xpath('//div[@id="basicInfoPrice"]//strong[contains(@class,"titleL")]')
        price_usd = None
        if price_element:
            price_usd = price_element[0].text_content().replace("<!--[-->","").replace("<!--]-->","").replace("$","").replace("\xa0","").strip()

        odometer_element = tree.xpath('//span[contains(@class,"body") and contains(text(),"км")]')
        odometer = None
        if odometer_element:
            odometer_raw = odometer_element[0].text_content().replace("\xa0", "").strip() 

            if "тис" in odometer_raw:
                odometer = int(re.sub(r"\D", "", odometer_raw)) * 1000
            else:
                odometer = int(re.sub(r"\D", "", odometer_raw))   

        username_element = tree.xpath('//div[@id="sellerInfoUserName"]//span[contains(@class,"titleM")]')
        username = None
        if username_element:
            username = username_element[0].text_content().replace("<!--[-->","").replace("<!--]-->","").strip()
        
        phone_element = tree.xpath('//a[starts-with(@href,"tel:")]')
        phone_number = None
        if phone_element:
            phone_number = int('38' + re.sub(r"\D", "", phone_element[0].get("href").replace("tel:","").strip()))

        image_element = tree.xpath('//div[@id="photoSlider"]//li[contains(@class,"carousel__slide--active")]//img/@src')       
        image_url = None
        if image_element:
            image_url = image_element[0].strip()
        
        images_count_element = tree.xpath('//span[contains(@class,"common-badge")]//span[2]')
        images_count = None
        if images_count_element:
            images_count = images_count_element[0].text_content().strip()

        car_number_element = tree.xpath('//div[contains(@class,"car-number")]//span[contains(@class,"common-text")]')
        car_number = None
        if car_number_element:
            car_number = car_number_element[0].text_content().replace("<!--[-->","").replace("<!--]-->","").strip()

        car_vin_element = tree.xpath('//div[@id="badgesVin" or contains(@class,"badge-template")]//span[contains(@class,"common-text")]')
        car_vin = None
        if car_vin_element:
            car_vin = car_vin_element[0].text_content().replace("<!--[-->","").replace("<!--]-->","").strip()    
        
        data = {
            "title": title,
            "price_usd": price_usd,
            "odometer": odometer,
            "username": username,
            "phone_number": phone_number,
            "image_url": image_url, 
            "images_count": images_count,
            "car_number": car_number,
            "car_vin": car_vin,
        }
        
        return data