import os
import random
import time

fileName = "database.txt"
bank_accounts = {}
IDList = []
IBANList = []
TCIDList = []

def isDatabase(filename): # Dosya Kontrolü
    """
    The function isDatabase() checks whether there is any data read from the file
    """
    if os.path.isfile(filename) != 0:
        return True    
    else:
        return False

def fileWrite(accounts): # Dosya Yazma
    """
    The function fileWrite() writes data to the file by making it meaningful for the program to read.
    """
    with open(fileName, "w",encoding="utf-8") as file:
        for key in accounts.keys():
            file.write(key + "-")
            values = bank_accounts[key].values()
            for valuesItem in values:
                if isinstance(valuesItem, str):
                    file.write(valuesItem + "-")
                else:
                    accountlist = []
                    for item in valuesItem.items():
                        account = ":".join(map(str, item))
                        accountlist.append(account)
                    account = ",".join(map(str, accountlist))
                    file.write(account)
            file.write("\n")

def fileRead(accounts): # Dosya Okuma
    """
    The function fileRead() reads data from the file and converts it to the appropriate data type.
    """
    file = open(fileName, "r",encoding="utf-8")
    datas = file.readlines()
    file.close()
    for data in datas:
        data = data.strip("\n").split("-")
        IDList.append(data[0])  
        TCIDList.append(data[2])
        IBANdata = data[5].split(",")
        temp = {}
        temp["name surname"] = data[1]
        temp["tc id"] = data[2]
        temp["phone number"] =  data[3]
        temp["email address"] = data[4]
        temp["accounts"] = {}
        for item in IBANdata:
            item = item.split(":")
            IBANList.append(item[0])
            temp["accounts"].update({item[0]: item[1]})
        accounts[data[0]] = temp
    return accounts

def moneytransferaction(): # Para Transfer İşlemleri
    """
    The "moneytransferaction()" function is a function
    that transfers money between customers' own accounts or between customers' accounts.
    """
    global bank_accounts
    fileRead(bank_accounts)

    def accountsbetweentransfer():
        actionControl = None
        while actionControl == None:
            while True:
                try:
                    userBankID = input("Bank ID giriniz: ")
                    accounts = bank_accounts[userBankID]["accounts"]
                    break
                except KeyError:
                    print("Sistemde kayıtlı ID bulunamadı... Lütfen tekrar deneyiniz.")
                    time.sleep(2)
                    os.system("cls")
            accountDict = {}
            i = 0
            for account in accounts:
                i += 1
                accountDict[str(i)] = account
            while True:
                try:
                    print()
                    for key, value in accountDict.items():
                        print("     {}. : {} --> {}".format(key, value, accounts[value]))
                    selectionIndex = input("Gönderici hesabı seçiniz: ")
                    senderIBAN = accountDict[selectionIndex]
                    break
                except KeyError:
                    print("Yanlış hesap seçimi yapıldı. Lütfen tekrar deneyiniz.")
                    time.sleep(2)
                    os.system("cls")               
            while True:
                try:
                    senderMoney = int(input("Gönderilecek parayı giriniz: "))
                    break
                except ValueError:
                    print("Parayı uygun formatta giriniz.")
            senderBalance = int(bank_accounts[userBankID]["accounts"][senderIBAN])
            if senderMoney > senderBalance:
                print("Göndermek istediğiniz para seçtiğiniz hesabınızda yeteri kadar yok.")
                time.sleep(2)
                os.system("cls")
                continue
            IBANControl = False
            receiverID = None
            receiverIBAN = None
            print()
            while IBANControl == False:
                receiverIBAN = input("Alıcı IBAN giriniz: ")
                if len(receiverIBAN) == 12:
                    receiverIBAN = receiverIBAN[:4] + " " + receiverIBAN[4:8] + " " + receiverIBAN[8:]
                elif len(receiverIBAN) < 14 or len(receiverIBAN) > 14:
                    print("Yanlış formatta IBAN bilgisi lütfen tekrar deneyiniz.")
                    continue
                for key in bank_accounts.keys():
                    for account in bank_accounts[key]["accounts"]:
                        if receiverIBAN == account:
                            receiverID = key
                            IBANControl = True
                if IBANControl == False:
                    print("Alıcı IBAN bulunamadı.")
                    continue
            while True:
                assent = input("Para transfer işlemini onaylıyor musunuz?(E/H): ").upper()
                if assent in ["E", "H"]:
                    break
            if assent == "E":
                receiverBalance = int(bank_accounts[receiverID]["accounts"][receiverIBAN])
                receiverBalance += senderMoney
                senderBalance -= senderMoney
                bank_accounts[userBankID]["accounts"][senderIBAN] = senderBalance
                bank_accounts[receiverID]["accounts"][receiverIBAN] = receiverBalance
                print("Para transfer işlemi başarıyla tamamlanmıştır.")
                time.sleep(2)
                actionControl = "ç"
            elif assent == "H":
                print()
                print("İşleme baştan yapmak için ----> 1",
                      "İşlemden çıkmak için      ----> 2",sep="\n")
                while True:
                    action = input("İşlem seçimi: ")
                    if action in ["1", "2"]:
                        os.system("cls")
                        break
                if action == "1":
                    continue
                elif action == "2":
                    actionControl = "ç"

    def ownaccountsbetweentransfer():
        actionControl = None
        while actionControl == None:
            while True:
                try:
                    userBankID = input("Banka ID giriniz: ")
                    accounts = bank_accounts[userBankID]["accounts"]
                    break
                except KeyError:
                    print("Sistemde kayıtlı ID bulunmadı... Lütfen tekrar deneyiniz.")
                    time.sleep(2)
                    os.system("cls")
            if len(accounts) == 1:
                print(
                    "Sadece birden fazla sistemde kayıtlı banka hesabı olan müşteriler için bu işlem gerçekleştirilmektedir.")
                time.sleep(2)
                break
            accountsDict = {}
            i = 0
            for account in accounts:
                i += 1
                accountsDict[str(i)] = account
            while True:            
                try:
                    print()
                    for key, value in accountsDict.items():
                        print("     {}. : {} --> {}".format(key, value, accounts[value]))
                    selectionIndex1 = input("Gönderici hesabı seçiniz: ")
                    selectionAccount1 = accountsDict[selectionIndex1]
                    break
                except KeyError:
                    print("Yanlış hesap seçimi yapıldı. Lütfen tekrar deneyiniz.")
                    time.sleep(2)
                    os.system("cls")
            print()
            for key, value in accountsDict.items():
                if key != selectionIndex1:
                    print("     {}. : {} --> {}".format(key, value, accounts[value]))
            while True:
                try:
                    selectionIndex2 = input("Alıcı hesabı seçiniz: ")
                    selectionAccount2 = accountsDict[selectionIndex2]
                    if selectionAccount1 != selectionAccount2:
                        break
                    else:
                        print("Aynı hesabı üst üste seçim yapılamaz!!!")
                except KeyError:
                    print("Olmayan hesabı yaptınız. Lütfen tekrar deneyiniz.")
            while True:
                try:
                    sendBalance = int(input("Gönderilcek parayı giriniz: "))
                    break
                except ValueError:
                    print("Parayı uygun formatta giriniz.")
            accountBalance1 = int(accounts[selectionAccount1])
            accountBalance2 = int(accounts[selectionAccount2])
            if sendBalance > accountBalance1:
                print(
                    "Göndereceğiniz para gönderici hesabınızda yeterli bakiye bulunmamaktadır. Lütfen tekrar deneyniz.")
                time.sleep(2)
                os.system("cls")
                continue
            while True:
                assent = input("Para transfer işlemini onaylıyor musunuz?(E/H): ").upper()
                if assent in ["E", "H"]:
                    break
            if assent == "E":
                accountBalance1 -= sendBalance
                accountBalance2 += sendBalance
                accounts[selectionAccount1] = accountBalance1
                accounts[selectionAccount2] = accountBalance2
                bank_accounts[userBankID]["accounts"] = accounts
                print("Hesaplar arası para transferi işlemi başarı ile tamamlanmıştır.")
                time.sleep(2)
                actionControl = "ç"
            elif assent == "H":
                print()
                print("İşleme baştan yapmak için ----> 1",
                      "İşlemden çıkmak için      ----> 2", sep="\n")
                while True:
                    action = input("İşlem seçimi: ")
                    if action in ["1", "2"]:
                        os.system("cls")
                        break
                if action == "1":
                    continue
                elif action == "2":
                    actionControl = "ç"

    while True:
        print()
        print("Kendi hesaplarınız arasında transfer işlemleri için ----> 1",
              "Başka hesaplar arası transfer işlemleri için        ----> 2",
              "Ana menüye dönmek için                              ----> 3",sep="\n")
        action = input("İşlem seçimi: ")
        os.system("cls")
        if action == "1":
            ownaccountsbetweentransfer()
        elif action == "2":
            accountsbetweentransfer()
        elif action == "3":
            break
        fileWrite(bank_accounts)
        os.system("cls")

def moneyaction(): # Para Yatırma ve Çekme İşlemleri
    """
    The 'moneyAction' function is the function that performs
    withdrawal or deposit operations on customer bank accounts.
    """
    global bank_accounts
    fileRead(bank_accounts)
    banknotes = ("5", "10", "20", "50", "100", "200")
    
    def invenstment():  # Para Yatırma
        while True:
            try:
                userBankID = input("Banka ID giriniz: ")
                accounts = bank_accounts[userBankID]["accounts"]
                break
            except KeyError:
                print("Sistemde kayıtlı ID bulanamadı... Lütfen ID'yi tekrar giriniz")
                time.sleep(2)
                os.system("cls")
        accountDicts = {}
        i = 0
        for account in accounts:
            i += 1
            accountDicts[str(i)] = account
        actionControl = None
        while actionControl == None:
            while True:
                try:
                    print()
                    for key, value in accountDicts.items():
                        print("     {}. : {} --> {}".format(key, value, accounts[value]))
                    selectionIndex = input("Hesap seçimi: ")
                    selectionAccount = accountDicts[selectionIndex]
                    break
                except KeyError:
                    print("Yanlış hesap seçimi yapıldı. Lütfen tekrar deneyiniz.")
                    time.sleep(2)
                    os.system("cls")    
            addMoneys = []
            control = None
            while control == None:
                inputCustomerMoney = input("Paralarınızı sisteme giriniz(İşlemi bitirmek için '' girin): ")
                if inputCustomerMoney == "":
                    control = inputCustomerMoney
                elif inputCustomerMoney not in banknotes:
                    print("Lütfen paraları 5, 10, 20, 50, 100, 200 olacak şekilde giriniz...")
                else:
                    money = int(inputCustomerMoney)
                    addMoneys.append(money)
            moneyDict = {}
            for money in addMoneys:
                if money not in moneyDict.keys():
                    moneyDict[money] = addMoneys.count(money)
            total = 0
            for key, value in moneyDict.items():
                print("     {} TL ----> {} Adet".format(key, value))
                total += value * key
            print("     Toplam:  {} TL".format(total))
            while True:
                assent = input("Yatırdığınız paraları ve toplam tutarı onaylıyor musunuz?(E/H): ").upper()
                if assent in ["E", "H"]:
                    break
            if assent == "E":
                balance = int(bank_accounts[userBankID]["accounts"][selectionAccount]) + total
                bank_accounts[userBankID]["accounts"][selectionAccount] = balance
                print("Para yatırma işleminiz başarılı...")
                actionControl = "ç"
                time.sleep(2)
            elif assent == "H":
                print()
                print("İşleme baştan yapmak için ----> 1",
                      "İşlemden çıkmak için      ----> 2", sep="\n")
                while True:
                    action = input("İşlem seçimi: ")
                    if action in ["1", "2"]:
                        os.system("cls")
                        break
                if action == "1":
                    continue
                elif action == "2":
                    actionControl = "ç"

    def withdrawal():  # Para Çekme
        while True:
            try:
                userBankID = input("Banka ID giriniz: ")
                accounts = bank_accounts[userBankID]["accounts"]
                break
            except KeyError:
                print("Sistemde kayıtlı ID bulunmadı... Lütfen tekrar deneyiniz.")
                time.sleep(2)
                os.system("cls")
        accountDicts = {}
        i = 0
        for account in accounts:
            i += 1
            accountDicts[str(i)] = account
        actionControl = None
        while actionControl == None:
            while True:
                print()
                for key, value in accountDicts.items():
                    print("     {}. : {} --> {}".format(key, value, accounts[value]))
                try:
                    selectionIndex = input("Hesap seçimi: ")
                    selectionAccount = accountDicts[selectionIndex]
                    break
                except KeyError:
                    print("Hesap seçimi hatası yaptınız... Lütfen tekrar deneyiniz")
                    time.sleep(2)
                    os.system("cls")
            while True:
                try:
                    balance = int(input("Hesabınızdan çekmek istediğiniz tutar giriniz: "))
                    if balance >= 50 and balance % 5 == 0:
                        break
                    else:
                        print(
                        "Girdiğiniz tutar 50 TL ve üstü olmalıdır. 5'in katı olacak şekilde para çekme miktarı giriniz.")
                except ValueError:
                    print("Lütfen geçerli bir para giriniz")
            accountBalance = int(bank_accounts[userBankID]["accounts"][selectionAccount])
            if balance > accountBalance:
                print()
                print("Hesabınızdan çekmek istediğiniz tutar seçtiğiniz hesabınızdaki bakiyeye yetersiz...")
                print("İşleme tekrar denemek için ----> 1",
                      "Çıkmak için                ----> 2", sep="\n")
                while True:
                    action = input("İşlem seçimi: ")
                    if action in ["1", "2"]:
                        os.system("cls")
                        break
                if action == "1":
                    continue
                elif action == "2":
                    actionControl = "ç"
            else:
                while True:
                    assent = input("Hesabınızdan para çekme işlemini onaylıyor musunuz?(E/H): ").upper()
                    if assent in ["E", "H"]:
                        break
                if assent == "E":   
                    outBankNotes = {}
                    convertbanknotes = []
                    for banknote in banknotes:
                        banknote = int(banknote)
                        convertbanknotes.append(banknote)
                    convertbanknotes = tuple(convertbanknotes)
                    accountBalance -= balance
                    bank_accounts[userBankID]["accounts"][selectionAccount] = accountBalance
                    bigbanknote = None
                    while balance != 0:
                        for banknote in convertbanknotes:
                            if banknote <= balance:
                                bigbanknote = banknote
                        outBankNotes[bigbanknote] = balance // bigbanknote
                        balance = balance % bigbanknote
                    for key, value in outBankNotes.items():
                        print("     {} TL ---- {} Adet".format(key, value))
                    print("Para çekme işleminiz başarılı...")
                    actionControl = "ç"
                    time.sleep(2)
                elif assent == "H":
                    print()
                    print("İşleme baştan yapmak için ----> 1",
                          "İşlemden çıkmak için      ----> 2", sep="\n")
                    while True:
                        action = input("İşlem seçimi: ")
                        if action in ["1", "2"]:
                            os.system("cls")
                            break
                    if action == "1":
                        continue
                    elif action == "2":
                        actionControl = "ç"

    while True:
        print()
        print("Para yatırma işlemleri için ----> 1",
              "Para çekme işlemleri için   ----> 2",
              "Ana menüye dönmek için      ----> 3",sep="\n")
        action = input("İşlem seçimi: ")
        os.system("cls")
        if action == "1":
            invenstment()
        elif action == "2":
            withdrawal()
        elif action == "3":
            break
        fileWrite(bank_accounts)
        os.system("cls")

def accountdeleteaction():  # Silme
    """
    The "accountDeleteAction" function is responsible for deleting functions of bank customers
    or facilitating the deletion of accounts of registered customers in the system.
    """
    global bank_accounts
    fileRead(bank_accounts)
    while True:
        print()
        print("Müşterinin bankadaki üyeliğini silmek için   ----> 1",
              "Müşterinin mevcut olan hesapları silmek için ----> 2",
              "Ana menüye dönmek için                       ----> 3",sep="\n")
        action = input("İşlem seçimi: ")
        os.system("cls")
        if action == "1":
            actionControl = None
            while actionControl == None:
                while True:
                    try:
                        userBankID = input("Banka ID giriniz: ")
                        accounts = bank_accounts[userBankID]["accounts"]
                        print("{}".format(bank_accounts[userBankID]["name surname"]))
                        break
                    except KeyError:
                        print("Sistemde kayıtlı ID bulunamadı... Lütfen tekrar deneyiniz.")
                        time.sleep(2)
                        os.system("cls")
                control = None
                while control == None:
                    accounts = bank_accounts[userBankID]["accounts"]
                    count = 0
                    for key, value in accounts.items():
                        value = int(value)
                        if value > 0:
                            print("{} : {}".format(key, value))
                            count += 1
                    if count > 0:
                        print("Hesaplarınızda paralarınız mevcuttur.")
                        while True:
                            choose = input("Hesaplarınızdaki paralarnız ile işlem yapmak istiyor musunuz?(E/H): ").upper()
                            if choose in ["E", "H"]:
                                break
                        if choose == "E":
                            print()
                            print("Para transferi işlemleri için   ----> 1",
                                  "Para yatırma ve çekme işlemleri ----> 2",
                                  "Çıkmak için                     ----> 3",sep="\n")
                            action = input("İşlem seçimi: ")
                            os.system("cls")
                            if action == "1":
                                moneytransferaction()
                            elif action == "2":
                                moneyaction()
                            elif action == "3":
                                time.sleep(2)
                                actionControl = "ç"
                                control = "ç"
                        elif choose == "H":
                            actionControl = "ç" 
                    else:
                        del bank_accounts[userBankID]
                        print("Hesap silme işlemi tamamlandı. Bankamızda hiçbir ilişiğiniz yoktur.")
                        time.sleep(2)
                        actionControl = "ç"
                        break
        elif action == "2":
            actionControl = None
            while actionControl == None:
                while True:
                    try:
                        userBankID = input("Banka ID giriniz: ")
                        accounts = bank_accounts[userBankID]["accounts"]
                        break
                    except KeyError:
                        print("Sistemde kayıtlı olmayan ID girdiniz. Tekrar deneyiniz.")
                        time.sleep(2)
                        os.system("cls")
                if len(accounts) == 1:
                    print("Mevcut hesaplarınızda 1 tane hesabınız bulunduğundan hesap silme işlemi gerçekleştiremez.")
                    time.sleep(2)
                    break
                while True:
                    try:
                        print()
                        print("{}".format(bank_accounts[userBankID]["name surname"]))
                        accountsDict = {}
                        i = 0
                        for key, value in accounts.items():
                            i += 1
                            print("{}. ----> {} : {}".format(i, key, value))
                            accountsDict[str(i)] = key
                        selectionIndex = input("Hesap seçimi: ")
                        selectionAccount = accountsDict[selectionIndex]
                        accountBalance = int(bank_accounts[userBankID]["accounts"][selectionAccount])
                        break
                    except KeyError:
                        print("Yanlış bir hesap seçimi yapıldı. Lütfen tekrar deneyiniz.")
                        time.sleep(2)
                        os.system("cls")
                if accountBalance > 0:
                    print("Silmek istediğiniz hesabınızda bakiye olmaması gerekir...")
                    print()
                    print("Silmek istediğniz hesabınızı devam etmek için ----> 1",
                          "İşleme başka bir hesap ile devam etmek için   ----> 2",
                          "Çıkmak için                                   ----> 3", sep="\n")
                    while True:
                        choose = input("İşlem seçimi: ")
                        if choose in ["1", "2", "3"]:
                            os.system("cls")
                            break
                    if choose == "1":
                        while True:
                            valueMoney = int(bank_accounts[userBankID]["accounts"][selectionAccount])
                            if valueMoney != 0:
                                print("Hesabınıda para mevcut silinecek olan hesapta bakiye olmaması gerekir.")
                                print()
                                print("Para transferleri için                       ----> 1",
                                      "Para yatırma ve çekme işlemleri için         ----> 2",
                                      "Çıkmak için                                  ----> 3",sep="\n")
                                action = input("İşlem seçimi: ")
                                os.system("cls")
                                if action == "1":
                                    moneytransferaction()
                                elif action == "2":
                                    moneyaction()
                                elif action == "3":
                                    actionControl = "ç"
                                    break
                            else:
                                bank_accounts[userBankID]["accounts"].pop(selectionAccount)
                                print("Hesabınız silinmiştir...")
                                time.sleep(2.5)
                                actionControl = "ç"
                                break
                    elif choose == "2":
                        continue
                    elif choose == "3":
                        actionControl = "ç"
                else:
                    bank_accounts[userBankID]["accounts"].pop(selectionAccount)
                    os.system("cls")
                    print("Hesabınız silinmiştir...")
                    time.sleep(2.5)
                    actionControl = "ç"
        elif action == "3":
            break
        fileWrite(bank_accounts)
        os.system("cls")

def accountsearchaction():  # Arama
    """
    The "accountSearchAction" function is a search function for retrieving
    relevant information about registered customers in the system.
    """
    global bank_accounts
    fileRead(bank_accounts)
    control = False
    ID = None
    while True:
        print()
        print('"AD SOYAD/TC KİMLİK NO/TELEFON NUMARASI/E-MAİL ADRESİ" ile bilgiler aranır')
        keySearchWord = input("Arama parametresi: ")
        print("     Girilen bilgi aranıyor...")
        time.sleep(0.5)
        if keySearchWord.lower() == "ç":
            print("     Sistemden çıkış yapılıyor...")
            time.sleep(0.5)
            break
        for id in bank_accounts:
            for key, value in bank_accounts[id].items():
                if keySearchWord == value:
                    ID = id
                    control = True
                elif keySearchWord in bank_accounts.keys():
                    ID = keySearchWord
                    control = True
                elif keySearchWord == " ":
                    control = False
        if control == True:
            print("     ID: {}".format(ID))
            print("     AD SOYAD: {}".format(bank_accounts[ID]["name surname"]))
            print("     TC KİMLİK NO: {}".format(bank_accounts[ID]["tc id"]))
            print("     TELEFON NUMARASI: {}".format(bank_accounts[ID]["phone number"]))
            print("     E-MAİL ADRESİ: {}".format(bank_accounts[ID]["email address"]))
            print("     HESAPLAR:")
            accounts = bank_accounts[ID]["accounts"].items()
            for account in accounts:
                print("         {} : {}".format(account[0], account[1]))
            control = False
        elif control == False:
            print("     Girdiğiniz bilgiye müşteri bulanamadı veya girdiğiniz bilgi müşteriye mevcut olmayan bilgi...")
        time.sleep(8)
        os.system("cls")

def accountupdateaction():  # Güncelleme
    """
    The "accountUpdateAction" function is responsible for updating the account information of the customer.
    """
    global bank_accounts
    fileRead(bank_accounts)
    updateKey = None
    message = None
    while True:
        print()
        print("Güncelleme işlemi için ----> 1",
              "Ana menüye dönmek için ----> 2", sep="\n")
        action = input("İşlem seçimi: ")
        os.system("cls")
        if action == "1":
            print()
            print("'Ad ve Soyad' güncellemesi için       ---> 1",
                  "'TC Kimlik No' güncellemesi için      ---> 2",
                  "'Telefon Numarası' güncellemesi için  ---> 3",
                  "'E-mail adresi' güncellemesi için     ---> 4", sep="\n")
            choose = input("İşlem seçimi: ")
            os.system("cls")
            match choose:
                case "1":
                    updateKey = "name surname"
                    message = "Ad Soyad:"
                case "2":
                    updateKey = "tc id"
                    message = "TC Kimlik No:"
                case "3":
                    updateKey = "phone number"
                    message = "Telefon Numarası:"
                case "4":
                    updateKey = "email address"
                    message = "E-Mail Adresi:"
                case _:
                    continue
            while True:
                try:
                    userBankID = input("Banka ID giriniz: ")
                    controlItem = bank_accounts[userBankID][updateKey]
                except KeyError:
                    print("Sistemde kayıtlı ID bulanamadı... Lütfen ID'yi tekrar giriniz")
                    time.sleep(2)
                    os.system("cls")
                else:
                    print()
                    print("{}".format(bank_accounts[userBankID]["name surname"]))
                    item = input("{} ".format(message))
                    if updateKey == "name surname":
                        item = item.title()
                        if len(item.split(" ")) < 2:
                            print("Ad ve soyad bilginizi aralarında boşluk olacak şekilde giriniz.")
                            time.sleep(3)
                            os.system("cls")
                            continue
                    elif updateKey == "tc id":
                        if len(item) < 11 or len(item) > 11:
                            print("TC Kimlik numaranızı 11 haneli olcak şekilde giriniz.")
                            time.sleep(3)
                            os.system("cls")
                            continue
                        elif item in TCIDList:
                            print("Sistemde kayıtlı TC Kimlik Numarası girmeyiniz.")
                            time.sleep(3)
                            os.system("cls")
                            continue
                        else:
                            index = TCIDList.index(bank_accounts[userBankID][updateKey])
                            TCIDList[index] = item
                    elif updateKey == "phone number":
                        if len(item[1:]) < 10 or len(item) > 11:
                            print("Numaranızı başına '0' olacak şekilde giriniz.")
                            time.sleep(3)
                            os.system("cls")
                            continue
                    bank_accounts[userBankID][updateKey] = item
                    print("Güncelleme işlemi başarı ile yapıldı...")
                    time.sleep(2.5)
                    break
        elif action == "2":
            break
        else:
            continue
        fileWrite(bank_accounts)
        os.system("cls")

def accountaddaction():  # Ekleme
    """
    The 'accountAddAction' function is responsible for adding a new customer and adding to existing accounts.
    """
    global bank_accounts
    if isDatabase(fileName) == True:
        bank_accounts = fileRead(bank_accounts)
    else:
        file = open(fileName,"w")
        file.close()

    def accountinformationcreate():  # IBAN Oluşturma
        """
        The 'accountInformationCreate' function is responsible for generating accounts for the customer.
        :return the IBAN value:
        """
        iban_code = "TR"
        iban_no = []
        while len(iban_no) != 3:
            ibandigit = ""
            if len(iban_no) == 0:
                for index in range(2):
                    ibandigit += str(random.randint(0, 9))
            else:
                for index in range(4):
                    ibandigit += str(random.randint(0, 9))
            iban_no.append(ibandigit)
        iban_no = " ".join(iban_no)
        iban_no = iban_code + iban_no
        return {iban_no: "0"}

    while True:
        print()
        print("Yeni bir bankacılık sistemine kayıt olmak için    ----> 1",
              "Bankacılık hesabınıza yeni bir hesap eklemek için ----> 2",
              "Ana menüye dönmek için                            ----> 3", sep="\n")
        action = input("İşlem seçimi: ")
        os.system("cls")
        if action == "1":
            temp = {}
            while True:
                bankID = str(random.randint(10000, 99999))
                if bankID not in IDList:
                    break
            while True:
                name_surname = input("Ad Soyad: ")
                controlNameSurname = name_surname.split(" ")
                if len(controlNameSurname) < 2:
                    print("İsim ve soyad bilginizi arasında boşluk olacak şekilde tekrar giriniz.")
                else:
                    break
            while True:
                tc_id = input("TC Kimlik No: ")
                if tc_id in TCIDList:
                    print("Sistemde kayıtlı TC Kimlik Numarası girmeyiniz!!!")
                elif len(tc_id) < 11 or len(tc_id) > 11:
                    print("TC Kimlik numaranızı 11 haneli olacak şekilde tekrar giriniz.")
                else:
                    break
            while True:
                phone_number = input("Telefon Numarası: ")
                if len(phone_number[1:]) < 10:
                    print("Telefon Numaranızı başında '0' olacak şekilde tekrar giriniz")
                else:
                    break
            email_address = input("Email Adresi: ")
            while True:
                if accountinformationcreate() in IBANList:
                    continue
                else:
                    break
            temp["name surname"] = name_surname
            temp["tc id"] = tc_id
            temp["phone number"] = phone_number
            temp["email address"] = email_address
            temp["accounts"] = accountinformationcreate()
            bank_accounts[bankID] = temp
            print("Bilgileriniz kontrol ediliyor...\n")

            print("Bankamıza hoş geldiniz.")
            print("ID: {}".format(bankID))
            print("AD SOYAD: {}".format(temp["name surname"]))
            time.sleep(5)
        elif action == "2":
            while True:
                try:
                    userBankID = input("Banka ID giriniz: ")
                    account = bank_accounts[userBankID]["accounts"]
                except KeyError:
                    print("Sistemde kayıtlı ID bulanamadı... Lütfen tekrar deneyiniz")
                    time.sleep(2)
                    os.system("cls")
                else:
                    print("{}".format(bank_accounts[userBankID]["name surname"]))
                    account.update(accountinformationcreate())
                    bank_accounts[userBankID]["accounts"] = account
                    print("Yeni hesap açma işlemi başarılı bir şekilde tamamlandı.")
                    time.sleep(2.5)
                    break
        elif action == "3":
            break
        fileWrite(bank_accounts)
        os.system("cls")

def master(): # Arayüz
    """
    The 'master' function is the main control center of the automation.
    """
    while True:
        print()
        print("BANKACILIK UYGULAMASI")
        print("Bankacılık sistemine yeni kayıt olmak veya yeni bir hesap eklemek için ----> 1",
              "Bankacılık sisteminde bilgileri güncellemek için                       ----> 2",
              "Bankacılık sistemnde ilgili hesapları aramak için                      ----> 3",
              "Bankacılık sisteminden çıkmak veya hesap silme işlemleri için          ----> 4",
              "Bankacılık sisteminde para çekme ve yatırma işlemleri için             ----> 5",
              "Bankacılık sisteminde para transfer işlemleri için                     ----> 6",
              "Sistemden çıkmak için                                                  ----> 0",
              sep="\n")
        action = input("Lütfen işlem seçiniz: ")
        os.system("cls")
        match action:
            case "1":
                accountaddaction()
            case "2":
                accountupdateaction()
            case "3":
                accountsearchaction()
            case "4":
                accountdeleteaction()
            case "5":
                moneyaction()
            case "6":
                moneytransferaction()
            case "0":
                quit()
        os.system("cls")

master() 