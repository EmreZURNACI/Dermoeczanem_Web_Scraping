import time
from math import ceil

from selenium import webdriver
from selenium.webdriver.common.by import By

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("detach", True)
driver = webdriver.Chrome(chromeOptions)
driver.get("https://www.dermoeczanem.com/")
driver.maximize_window()
driver.implicitly_wait(3)
kategorilerVeAdetleri = list()
linkYorumAdetYildiz = list()
yorumlarDizisi = list()
markaListesi = list()
def beklet(zaman):
    time.sleep(float(zaman))


def linklestir(string):
    return str(string).lower().strip().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace(
        'ö', 'o').replace(
        'ş', 's').replace('ü', 'u')


def reklamlarıTemizle():
    try:
        driver.find_element(By.CLASS_NAME, "close-button").click()
        driver.find_element(By.ID, "web_push_hayir").click()
        driver.find_element(By.ID, "headeradsclose").click()
        driver.find_element(By.ID, "cookieClose_").click()
        beklet(1)
    except:
        pass


def ilgiliKategoriyeUlasma():
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/header/div/div[6]/div[3]/div/div/ul/li[5]/a").click()
    beklet(1)
    driver.find_element(By.XPATH,
                        "/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[1]/div/div[2]/div/ul/li/ul/li/ul/li[12]/a").click()


def kategorilerAdetleri():
    """KATEGORİ ADLARI VE ONA AİT ADETLER ALINDI LİSTEDE BİRLEŞTİRİLDİ"""
    kategoriAdet = len(driver.find_elements(By.XPATH,
                                            "/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[1]/div/div[2]/div/ul/li/ul/li/ul/li"))
    for i in range(kategoriAdet):
        kategorilerVeAdetleri.append(
            [
                driver.find_element(By.XPATH,
                                    f"/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[1]/div/div[2]/div/ul/li/ul/li/ul/li[{i + 1}]/a/span").text
                ,
                int(driver.find_element(By.XPATH,
                                        f"/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[1]/div/div[2]/div/ul/li/ul/li/ul/li[{i + 1}]/a/font").text.split(
                    "(")[1].split(")")[0])
            ]
        )


def markalariGetir():
    # Marka adeti bulur ve bütün markaları listeye çeker.
    markaAdedi = len(driver.find_elements(By.XPATH,
                                          "/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[2]/div/ul/li"))
    for i in range(markaAdedi):
        markaListesi.append(driver.find_element(By.XPATH,
                                                f"/html/body/div[1]/div[1]/div/div/div/div/aside/div/div[5]/div/div/div[2]/div/div[2]/div/ul/li[{i + 1}]/label").text.split(
            "(")[0])


def linklerYildizlarYorumlar():
    #ürünlerin her birisinin linkini,adı,yorum adedini ve ort yıldzı listeye ekler
    sayac = 0
    for i, item in enumerate(kategorilerVeAdetleri):
        driver.get(f"https://www.dermoeczanem.com/{linklestir(item[0])}?pg={1}")
        yildizSayac = 0
        beklet(2)
        sayfadakiUrunAdeti = len(driver.find_elements(By.CSS_SELECTOR,
                                                      ".catalogWrapper div.col.col-3.col-md-3.col-sm-3.col-xs-6.productItem.ease"))
        for i in range(sayfadakiUrunAdeti):
            linkYorumAdetYildiz.append(
                [
                    # ürünün linki
                    driver.find_elements(By.CSS_SELECTOR,
                                         ".catalogWrapper div.col.col-3.col-md-3.col-sm-3.col-xs-6.productItem.ease a.image-wrapper")[
                        i].get_attribute("href"),
                    #ürünün adı
                    driver.find_elements(By.CSS_SELECTOR, "div.proRowName div.row a")[i].get_attribute("title")
                ]
            )
            #ürünün adı ve ürünün yorum adedi olan bir üst dive eriştik,ürüne herhangi bir yorum yapıldı mi kontrol edildi
            element_text = driver.find_elements(By.CSS_SELECTOR, "div.proRowName div.row")[i].text
            if "(" in element_text:
                # ürünün yorum adedi
                linkYorumAdetYildiz[sayac].append(int(element_text.split(")")[0].split("(")[1]))
                # ürünün ortalama yıldızı
                linkYorumAdetYildiz[sayac].append("{:.2f}".format((float(str(driver.find_elements(By.CSS_SELECTOR, "div.stars div.fl.stars-inner")[yildizSayac].get_attribute("style")).split(":")[1].split("%")[0]))/20))
                yildizSayac += 1
            else:
                linkYorumAdetYildiz[sayac].append(int(0))
                linkYorumAdetYildiz[sayac].append(float(0))
            sayac += 1

def yorumlariGetir():
    #listeye atılan ürün linklerinin her birini dolaşarak yorumları,yorum tarihini ve yorum yıldızını çeker
    for i, item in enumerate(linkYorumAdetYildiz):
        driver.get(item[0])
        beklet(2)
        driver.find_element(By.CLASS_NAME, "comment-btn").click()
        beklet(1 / 4)
        yorumlarYildizlarTarihleri = list()
        #Ürünün yorumları onarlı component şeklinde listelendiği için 10 defa next butonuna tıklayarak her seferinde farklı yorumların listelendiği componenti getirdik
        #boylece 10 * 10 'dan 100 adet yorum çekildi.
        if item[2] > 100:
            for i in range(10):
                for j in range(10):
                    if driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text.strip() == "" or len(
                            driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text.strip()) == 0:
                        yorumlarYildizlarTarihleri.append(
                            [
                                driver.find_elements(By.XPATH, '//div[@itemprop="name"]')[j].text,
                                driver.find_elements(By.XPATH, '//span[@itemprop="ratingValue"]')[j].get_attribute(
                                    "content"),
                                driver.find_elements(By.XPATH, '//div[@itemprop="datePublished"]')[j].text
                            ]
                        )
                    else:
                        yorumlarYildizlarTarihleri.append(
                            [
                                driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text,
                                driver.find_elements(By.XPATH, '//span[@itemprop="ratingValue"]')[j].get_attribute(
                                    "content"),
                                driver.find_elements(By.XPATH, '//div[@itemprop="datePublished"]')[j].text
                            ]
                        )
                        beklet(0.25)
                try:
                    driver.find_element(By.CLASS_NAME, "nextPage").click()
                    beklet(1.5)
                except:
                    pass
        else:
            for i in range(ceil(item[2] / 10)):
                for j in range(0, len(driver.find_elements(By.CSS_SELECTOR,
                                                           f"#commentTabContent > div.col.col-12.comment-list > div > div > div > div > div:nth-child(6)"))):
                    if driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text.strip() == "" or len(
                            driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text.strip()) == 0:
                        yorumlarYildizlarTarihleri.append(
                            [
                                driver.find_elements(By.XPATH, '//div[@itemprop="name"]')[j].text,
                                driver.find_elements(By.XPATH, '//span[@itemprop="ratingValue"]')[j].get_attribute(
                                    "content"),
                                driver.find_elements(By.XPATH, '//div[@itemprop="datePublished"]')[j].text
                            ]
                        )
                    else:
                        yorumlarYildizlarTarihleri.append(
                            [
                                driver.find_elements(By.XPATH, '//div[@itemprop="description"]')[j].text,
                                driver.find_elements(By.XPATH, '//span[@itemprop="ratingValue"]')[j].get_attribute(
                                    "content"),
                                driver.find_elements(By.XPATH, '//div[@itemprop="datePublished"]')[j].text
                            ]
                        )
                    beklet(0.25)
                try:
                    driver.find_element(By.CLASS_NAME, "nextPage").click()
                    beklet(1.5)
                except:
                    pass
        yorumlarDizisi.append(yorumlarYildizlarTarihleri)


def enCokYorumlanan():
    return sorted(linkYorumAdetYildiz, key=lambda x: x[2], reverse=True)[0]


def enCokSevilen():
    return sorted(linkYorumAdetYildiz, key=lambda x: x[3], reverse=True)[0]


def benzersizleştir():
    seen = set()
    unique_list = []

    for sublist in linkYorumAdetYildiz:
        first_element = sublist[0]
        if first_element not in seen:
            seen.add(first_element)
            unique_list.append(sublist)


def yorumsuzlariSil():
    linkYorumAdetYildiz[:] = [alt_liste for alt_liste in linkYorumAdetYildiz if alt_liste[2] != 0]


reklamlarıTemizle()
ilgiliKategoriyeUlasma()
markalariGetir()
kategorilerAdetleri()
linklerYildizlarYorumlar()
benzersizleştir()
yorumsuzlariSil()
yorumlariGetir()
print("En Cok Yorumlanan",enCokYorumlanan())
print("En cok yıldızlanan",enCokSevilen())
