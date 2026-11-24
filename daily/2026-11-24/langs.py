CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
बेटी ने पापा का बिना चेहरे का चित्र बनाया। पापा विदेश में हैं
மகள் முகம் இல்லாத அப்பாவை வரைந்தாள். அப்பா வெளிநாட்டில்
కూతురు ముఖం లేని నాన్నను గీసింది. నాన్న విదేశంలో ఉన్నారు
মেয়ে মুখহীন বাবার ছবি আঁকল। বাবা বিদেশে
मुलीने चेहरा नसलेल्या बाबांचे चित्र काढले. बाबा परदेशात आहेत
بیٹی نے بغیر چہرے کے ابو کی تصویر بنائی۔ ابو بیرون ملک ہیں
Gumuhit si Bunso kay Papa na Walang Mukha. Nasa Abroad si Papa
Putriku Menggambar Ayah Tanpa Wajah. Ayah di Luar Negeri
Anak Saya Lukis Ayah Tanpa Muka. Ayah di Luar Negara
သမီးက မျက်နှာမပါတဲ့ ဖေဖေကို ဆွဲတယ်။ ဖေဖေက နိုင်ငံခြားမှာ
ลูกสาววาดพ่อไม่มีหน้า พ่ออยู่ต่างประเทศ
Con Gái Vẽ Bố Không Có Mặt. Bố Đang Ở Nước Ngoài
Mi Hija Dibujó a Papá Sin Cara. Papá Está en el Extranjero
Minha Filha Desenhou o Pai Sem Rosto. Ele Está no Exterior
Ma Fille a Dessiné Papa Sans Visage. Papa Est à l'Étranger
Meine Tochter Malte Papa ohne Gesicht. Papa Ist im Ausland
Mia Figlia Ha Disegnato Papà Senza Faccia. È all'Estero
Mijn Dochter Tekende Papa Zonder Gezicht. Papa Is in het Buitenland
Min Dotter Ritade Pappa Utan Ansikte. Pappa Är Utomlands
Córka Narysowała Tatę Bez Twarzy. Tata Jest za Granicą
Дочь Нарисовала Папу Без Лица. Папа За Границей
Kızım Babamı Yüzsüz Çizdi. Babam Yurt Dışında
رسمت ابنتي أبي بلا وجه. أبي مسافر خارج البلاد
娘がパパを顔なしで描いた。パパは海外にいる
딸이 얼굴 없는 아빠를 그렸다. 아빠는 해외에 있다
女儿画了没有脸的爸爸。爸爸在国外
"""
E1_H = """
बेटी ने पापा का चित्र बिना चेहरे के बनाया। आज रात दरवाज़े पर उनकी चाबियाँ खनकीं।
மகள் முகமில்லாமல் அப்பாவை வரைந்தாள். இன்றிரவு கதவருகே அவர் சாவி ஒலித்தது.
కూతురు ముఖం లేకుండా నాన్నను గీసింది. ఈ రాత్రి తలుపు దగ్గర ఆయన తాళాలు మోగాయి.
মেয়ে মুখ ছাড়া বাবাকে এঁকেছে। আজ রাতে দরজায় তাঁর চাবি ঝনঝন করল।
मुलीने बाबांचे चित्र चेहऱ्याशिवाय काढले. आज रात्री दारात त्यांच्या चाव्या वाजल्या.
بیٹی نے ابو کی تصویر بغیر چہرے کے بنائی۔ آج رات دروازے پر ان کی چابیاں کھنکیں۔
Iginuhit ng anak ko si Papa nang walang mukha. Ngayong gabi, tumunog ang mga susi niya sa pinto.
Putriku menggambar Ayah tanpa wajah. Malam ini kunci Ayah berdenting di pintu.
Anak saya lukis Ayah tanpa muka. Malam ini kunci Ayah berbunyi di pintu.
သမီးက ဖေဖေ့ကို မျက်နှာမပါဘဲ ဆွဲတယ်။ ဒီညမှာ တံခါးမှာ သူ့သော့သံ ကြားရတယ်။
ลูกสาววาดพ่อไม่มีหน้า คืนนี้เสียงกุญแจของพ่อดังที่ประตู
Con gái vẽ bố không có mặt. Tối nay chùm chìa khóa của bố kêu leng keng ngoài cửa.
Mi hija dibujó a papá sin cara. Esta noche sus llaves sonaron en la puerta.
Minha filha desenhou o pai sem rosto. Esta noite as chaves dele tilintaram na porta.
Ma fille a dessiné papa sans visage. Ce soir, ses clés ont tinté à la porte.
Meine Tochter malte Papa ohne Gesicht. Heute Nacht klimperten seine Schlüssel an der Tür.
Mia figlia ha disegnato papà senza faccia. Stanotte le sue chiavi hanno tintinnato alla porta.
Mijn dochter tekende papa zonder gezicht. Vannacht rinkelden zijn sleutels aan de deur.
Min dotter ritade pappa utan ansikte. I natt skramlade hans nycklar vid dörren.
Córka narysowała tatę bez twarzy. Dziś w nocy jego klucze zabrzęczały przy drzwiach.
Дочь нарисовала папу без лица. Этой ночью у двери звякнули его ключи.
Kızım babamı yüzsüz çizdi. Bu gece kapıda anahtarlarının sesi geldi.
رسمت ابنتي أبي بلا وجه. الليلة رنّت مفاتيحه عند الباب.
娘がパパを顔なしで描いた。今夜、玄関で彼の鍵が鳴った。
딸이 얼굴 없는 아빠를 그렸다. 오늘 밤 현관에서 아빠의 열쇠 소리가 났다.
女儿画了没有脸的爸爸。今晚门口响起了他的钥匙声。
"""
E2_T = """
स्लीप टॉक Pt 1: पति नींद में हमारी बच्ची की आवाज़ में बोलते हैं
ஸ்லீப் டாக் Pt 1: கணவர் தூக்கத்தில் குழந்தையின் குரலில் பேசுகிறார்
స్లీప్ టాక్ Pt 1: భర్త నిద్రలో మా పాప గొంతుతో మాట్లాడుతున్నాడు
স্লিপ টক Pt 1: স্বামী ঘুমের মধ্যে আমাদের বাচ্চার গলায় কথা বলে
स्लीप टॉक Pt 1: नवरा झोपेत आमच्या बाळाच्या आवाजात बोलतो
سلیپ ٹاک Pt 1: شوہر نیند میں ہماری بچی کی آواز میں بولتے ہیں
Sleep Talk Pt 1: Nagsasalita ang Asawa Ko sa Boses ng Baby Namin
Sleep Talk Pt 1: Suamiku Bicara dalam Suara Bayi Kami
Sleep Talk Pt 1: Suami Saya Bercakap dalam Suara Bayi Kami
အိပ်မက်စကား Pt 1: ယောက်ျားက အိပ်ရင်း ကျွန်မတို့ကလေးအသံနဲ့ ပြောတယ်
Sleep Talk Pt 1: สามีละเมอด้วยเสียงลูกน้อยของเรา
Sleep Talk Pt 1: Chồng Tôi Nói Mớ Bằng Giọng Con Gái Chúng Tôi
Sleep Talk Pt 1: Mi Marido Habla Dormido con la Voz de Nuestro Bebé
Sleep Talk Pt 1: Meu Marido Fala Dormindo com a Voz do Nosso Bebê
Sleep Talk Pt 1: Mon Mari Parle dans son Sommeil avec la Voix de Notre Bébé
Sleep Talk Pt 1: Mein Mann Spricht im Schlaf mit der Stimme Unseres Babys
Sleep Talk Pt 1: Mio Marito Parla nel Sonno con la Voce della Nostra Bimba
Sleep Talk Pt 1: Mijn Man Praat in Zijn Slaap met de Stem van Onze Baby
Sleep Talk Pt 1: Min Man Pratar i Sömnen med Vår Bebis Röst
Sleep Talk Pt 1: Mój Mąż Mówi przez Sen Głosem Naszego Dziecka
Sleep Talk Pt 1: Муж Говорит Во Сне Голосом Нашего Малыша
Sleep Talk Pt 1: Kocam Uykusunda Bebeğimizin Sesiyle Konuşuyor
Sleep Talk Pt 1: زوجي يتكلم أثناء النوم بصوت طفلتنا
スリープトーク Pt 1: 夫が寝言で赤ちゃんの声で話す
슬립토크 Pt 1: 남편이 잠꼬대를 아기 목소리로 한다
梦话 Pt 1: 丈夫说梦话时用的是我们宝宝的声音
"""
E2_H = """
पति नींद में हमारी बच्ची की आवाज़ में बोले। पालना खाली था।
கணவர் தூக்கத்தில் குழந்தையின் குரலில் பேசினார். தொட்டில் காலியாக இருந்தது.
భర్త నిద్రలో మా పాప గొంతుతో మాట్లాడాడు. ఉయ్యాల ఖాళీగా ఉంది.
স্বামী ঘুমের মধ্যে বাচ্চার গলায় কথা বলল। দোলনা খালি ছিল।
नवरा झोपेत बाळाच्या आवाजात बोलला. पाळणा रिकामा होता.
شوہر نیند میں ہماری بچی کی آواز میں بولے۔ جھولا خالی تھا۔
Nagsalita ang asawa ko sa tulog gamit ang boses ng baby namin. Walang laman ang crib.
Suamiku bicara saat tidur dengan suara bayi kami. Boksnya kosong.
Suami saya bercakap dalam tidur dengan suara bayi kami. Katilnya kosong.
ယောက်ျားက အိပ်ရင်း ကလေးအသံနဲ့ ပြောတယ်။ ကလေးခုတင် ဗလာပဲ။
สามีละเมอด้วยเสียงลูกน้อยของเรา เปลว่างเปล่า
Chồng nói mớ bằng giọng con gái chúng tôi. Cũi trống không.
Mi marido habló dormido con la voz de nuestro bebé. La cuna estaba vacía.
Meu marido falou dormindo com a voz do nosso bebê. O berço estava vazio.
Mon mari a parlé en dormant avec la voix de notre bébé. Le berceau était vide.
Mein Mann sprach im Schlaf mit der Stimme unseres Babys. Das Bettchen war leer.
Mio marito ha parlato nel sonno con la voce della nostra bimba. La culla era vuota.
Mijn man praatte in zijn slaap met de stem van onze baby. De wieg was leeg.
Min man pratade i sömnen med vår bebis röst. Spjälsängen var tom.
Mąż mówił przez sen głosem naszego dziecka. Łóżeczko było puste.
Муж сказал во сне голосом нашего малыша. Кроватка была пуста.
Kocam uykusunda bebeğimizin sesiyle konuştu. Beşik boştu.
تكلم زوجي أثناء نومه بصوت طفلتنا. وكان السرير فارغًا.
夫が寝言で赤ちゃんの声で話した。ベビーベッドは空だった。
남편이 잠꼬대를 아기 목소리로 했다. 아기 침대는 비어 있었다.
丈夫用宝宝的声音说梦话。婴儿床是空的。
"""
E3_T = """
स्लीप टॉक Pt 2: मेरी बच्ची बिस्तर के नीचे एक हाथ पकड़े थी
ஸ்லீப் டாக் Pt 2: என் குழந்தை கட்டிலுக்கு அடியில் ஒரு கையைப் பிடித்திருந்தாள்
స్లీప్ టాక్ Pt 2: మంచం కింద నా పాప ఒక చేతిని పట్టుకుంది
স্লিপ টক Pt 2: খাটের নিচে আমার বাচ্চা একটা হাত ধরে ছিল
स्लीप टॉक Pt 2: माझे बाळ पलंगाखाली एक हात धरून होते
سلیپ ٹاک Pt 2: میری بچی بستر کے نیچے ایک ہاتھ تھامے تھی
Sleep Talk Pt 2: May Hawak na Kamay ang Baby Ko sa Ilalim ng Kama
Sleep Talk Pt 2: Bayiku Memegang Tangan di Bawah Ranjang
Sleep Talk Pt 2: Bayi Saya Pegang Tangan di Bawah Katil
အိပ်မက်စကား Pt 2: ကျွန်မကလေး ခုတင်အောက်မှာ လက်တစ်ဖက်ကို ကိုင်ထားတယ်
Sleep Talk Pt 2: ลูกน้อยจับมือหนึ่งอยู่ใต้เตียง
Sleep Talk Pt 2: Con Tôi Nắm Một Bàn Tay Dưới Gầm Giường
Sleep Talk Pt 2: Mi Bebé Sostenía una Mano Debajo de la Cama
Sleep Talk Pt 2: Meu Bebê Segurava uma Mão Embaixo da Cama
Sleep Talk Pt 2: Mon Bébé Tenait une Main sous le Lit
Sleep Talk Pt 2: Mein Baby Hielt Unter dem Bett eine Hand
Sleep Talk Pt 2: La Mia Bimba Stringeva una Mano Sotto il Letto
Sleep Talk Pt 2: Mijn Baby Hield een Hand Vast onder het Bed
Sleep Talk Pt 2: Min Bebis Höll en Hand Under Sängen
Sleep Talk Pt 2: Moje Dziecko Trzymało Rękę pod Łóżkiem
Sleep Talk Pt 2: Мой Малыш Держал Чью-то Руку Под Кроватью
Sleep Talk Pt 2: Bebeğim Yatağın Altında Bir El Tutuyordu
Sleep Talk Pt 2: طفلتي كانت تمسك يدًا تحت السرير
スリープトーク Pt 2: 赤ちゃんはベッドの下で誰かの手を握っていた
슬립토크 Pt 2: 아기가 침대 밑에서 누군가의 손을 잡고 있었다
梦话 Pt 2: 宝宝在床底下握着一只手
"""
E3_H = """
मैंने पूछा बच्ची कहाँ है। सोते पति बोले: बिस्तर के नीचे।
நான் குழந்தை எங்கே என்றேன். தூங்கும் கணவர் சொன்னார்: கட்டிலுக்கு அடியில்.
పాప ఎక్కడ అని అడిగాను. నిద్రలో భర్త అన్నాడు: మంచం కింద.
আমি জিজ্ঞেস করলাম বাচ্চা কোথায়। ঘুমন্ত স্বামী বলল: খাটের নিচে।
मी विचारले बाळ कुठे आहे. झोपलेला नवरा म्हणाला: पलंगाखाली.
میں نے پوچھا بچی کہاں ہے۔ سوتے شوہر نے کہا: بستر کے نیچے۔
Tinanong ko kung nasaan ang baby ko. Sabi ng natutulog kong asawa: sa ilalim ng kama.
Aku tanya di mana bayiku. Suamiku yang tidur menjawab: di bawah ranjang.
Saya tanya di mana bayi saya. Suami yang tidur jawab: di bawah katil.
ကလေးဘယ်မှာလဲလို့ မေးတော့ အိပ်နေတဲ့ယောက်ျားက ခုတင်အောက်လို့ ပြောတယ်။
ฉันถามว่าลูกอยู่ไหน สามีที่หลับอยู่ตอบว่า ใต้เตียง
Tôi hỏi con đâu. Chồng đang ngủ đáp: dưới gầm giường.
Pregunté dónde estaba mi bebé. Mi marido dormido dijo: debajo de la cama.
Perguntei onde estava meu bebê. Meu marido dormindo disse: embaixo da cama.
J'ai demandé où était mon bébé. Mon mari endormi a dit : sous le lit.
Ich fragte, wo mein Baby ist. Mein schlafender Mann sagte: unter dem Bett.
Ho chiesto dov'era la mia bimba. Mio marito, dormendo, ha detto: sotto il letto.
Ik vroeg waar mijn baby was. Mijn slapende man zei: onder het bed.
Jag frågade var min bebis var. Min sovande man sa: under sängen.
Zapytałam, gdzie moje dziecko. Śpiący mąż powiedział: pod łóżkiem.
Я спросила, где мой малыш. Спящий муж ответил: под кроватью.
Bebeğimin nerede olduğunu sordum. Uyuyan kocam dedi ki: yatağın altında.
سألت أين طفلتي. قال زوجي النائم: تحت السرير.
赤ちゃんはどこかと尋ねた。眠ったままの夫が言った。ベッドの下。
아기가 어디 있냐고 물었다. 자는 남편이 말했다. 침대 밑.
我问宝宝在哪里。熟睡的丈夫说：床底下。
"""
