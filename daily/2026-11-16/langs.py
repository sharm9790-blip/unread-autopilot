CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
माँ ने दो बार शुभरात्रि कहा। माँ मेरे पास सो रही थी
அம்மா இருமுறை குட்நைட் சொன்னாள். அம்மா என் அருகில் தூங்கினாள்
అమ్మ రెండుసార్లు గుడ్‌నైట్ చెప్పింది. అమ్మ నా పక్కనే నిద్రపోతోంది
মা দুবার শুভরাত্রি বলল। মা আমার পাশেই ঘুমিয়ে ছিল
आईने दोनदा गुडनाईट म्हटलं. आई माझ्या शेजारी झोपली होती
امی نے دو بار شب بخیر کہا۔ امی میرے پاس سو رہی تھیں
Dalawang Beses Nag-Goodnight si Mama. Tulog Siya Katabi Ko
Ibu Bilang Selamat Malam Dua Kali. Ibu Tidur di Sebelahku
Ibu Kata Selamat Malam Dua Kali. Ibu Tidur di Sebelahku
အမေ ညကောင်းပါစေ နှစ်ကြိမ်ပြောတယ်။ အမေက ကျွန်မဘေးမှာ အိပ်နေတယ်
แม่บอกฝันดีสองครั้ง แต่แม่หลับอยู่ข้างฉัน
Mẹ Chúc Ngủ Ngon Hai Lần. Mẹ Đang Ngủ Cạnh Tôi
Mamá Dijo Buenas Noches Dos Veces. Dormía a Mi Lado
A Mãe Disse Boa Noite Duas Vezes. Ela Dormia Ao Meu Lado
Maman a Dit Bonne Nuit Deux Fois. Elle Dormait à Côté de Moi
Mama Sagte Zweimal Gute Nacht. Sie Schlief Neben Mir
Mamma Ha Detto Buonanotte Due Volte. Dormiva Accanto a Me
Mama Zei Twee Keer Welterusten. Ze Sliep Naast Me
Mamma Sa God Natt Två Gånger. Hon Sov Bredvid Mig
Mama Powiedziała Dobranoc Dwa Razy. Spała Obok Mnie
Мама Дважды Пожелала Спокойной Ночи. Она Спала Рядом
Annem İki Kez İyi Geceler Dedi. Yanımda Uyuyordu
قالت أمي تصبحين على خير مرتين. وكانت نائمة بجانبي
ママはおやすみを2回言った。ママは隣で寝ていた
엄마가 잘 자라고 두 번 말했다. 엄마는 내 옆에서 자고 있었다
妈妈说了两次晚安。妈妈却睡在我身边
"""
E1_H = """
माँ ने दो बार शुभरात्रि कहा। दूसरी बार हॉल से आवाज़ आई।
அம்மா இருமுறை குட்நைட் சொன்னாள். இரண்டாவது முறை நடைபாதையிலிருந்து.
అమ్మ రెండుసార్లు గుడ్‌నైట్ చెప్పింది. రెండోసారి హాల్లోంచి.
মা দুবার শুভরাত্রি বলল। দ্বিতীয়বার করিডোর থেকে।
आईने दोनदा गुडनाईट म्हटलं. दुसऱ्यांदा हॉलमधून.
امی نے دو بار شب بخیر کہا۔ دوسری بار راہداری سے۔
Dalawang beses nag-goodnight si Mama. Ang pangalawa ay galing sa pasilyo.
Ibu bilang selamat malam dua kali. Yang kedua dari lorong.
Ibu kata selamat malam dua kali. Yang kedua dari lorong.
အမေ ညကောင်းပါစေ နှစ်ကြိမ်ပြောတယ်။ ဒုတိယအကြိမ်က စင်္ကြံကနေ။
แม่บอกฝันดีสองครั้ง ครั้งที่สองมาจากทางเดิน
Mẹ chúc ngủ ngon hai lần. Lần thứ hai vọng từ hành lang.
Mamá dijo buenas noches dos veces. La segunda vino del pasillo.
A mãe disse boa noite duas vezes. A segunda veio do corredor.
Maman a dit bonne nuit deux fois. La seconde venait du couloir.
Mama sagte zweimal Gute Nacht. Das zweite Mal vom Flur.
Mamma ha detto buonanotte due volte. La seconda dal corridoio.
Mama zei twee keer welterusten. De tweede keer vanuit de gang.
Mamma sa god natt två gånger. Andra gången från hallen.
Mama powiedziała dobranoc dwa razy. Drugi raz z korytarza.
Мама дважды пожелала спокойной ночи. Второй раз из коридора.
Annem iki kez iyi geceler dedi. İkincisi koridordan geldi.
قالت أمي تصبحين على خير مرتين. والثانية جاءت من الممر.
ママはおやすみを2回言った。2回目は廊下からだった。
엄마가 잘 자라고 두 번 말했다. 두 번째는 복도에서였다.
妈妈说了两次晚安。第二次是从走廊传来的。
"""
E2_T = """
कुत्ते की चेतावनी Pt 1: मेरा कुत्ता पत्नी पर गुर्राना बंद कर गया
நாயின் எச்சரிக்கை Pt 1: என் நாய் மனைவியைப் பார்த்து உறுமுவதை நிறுத்தியது
కుక్క హెచ్చరిక Pt 1: నా కుక్క నా భార్యపై గుర్రుమనడం ఆపింది
কুকুরের সতর্কতা Pt 1: আমার কুকুর স্ত্রীর দিকে গর্জন থামাল
कुत्र्याचा इशारा Pt 1: माझ्या कुत्र्याने बायकोवर गुरगुरणं थांबवलं
کتے کی وارننگ Pt 1: میرے کتے نے بیوی پر غرانا بند کر دیا
Babala ng Aso Pt 1: Tumigil ang Aso Ko sa Pag-ungol sa Asawa Ko
Peringatan Anjing Pt 1: Anjingku Berhenti Menggeram pada Istriku
Amaran Anjing Pt 1: Anjing Saya Berhenti Menggeram pada Isteri
ခွေးသတိပေးချက် Pt 1: ကျွန်တော့်ခွေး ဇနီးကို ဟောင်တာ ရပ်သွားတယ်
คำเตือนจากหมา Pt 1: หมาของผมหยุดขู่ภรรยาผม
Chó Cảnh Báo Pt 1: Chó Tôi Thôi Gầm Gừ Vợ Tôi
Aviso del Perro Pt 1: Mi Perro Dejó de Gruñirle a Mi Esposa
Aviso do Cão Pt 1: Meu Cão Parou de Rosnar Para Minha Esposa
Chien Alerte Pt 1: Mon Chien Ne Grogne Plus Contre Ma Femme
Hundewarnung Pt 1: Mein Hund Hörte Auf, Meine Frau Anzuknurren
Avviso del Cane Pt 1: Il Mio Cane Ha Smesso di Ringhiare a Mia Moglie
Hondenwaarschuwing Pt 1: Mijn Hond Stopte met Grommen naar Mijn Vrouw
Hundvarning Pt 1: Min Hund Slutade Morra åt Min Fru
Ostrzeżenie Psa Pt 1: Mój Pies Przestał Warczeć na Żonę
Предупреждение Пса Pt 1: Мой Пёс Перестал Рычать на Жену
Köpeğin Uyarısı Pt 1: Köpeğim Karıma Hırlamayı Bıraktı
تحذير الكلب Pt 1: كلبي توقف عن النباح على زوجتي
犬の警告 Pt 1: 犬が妻に唸るのをやめた
개의 경고 Pt 1: 우리 개가 아내에게 으르렁거리길 멈췄다
狗的警告 Pt 1: 我的狗不再对妻子低吼了
"""
E2_H = """
मेरा कुत्ता रोज़ रात पत्नी पर गुर्राता था। आज रात वह चुप हो गया।
என் நாய் தினமும் மனைவியைப் பார்த்து உறுமும். இன்றிரவு அமைதியானது.
నా కుక్క ప్రతి రాత్రి నా భార్యపై గుర్రుమనేది. ఈ రాత్రి మౌనంగా ఉంది.
আমার কুকুর রোজ রাতে স্ত্রীর দিকে গর্জন করত। আজ রাতে চুপ।
माझा कुत्रा रोज रात्री बायकोवर गुरगुरायचा. आज रात्री शांत झाला.
میرا کتا ہر رات بیوی پر غراتا تھا۔ آج رات خاموش ہو گیا۔
Gabi-gabi inuungol ng aso ko ang asawa ko. Ngayong gabi, tumahimik siya.
Anjingku menggeram pada istriku tiap malam. Malam ini dia diam.
Anjing saya menggeram pada isteri setiap malam. Malam ini dia diam.
ကျွန်တော့်ခွေးက ညတိုင်း ဇနီးကို ဟောင်တယ်။ ဒီည တိတ်သွားတယ်။
หมาผมขู่ภรรยาทุกคืน คืนนี้มันเงียบไป
Chó tôi gầm gừ vợ tôi mỗi đêm. Đêm nay nó im lặng.
Mi perro le gruñía a mi esposa cada noche. Esta noche se quedó callado.
Meu cão rosnava para minha esposa toda noite. Hoje ele ficou quieto.
Mon chien grognait contre ma femme chaque nuit. Ce soir, il s'est tu.
Mein Hund knurrte meine Frau jede Nacht an. Heute Nacht war er still.
Il mio cane ringhiava a mia moglie ogni notte. Stanotte è rimasto zitto.
Mijn hond gromde elke nacht naar mijn vrouw. Vannacht was hij stil.
Min hund morrade åt min fru varje natt. I natt blev han tyst.
Mój pies warczał na żonę co noc. Dziś w nocy ucichł.
Мой пёс каждую ночь рычал на жену. Сегодня он затих.
Köpeğim her gece karıma hırlardı. Bu gece sustu.
كان كلبي يزمجر على زوجتي كل ليلة. الليلة صمت.
犬は毎晩、妻に唸っていた。今夜は静かだった。
우리 개는 매일 밤 아내에게 으르렁거렸다. 오늘 밤은 조용했다.
我的狗每晚都对妻子低吼。今晚它安静了。
"""
E3_T = """
कुत्ते की चेतावनी Pt 2: मेरी असली पत्नी सड़क से चिल्लाई
நாயின் எச்சரிக்கை Pt 2: என் உண்மையான மனைவி தெருவிலிருந்து கத்தினாள்
కుక్క హెచ్చరిక Pt 2: నా అసలైన భార్య వీధిలోంచి అరిచింది
কুকুরের সতর্কতা Pt 2: আমার আসল স্ত্রী রাস্তা থেকে চেঁচাল
कुत्र्याचा इशारा Pt 2: माझी खरी बायको रस्त्यावरून ओरडली
کتے کی وارننگ Pt 2: میری اصلی بیوی سڑک سے چلائی
Babala ng Aso Pt 2: Sumigaw ang Tunay Kong Asawa Mula sa Kalsada
Peringatan Anjing Pt 2: Istri Asliku Berteriak dari Jalan
Amaran Anjing Pt 2: Isteri Sebenar Saya Menjerit dari Jalan
ခွေးသတိပေးချက် Pt 2: ကျွန်တော့်ဇနီးအစစ်က လမ်းပေါ်ကနေ အော်တယ်
คำเตือนจากหมา Pt 2: ภรรยาตัวจริงตะโกนมาจากถนน
Chó Cảnh Báo Pt 2: Vợ Thật Của Tôi Hét Từ Ngoài Đường
Aviso del Perro Pt 2: Mi Esposa de Verdad Gritó Desde la Calle
Aviso do Cão Pt 2: Minha Esposa de Verdade Gritou da Rua
Chien Alerte Pt 2: Ma Vraie Femme a Crié Depuis la Rue
Hundewarnung Pt 2: Meine Echte Frau Rief von der Straße
Avviso del Cane Pt 2: La Mia Vera Moglie Ha Gridato dalla Strada
Hondenwaarschuwing Pt 2: Mijn Echte Vrouw Riep vanaf de Straat
Hundvarning Pt 2: Min Riktiga Fru Ropade från Gatan
Ostrzeżenie Psa Pt 2: Moja Prawdziwa Żona Krzyknęła z Ulicy
Предупреждение Пса Pt 2: Моя Настоящая Жена Крикнула с Улицы
Köpeğin Uyarısı Pt 2: Gerçek Karım Sokaktan Bağırdı
تحذير الكلب Pt 2: زوجتي الحقيقية صرخت من الشارع
犬の警告 Pt 2: 本物の妻が通りから叫んだ
개의 경고 Pt 2: 진짜 아내가 길에서 소리쳤다
狗的警告 Pt 2: 真正的妻子在街上喊了一声
"""
E3_H = """
मेरी पत्नी के रूप में कुछ ने कुत्ते को बुलाया। तभी असली पत्नी चिल्लाई।
மனைவி உருவில் ஏதோ நாயை அழைத்தது. அப்போது உண்மையான மனைவி கத்தினாள்.
భార్య రూపంలో ఏదో కుక్కను పిలిచింది. అప్పుడు అసలు భార్య అరిచింది.
স্ত্রীর রূপে কিছু একটা কুকুরকে ডাকল। তখন আসল স্ত্রী চেঁচাল।
बायकोच्या रूपातल्या कशाने कुत्र्याला हाक मारली. तेव्हा खरी बायको ओरडली.
بیوی کی شکل میں کسی چیز نے کتے کو بلایا۔ پھر اصلی بیوی چلائی۔
May tumawag sa aso ko na kamukha ng asawa ko. Saka sumigaw ang tunay.
Sesuatu berwujud istriku memanggil anjingku. Lalu istri asliku berteriak.
Sesuatu berupa isteri saya memanggil anjing saya. Lalu isteri sebenar menjerit.
ဇနီးပုံစံနဲ့ တစ်ခုခုက ခွေးကိုခေါ်တယ်။ ဒါနဲ့ ဇနီးအစစ်က အော်တယ်။
บางสิ่งในร่างภรรยาเรียกหมาของผม แล้วภรรยาตัวจริงก็ตะโกน
Thứ mang hình vợ tôi gọi con chó ra. Rồi vợ thật hét lên.
Algo con la forma de mi esposa llamó al perro. Entonces gritó la de verdad.
Algo com a forma da minha esposa chamou o cão. Então a de verdade gritou.
Quelque chose sous les traits de ma femme a appelé le chien. Puis la vraie a crié.
Etwas in der Gestalt meiner Frau rief den Hund. Dann schrie die echte.
Qualcosa con la forma di mia moglie ha chiamato il cane. Poi ha gridato quella vera.
Iets in de gedaante van mijn vrouw riep de hond. Toen riep de echte.
Något i min frus skepnad kallade på hunden. Sedan ropade den riktiga.
Coś w postaci mojej żony zawołało psa. Wtedy krzyknęła prawdziwa.
Нечто в облике жены позвало пса. Потом закричала настоящая.
Karımın suretindeki bir şey köpeği çağırdı. Sonra gerçek karım bağırdı.
نادى شيء بهيئة زوجتي كلبي. ثم صرخت زوجتي الحقيقية.
妻の姿をした何かが犬を呼んだ。そのとき本物の妻が叫んだ。
아내의 모습을 한 무언가가 개를 불렀다. 그때 진짜 아내가 소리쳤다.
妻子模样的东西叫出了狗。这时真正的妻子喊了起来。
"""
