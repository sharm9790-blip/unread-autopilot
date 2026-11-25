CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
बेटे ने काल्पनिक दोस्त का बिस्तर बनाया। उसमें कोई सोया था
மகன் கற்பனை நண்பனுக்கு படுக்கை போட்டான். அதில் யாரோ தூங்கியிருந்தார்கள்
కొడుకు ఊహా స్నేహితుడికి మంచం వేశాడు. అందులో ఎవరో పడుకున్నారు
ছেলে কাল্পনিক বন্ধুর বিছানা বানাল। সেখানে কেউ ঘুমিয়েছিল
मुलाने काल्पनिक मित्रासाठी अंथरूण केले. त्यात कोणी झोपले होते
بیٹے نے خیالی دوست کا بستر بنایا۔ اس میں کوئی سویا تھا
Gumawa ng Higaan ang Anak Ko para sa Imaginary Friend. May Natulog Dito
Anakku Membuat Kasur untuk Teman Khayalannya. Ada yang Tidur di Sana
Anak Saya Buat Katil untuk Kawan Khayalan. Ada Orang Tidur di Situ
သားက စိတ်ကူးထဲက သူငယ်ချင်းအတွက် အိပ်ရာပြင်တယ်။ တစ်ယောက်ယောက် အိပ်သွားတယ်
ลูกชายทำที่นอนให้เพื่อนในจินตนาการ มีคนนอนอยู่จริงๆ
Con Trai Làm Giường Cho Bạn Tưởng Tượng. Có Người Đã Ngủ Ở Đó
Mi Hijo Hizo una Cama para Su Amigo Imaginario. Alguien Durmió Ahí
Meu Filho Fez uma Cama pro Amigo Imaginário. Alguém Dormiu Nela
Mon Fils a Fait un Lit pour Son Ami Imaginaire. Quelqu'un y a Dormi
Mein Sohn Baute ein Bett für Seinen Fantasiefreund. Es War Benutzt
Mio Figlio Ha Fatto un Letto per l'Amico Immaginario. Ci Ha Dormito Qualcuno
Mijn Zoon Maakte een Bed voor Zijn Denkbeeldige Vriend. Er Was in Geslapen
Min Son Bäddade för Sin Låtsasvän. Någon Hade Sovit Där
Syn Pościelił Łóżko Wyimaginowanemu Przyjacielowi. Ktoś w Nim Spał
Сын Постелил Кровать Воображаемому Другу. В Ней Кто-то Спал
Oğlum Hayali Arkadaşına Yatak Yaptı. Birisi Orada Uyumuş
ابني جهّز سريرًا لصديقه الخيالي. وكان أحدهم قد نام فيه
息子が空想の友達にベッドを作った。誰かが寝た跡があった
아들이 상상 속 친구의 침대를 만들었다. 누군가 자고 간 흔적이 있다
儿子给想象中的朋友铺了张床。有人睡过的痕迹
"""
E1_H = """
बेटे ने काल्पनिक दोस्त के लिए बिस्तर बनाया। आज रात कंबल गर्म था।
மகன் கற்பனை நண்பனுக்கு படுக்கை போட்டான். இன்றிரவு போர்வை சூடாக இருந்தது.
కొడుకు ఊహా స్నేహితుడికి మంచం వేశాడు. ఈ రాత్రి దుప్పటి వెచ్చగా ఉంది.
ছেলে কাল্পনিক বন্ধুর জন্য বিছানা বানাল। আজ রাতে কম্বল গরম ছিল।
मुलाने काल्पनिक मित्रासाठी अंथरूण केले. आज रात्री पांघरूण उबदार होते.
بیٹے نے خیالی دوست کے لیے بستر بنایا۔ آج رات کمبل گرم تھا۔
Gumawa ng higaan ang anak ko para sa imaginary friend niya. Mainit ang kumot ngayong gabi.
Anakku membuat kasur untuk teman khayalannya. Malam ini selimutnya hangat.
Anak saya buat katil untuk kawan khayalannya. Malam ini selimutnya hangat.
သားက စိတ်ကူးထဲက သူငယ်ချင်းအတွက် အိပ်ရာပြင်တယ်။ ဒီည စောင်က နွေးနေတယ်။
ลูกชายทำที่นอนให้เพื่อนในจินตนาการ คืนนี้ผ้าห่มยังอุ่นอยู่
Con trai làm giường cho bạn tưởng tượng. Tối nay chăn còn ấm.
Mi hijo hizo una cama para su amigo imaginario. Esta noche la manta estaba tibia.
Meu filho fez uma cama pro amigo imaginário. Hoje à noite o cobertor estava quente.
Mon fils a fait un lit pour son ami imaginaire. Ce soir, la couverture était chaude.
Mein Sohn baute ein Bett für seinen Fantasiefreund. Heute Nacht war die Decke warm.
Mio figlio ha fatto un letto per l'amico immaginario. Stanotte la coperta era calda.
Mijn zoon maakte een bed voor zijn denkbeeldige vriend. Vannacht was de deken warm.
Min son bäddade för sin låtsasvän. Inatt var filten varm.
Mój syn pościelił łóżko wyimaginowanemu przyjacielowi. Dziś w nocy koc był ciepły.
Сын постелил кровать воображаемому другу. Сегодня ночью одеяло было тёплым.
Oğlum hayali arkadaşına yatak yaptı. Bu gece battaniye sıcaktı.
ابني جهّز سريرًا لصديقه الخيالي. الليلة كانت البطانية دافئة.
息子が空想の友達にベッドを作った。今夜、毛布が温かかった。
아들이 상상 속 친구의 침대를 만들었다. 오늘 밤 이불이 따뜻했다.
儿子给想象中的朋友铺了张床。今晚被子是温的。
"""
E2_T = """
चौथी कुर्सी Pt 1: बेटा खाने पर चार गिनता है। हम तीन हैं
நான்காவது நாற்காலி Pt 1: மகன் இரவு உணவில் நால்வரை எண்ணுகிறான். நாங்கள் மூவர்
నాలుగో కుర్చీ Pt 1: కొడుకు భోజనంలో నలుగురిని లెక్కిస్తాడు. మేము ముగ్గురం
চতুর্থ চেয়ার Pt 1: ছেলে খাবার টেবিলে চারজন গোনে। আমরা তিনজন
चौथी खुर्ची Pt 1: मुलगा जेवताना चार मोजतो. आम्ही तिघे आहोत
چوتھی کرسی Pt 1: بیٹا کھانے پر چار گنتا ہے۔ ہم تین ہیں
Ikaapat na Upuan Pt 1: Apat ang Bilang ng Anak Ko sa Hapunan. Tatlo Kami
Kursi Keempat Pt 1: Anakku Menghitung Empat Orang Saat Makan. Kami Bertiga
Kerusi Keempat Pt 1: Anak Saya Kira Empat Orang Waktu Makan. Kami Bertiga
စတုတ္ထကုလားထိုင် Pt 1: သားက ညစာမှာ လေးယောက်ရေတယ်။ ကျွန်တော်တို့ သုံးယောက်ပဲ
เก้าอี้ตัวที่สี่ Pt 1: ลูกชายนับได้สี่คนตอนกินข้าว แต่เรามีสามคน
Chiếc Ghế Thứ Tư Pt 1: Con Trai Đếm Bốn Người Ở Bữa Tối. Nhà Tôi Có Ba
La Cuarta Silla Pt 1: Mi Hijo Cuenta Cuatro en la Cena. Somos Tres
A Quarta Cadeira Pt 1: Meu Filho Conta Quatro no Jantar. Somos Três
La Quatrième Chaise Pt 1: Mon Fils Compte Quatre au Dîner. Nous Sommes Trois
Der Vierte Stuhl Pt 1: Mein Sohn Zählt Vier beim Essen. Wir Sind Drei
La Quarta Sedia Pt 1: Mio Figlio Conta Quattro a Cena. Siamo in Tre
De Vierde Stoel Pt 1: Mijn Zoon Telt Vier aan Tafel. Wij Zijn Met Z'n Drieën
Fjärde Stolen Pt 1: Min Son Räknar Fyra vid Middagen. Vi Är Tre
Czwarte Krzesło Pt 1: Syn Liczy Czworo przy Kolacji. Jest Nas Troje
Четвёртый Стул Pt 1: Сын Считает Четверых за Ужином. Нас Трое
Dördüncü Sandalye Pt 1: Oğlum Yemekte Dört Kişi Sayıyor. Biz Üçüz
الكرسي الرابع Pt 1: ابني يعدّ أربعة على العشاء. نحن ثلاثة
4つ目の椅子 Pt 1: 息子は夕食で4人と数える。うちは3人
네 번째 의자 Pt 1: 아들이 저녁에 네 명이라고 센다. 우리는 셋이다
第四把椅子 Pt 1: 儿子说晚饭桌上有四个人。我们只有三个
"""
E2_H = """
बेटा खाने की मेज़ पर चार गिनता है। हम तीन हैं।
மகன் இரவு உணவில் நால்வரை எண்ணுகிறான். நாங்கள் மூவர்தான்.
కొడుకు భోజనంలో నలుగురిని లెక్కిస్తాడు. మేము ముగ్గురమే.
ছেলে খাবার টেবিলে চারজন গোনে। আমরা তিনজন।
मुलगा जेवताना चार मोजतो. आम्ही तिघेच आहोत.
بیٹا کھانے کی میز پر چار گنتا ہے۔ ہم تین ہیں۔
Apat ang bilang ng anak ko sa hapunan. Tatlo lang kami.
Anakku menghitung empat orang di meja makan. Kami hanya bertiga.
Anak saya kira empat orang di meja makan. Kami cuma bertiga.
သားက ညစာစားပွဲမှာ လေးယောက်ရေတယ်။ ကျွန်တော်တို့ သုံးယောက်ပဲ။
ลูกชายนับได้สี่คนที่โต๊ะอาหาร แต่เรามีแค่สามคน
Con trai đếm bốn người ở bàn ăn. Nhà tôi chỉ có ba.
Mi hijo cuenta cuatro en la mesa. Somos tres.
Meu filho conta quatro na mesa do jantar. Somos três.
Mon fils compte quatre à table. Nous sommes trois.
Mein Sohn zählt vier am Esstisch. Wir sind drei.
Mio figlio conta quattro a tavola. Siamo in tre.
Mijn zoon telt vier aan tafel. Wij zijn met z'n drieën.
Min son räknar fyra vid bordet. Vi är tre.
Mój syn liczy czworo przy stole. Jest nas troje.
Сын считает за столом четверых. Нас трое.
Oğlum sofrada dört kişi sayıyor. Biz üç kişiyiz.
ابني يعدّ أربعة على مائدة العشاء. نحن ثلاثة فقط.
息子は食卓で4人と数える。うちは3人だ。
아들이 식탁에서 네 명이라고 센다. 우리는 셋뿐이다.
儿子说饭桌上有四个人。可我们只有三个。
"""
E3_T = """
चौथी कुर्सी Pt 2: उसकी थाली लगी थी। उसे मेरी जगह चाहिए
நான்காவது நாற்காலி Pt 2: அவளுக்கு தட்டு வைக்கப்பட்டது. அவளுக்கு என் இடம் வேண்டும்
నాలుగో కుర్చీ Pt 2: ఆమె కోసం కంచం పెట్టారు. ఆమెకు నా స్థానం కావాలి
চতুর্থ চেয়ার Pt 2: তার থালা সাজানো ছিল। সে আমার জায়গা চায়
चौथी खुर्ची Pt 2: तिचे ताट मांडलेले होते. तिला माझी जागा हवी आहे
چوتھی کرسی Pt 2: اس کی تھالی لگی تھی۔ اسے میری جگہ چاہیے
Ikaapat na Upuan Pt 2: Nakahain ang Plato Niya. Gusto Niya ang Upuan Ko
Kursi Keempat Pt 2: Piringnya Sudah Disiapkan. Dia Mau Tempatku
Kerusi Keempat Pt 2: Pinggannya Sudah Dihidang. Dia Mahu Tempat Saya
စတုတ္ထကုလားထိုင် Pt 2: သူ့ပန်းကန်ချထားတယ်။ သူက ကျွန်မနေရာကို လိုချင်တယ်
เก้าอี้ตัวที่สี่ Pt 2: จานของเธอวางไว้แล้ว เธอต้องการที่นั่งของฉัน
Chiếc Ghế Thứ Tư Pt 2: Đĩa Của Cô Ấy Đã Được Bày Ra. Cô Ấy Muốn Chỗ Của Tôi
La Cuarta Silla Pt 2: Su Plato Estaba Servido. Quiere Mi Lugar
A Quarta Cadeira Pt 2: O Prato Dela Estava Posto. Ela Quer o Meu Lugar
La Quatrième Chaise Pt 2: Son Assiette Était Mise. Elle Veut Ma Place
Der Vierte Stuhl Pt 2: Ihr Teller War Gedeckt. Sie Will Meinen Platz
La Quarta Sedia Pt 2: Il Suo Piatto Era Pronto. Vuole il Mio Posto
De Vierde Stoel Pt 2: Haar Bord Stond Klaar. Ze Wil Mijn Plek
Fjärde Stolen Pt 2: Hennes Tallrik Var Dukad. Hon Vill Ha Min Plats
Czwarte Krzesło Pt 2: Jej Talerz Był Nakryty. Chce Mojego Miejsca
Четвёртый Стул Pt 2: Её Тарелка Была Накрыта. Она Хочет Моё Место
Dördüncü Sandalye Pt 2: Tabağı Konmuştu. Benim Yerimi İstiyor
الكرسي الرابع Pt 2: كان طبقها موضوعًا. تريد مكاني
4つ目の椅子 Pt 2: 彼女の皿が並べられていた。私の席を欲しがっている
네 번째 의자 Pt 2: 그녀의 접시가 놓여 있었다. 그녀는 내 자리를 원한다
第四把椅子 Pt 2: 她的盘子摆好了。她想要我的位子
"""
E3_H = """
उसकी थाली लगी थी। वह मेरी जगह पर बैठना चाहती है।
அவளுக்கான தட்டு வைக்கப்பட்டிருந்தது. அவள் என் இடத்தில் உட்கார விரும்புகிறாள்.
ఆమె కంచం పెట్టి ఉంది. ఆమె నా స్థానంలో కూర్చోవాలనుకుంటోంది.
তার থালা সাজানো ছিল। সে আমার জায়গায় বসতে চায়।
तिचे ताट मांडलेले होते. तिला माझ्या जागी बसायचे आहे.
اس کی تھالی لگی تھی۔ وہ میری جگہ بیٹھنا چاہتی ہے۔
Nakahain na ang plato niya. Gusto niyang umupo sa upuan ko.
Piringnya sudah disiapkan. Dia ingin duduk di tempatku.
Pinggannya sudah dihidang. Dia mahu duduk di tempat saya.
သူ့ပန်းကန်ချထားပြီးသား။ သူက ကျွန်မနေရာမှာ ထိုင်ချင်တယ်။
จานของเธอวางไว้แล้ว เธออยากนั่งที่ของฉัน
Đĩa của cô ấy đã được bày sẵn. Cô ấy muốn ngồi chỗ của tôi.
Su plato ya estaba servido. Quiere sentarse en mi lugar.
O prato dela já estava posto. Ela quer sentar no meu lugar.
Son assiette était déjà mise. Elle veut s'asseoir à ma place.
Ihr Teller war schon gedeckt. Sie will auf meinem Platz sitzen.
Il suo piatto era già pronto. Vuole sedersi al mio posto.
Haar bord stond al klaar. Ze wil op mijn plek zitten.
Hennes tallrik var redan dukad. Hon vill sitta på min plats.
Jej talerz był już nakryty. Chce usiąść na moim miejscu.
Её тарелка уже стояла. Она хочет сесть на моё место.
Tabağı çoktan konmuştu. Benim yerime oturmak istiyor.
كان طبقها موضوعًا بالفعل. تريد الجلوس في مكاني.
彼女の皿はもう並べられていた。私の席に座りたがっている。
그녀의 접시가 이미 놓여 있었다. 그녀는 내 자리에 앉고 싶어 한다.
她的盘子已经摆好了。她想坐我的位子。
"""
