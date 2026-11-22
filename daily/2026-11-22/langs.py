CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
भैया की बस एक घंटे पहले टकराई। वो घंटी बजा रहे हैं
அண்ணாவின் பேருந்து ஒரு மணி நேரம் முன் விபத்தானது. அவர் மணி அடிக்கிறார்
అన్న బస్సు గంట క్రితం ప్రమాదానికి గురైంది. ఆయన బెల్ కొడుతున్నాడు
দাদার বাস এক ঘণ্টা আগে দুর্ঘটনায় পড়েছে। সে বেল বাজাচ্ছে
दादाची बस तासाभरापूर्वी अपघातग्रस्त झाली. तो बेल वाजवतोय
بھیا کی بس ایک گھنٹہ پہلے ٹکرائی تھی۔ وہ گھنٹی بجا رہے ہیں
Bumangga ang Bus ni Kuya Isang Oras Na ang Nakalipas. Nagdo-doorbell Siya
Bus Kakakku Kecelakaan Sejam Lalu. Dia Menekan Bel Rumah
Bas Abang Kemalangan Sejam Lalu. Dia Tekan Loceng Rumah
အစ်ကိုရဲ့ဘတ်စ်ကား တစ်နာရီအလိုက မတော်တဆဖြစ်ခဲ့တယ်။ သူ ခေါင်းလောင်းနှိပ်နေတယ်
รถบัสของพี่ชายชนเมื่อชั่วโมงก่อน แต่เขากำลังกดกริ่ง
Xe Buýt Của Anh Tôi Gặp Nạn Một Giờ Trước. Anh Ấy Đang Bấm Chuông
El Autobús de Mi Hermano Chocó Hace Una Hora. Está Tocando el Timbre
O Ônibus do Meu Irmão Bateu Há Uma Hora. Ele Está Tocando a Campainha
Le Bus de Mon Frère a Eu un Accident. Il Sonne à la Porte
Der Bus Meines Bruders Verunglückte Vor Einer Stunde. Er Klingelt
Il Bus di Mio Fratello Si È Schiantato un'Ora Fa. Sta Suonando
De Bus van Mijn Broer Crashte Een Uur Geleden. Hij Belt Aan
Min Brors Buss Krockade för en Timme Sedan. Han Ringer på Dörren
Autobus Mojego Brata Rozbił Się Godzinę Temu. Dzwoni do Drzwi
Автобус Брата Разбился Час Назад. Он Звонит в Дверь
Abimin Otobüsü Bir Saat Önce Kaza Yaptı. Kapı Zilini Çalıyor
حافلة أخي تحطمت قبل ساعة. وهو يرن الجرس الآن
兄のバスは1時間前に事故に遭った。今、玄関のベルを鳴らしている
오빠가 탄 버스가 한 시간 전에 사고 났다. 지금 초인종을 누른다
哥哥的巴士一小时前出事了。他正在按门铃
"""
E1_H = """
भैया की बस एक घंटे पहले टकराई थी, और अब वो हमारे दरवाज़े की घंटी बजा रहे हैं।
அண்ணாவின் பேருந்து ஒரு மணி நேரம் முன் விபத்தானது, இப்போது அவர் எங்கள் வீட்டு மணியை அடிக்கிறார்.
అన్న బస్సు గంట క్రితం ప్రమాదానికి గురైంది, ఇప్పుడు ఆయన మా డోర్‌బెల్ కొడుతున్నాడు.
দাদার বাস এক ঘণ্টা আগে দুর্ঘটনায় পড়েছে, আর এখন সে আমাদের ডোরবেল বাজাচ্ছে।
दादाची बस तासाभरापूर्वी अपघातग्रस्त झाली, आणि आता तो आमची दारावरची बेल वाजवतोय.
بھیا کی بس ایک گھنٹہ پہلے ٹکرائی تھی اور اب وہ ہمارے دروازے کی گھنٹی بجا رہے ہیں۔
Isang oras na ang nakalipas nang bumangga ang bus ni Kuya, at ngayon ay nagdo-doorbell siya.
Bus Kakakku kecelakaan sejam lalu, dan sekarang dia menekan bel pintu kami.
Bas Abang kemalangan sejam lalu, dan sekarang dia menekan loceng pintu kami.
အစ်ကိုရဲ့ဘတ်စ်ကား တစ်နာရီအလိုက မတော်တဆဖြစ်ခဲ့ပြီး အခု ကျွန်တော်တို့တံခါးခေါင်းလောင်းကို နှိပ်နေတယ်။
รถบัสของพี่ชายชนเมื่อชั่วโมงก่อน และตอนนี้เขากำลังกดกริ่งบ้านเรา
Xe buýt của anh tôi gặp nạn một giờ trước, và giờ anh ấy đang bấm chuông cửa nhà tôi.
El autobús de mi hermano chocó hace una hora, y ahora está tocando nuestro timbre.
O ônibus do meu irmão bateu há uma hora, e agora ele está tocando a nossa campainha.
Le bus de mon frère a eu un accident il y a une heure, et maintenant il sonne à notre porte.
Der Bus meines Bruders verunglückte vor einer Stunde, und jetzt klingelt er an unserer Tür.
Il bus di mio fratello si è schiantato un'ora fa, e ora sta suonando al nostro campanello.
De bus van mijn broer crashte een uur geleden, en nu belt hij bij ons aan.
Min brors buss krockade för en timme sedan, och nu ringer han på vår dörr.
Autobus mojego brata rozbił się godzinę temu, a teraz dzwoni do naszych drzwi.
Автобус моего брата разбился час назад, а теперь он звонит в нашу дверь.
Abimin otobüsü bir saat önce kaza yaptı ve şimdi kapı zilimizi çalıyor.
حافلة أخي تحطمت قبل ساعة، والآن هو يرن جرس بابنا.
兄のバスは1時間前に事故に遭ったのに、今、うちの玄関のベルを鳴らしている。
오빠가 탄 버스는 한 시간 전에 사고가 났는데, 지금 우리 집 초인종을 누르고 있다.
哥哥的巴士一小时前出了事，现在他正在按我们家的门铃。
"""
E2_T = """
छत · भाग 1: दादी ने छत बंद की थी। वहाँ गीले कपड़े टंगे हैं
மொட்டை மாடி · பகுதி 1: பாட்டி பூட்டினாள். ஈரத் துணிகள் தொங்குகின்றன
టెర్రస్ · పార్ట్ 1: అమ్మమ్మ తాళం వేసింది. తడి బట్టలు వేలాడుతున్నాయి
ছাদ · পর্ব ১: দিদা তালা দিয়েছিল। সেখানে ভেজা কাপড় ঝোলে
गच्ची · भाग १: आजीने कुलूप लावले. तिथे ओले कपडे लटकतात
چھت · حصہ 1: دادی نے تالا لگایا تھا۔ وہاں گیلے کپڑے لٹکتے ہیں
Terrace · Pt 1: Ni-lock ni Lola. May Basang Damit Doon
Teras · Pt 1: Nenek Mengunci Teras. Ada Baju Basah Tergantung
Teres · Pt 1: Nenek Kunci Teres. Ada Baju Basah Tergantung
အပေါ်ထပ်ခေါင်မိုး · အပိုင်း ၁။ အဘွားသော့ခတ်ခဲ့တယ်။ အဝတ်စိုတွေ ချိတ်ထားတယ်
ดาดฟ้า · ตอน 1: ย่าล็อกไว้ แต่มีผ้าเปียกแขวนอยู่
Sân Thượng · Pt 1: Bà Đã Khóa. Quần Áo Ướt Vẫn Treo Ở Đó
Terraza · Pt 1: Abuela la Cerró. Hay Ropa Mojada Colgada
Terraço · Pt 1: A Vovó Trancou. Há Roupa Molhada Pendurada
Terrasse · Pt 1 : Mamie l'a Fermée. Du Linge Mouillé y Pend
Dachterrasse · Pt 1: Oma Schloss Sie Ab. Nasse Wäsche Hängt Dort
Terrazza · Pt 1: La Nonna l'Ha Chiusa. Panni Bagnati Stesi
Terras · Pt 1: Oma Sloot Het Af. Er Hangt Natte Was
Terrass · Pt 1: Farmor Låste. Blöt Tvätt Hänger Där
Taras · Pt 1: Babcia Go Zamknęła. Wisi Tam Mokre Pranie
Терраса · Ч. 1: Бабушка Её Заперла. Там Висит Мокрое Бельё
Teras · Bölüm 1: Babaanne Kilitledi. Orada Islak Çamaşır Asılı
السطح · ج1: جدتي أغلقته. والملابس المبللة معلقة هناك
屋上 · 第1話：祖母が鍵をかけた。濡れた服が干してある
옥상 · 1부: 할머니가 잠갔다. 젖은 빨래가 걸려 있다
天台 · 第1集：奶奶锁了门。湿衣服却挂在那里
"""
E2_H = """
दादी ने मरने से पहले छत बंद कर दी थी, पर हर सुबह वहाँ गीले कपड़े टंगे मिलते हैं।
பாட்டி இறக்கும் முன் மொட்டை மாடியைப் பூட்டினாள், ஆனாலும் தினமும் விடியலில் ஈரத் துணிகள் தொங்குகின்றன.
అమ్మమ్మ చనిపోయే ముందు టెర్రస్‌కి తాళం వేసింది, అయినా ప్రతి తెల్లవారుజామున తడి బట్టలు వేలాడుతున్నాయి.
দিদা মারা যাওয়ার আগে ছাদে তালা দিয়েছিল, তবু প্রতি ভোরে সেখানে ভেজা কাপড় ঝোলে।
आजीने मरण्यापूर्वी गच्ची बंद केली होती, तरी रोज पहाटे तिथे ओले कपडे लटकलेले असतात.
دادی نے مرنے سے پہلے چھت پر تالا لگا دیا تھا، پھر بھی ہر صبح وہاں گیلے کپڑے لٹکے ہوتے ہیں۔
Ni-lock ni Lola ang terrace bago siya namatay, pero may nakasampay na basang damit doon tuwing madaling-araw.
Nenek mengunci teras sebelum meninggal, tetapi setiap subuh ada baju basah tergantung di sana.
Nenek kunci teres sebelum meninggal, tetapi setiap subuh ada baju basah tergantung di situ.
အဘွားမကွယ်လွန်ခင် ခေါင်မိုးကို သော့ခတ်ခဲ့ပေမယ့် နံနက်တိုင်း အဝတ်စိုတွေ ချိတ်ထားတယ်။
ย่าล็อกดาดฟ้าไว้ก่อนตาย แต่ทุกรุ่งเช้ามีผ้าเปียกแขวนอยู่ที่นั่น
Bà đã khóa sân thượng trước khi mất, nhưng mỗi bình minh vẫn có quần áo ướt treo ở đó.
La abuela cerró la terraza antes de morir, pero cada amanecer cuelga ropa mojada allí.
A vovó trancou o terraço antes de morrer, mas toda madrugada há roupa molhada pendurada lá.
Mamie a fermé la terrasse avant de mourir, mais chaque aube du linge mouillé y est étendu.
Oma schloss die Dachterrasse vor ihrem Tod ab, doch jeden Morgen hängt dort nasse Wäsche.
La nonna ha chiuso la terrazza prima di morire, ma ogni alba lì ci sono panni bagnati.
Oma sloot het terras af voor haar dood, maar elke ochtend hangt er natte was.
Farmor låste terrassen innan hon dog, men varje gryning hänger blöt tvätt där.
Babcia zamknęła taras przed śmiercią, a mimo to co świt wisi tam mokre pranie.
Бабушка заперла террасу перед смертью, но каждый рассвет там висит мокрое бельё.
Babaanne ölmeden önce terası kilitledi, ama her şafak orada ıslak çamaşırlar asılı oluyor.
أغلقت جدتي السطح قبل موتها، ومع ذلك تُعلَّق ملابس مبللة هناك كل فجر.
祖母は亡くなる前に屋上に鍵をかけたのに、毎朝そこには濡れた服が干してある。
할머니는 돌아가시기 전에 옥상을 잠갔는데, 매일 새벽 젖은 빨래가 걸려 있다.
奶奶去世前锁了天台，可每天黎明那里都挂着湿衣服。
"""
E3_T = """
छत · भाग 2: दादी ने पति की शर्ट टांगी। वो भीग रहे थे
மொட்டை மாடி · பகுதி 2: பாட்டி என் கணவர் சட்டையைத் தொங்கவிட்டாள்
టెర్రస్ · పార్ట్ 2: అమ్మమ్మ నా భర్త చొక్కా ఆరేసింది. అతను తడిసాడు
ছাদ · পর্ব ২: দিদা আমার স্বামীর শার্ট মেলেছিল। সে ভিজে গেল
गच्ची · भाग २: आजीने नवऱ्याचा शर्ट टांगला. तो भिजत होता
چھت · حصہ 2: دادی نے میرے شوہر کی شرٹ لٹکائی۔ وہ بھیگ رہے تھے
Terrace · Pt 2: Isinampay ni Lola ang Damit ng Asawa Ko. Basa Siya
Teras · Pt 2: Nenek Menjemur Baju Suamiku. Dia Basah Kuyup
Teres · Pt 2: Nenek Jemur Baju Suami Saya. Dia Basah Kuyup
အပေါ်ထပ်ခေါင်မိုး · အပိုင်း ၂။ အဘွားက ခင်ပွန်းရဲ့ရှပ်အင်္ကျီ လှန်းတယ်
ดาดฟ้า · ตอน 2: ย่าตากเสื้อสามีฉัน เขาตัวเปียกโชก
Sân Thượng · Pt 2: Bà Phơi Áo Chồng Tôi. Anh Ấy Ướt Sũng
Terraza · Pt 2: La Abuela Tendió la Camisa de Mi Esposo. Él Estaba Mojado
Terraço · Pt 2: A Vovó Estendeu a Camisa do Meu Marido. Ele Estava Molhado
Terrasse · Pt 2 : Mamie a Étendu la Chemise de Mon Mari. Il Était Trempé
Dachterrasse · Pt 2: Oma Hängte Das Hemd Meines Mannes Auf. Er War Nass
Terrazza · Pt 2: La Nonna Stese la Camicia di Mio Marito. Lui Era Bagnato
Terras · Pt 2: Oma Hing Het Overhemd van Mijn Man Op. Hij Was Nat
Terrass · Pt 2: Farmor Hängde Min Mans Skjorta. Han Var Dyngblöt
Taras · Pt 2: Babcia Powiesiła Koszulę Mojego Męża. Był Mokry
Терраса · Ч. 2: Бабушка Повесила Рубашку Мужа. Он Был Мокрый
Teras · Bölüm 2: Babaanne Kocamın Gömleğini Astı. O Sırılsıklamdı
السطح · ج2: جدتي نشرت قميص زوجي. وكان هو مبللاً
屋上 · 第2話：祖母が夫のシャツを干した。夫はずぶ濡れだった
옥상 · 2부: 할머니가 남편 셔츠를 널었다. 남편은 젖어 있었다
天台 · 第2集：奶奶晾起了我丈夫的衬衫。他浑身湿透
"""
E3_H = """
दादी छत पर मेरे पति की शर्ट टांग रही थीं, और नीचे वो पानी की खाँसी कर रहे थे।
பாட்டி மொட்டை மாடியில் என் கணவர் சட்டையைத் தொங்கவிட்டாள், கீழே அவர் தண்ணீரை இருமிக் கொண்டிருந்தார்.
అమ్మమ్మ టెర్రస్‌పై నా భర్త చొక్కా ఆరేస్తోంది, కింద ఆయన నీళ్లు దగ్గుతున్నాడు.
দিদা ছাদে আমার স্বামীর শার্ট মেলছিল, আর নিচে সে জল কাশছিল।
आजी गच्चीवर नवऱ्याचा शर्ट टांगत होती, आणि खाली तो पाणी ओकत खोकत होता.
دادی چھت پر میرے شوہر کی شرٹ لٹکا رہی تھیں اور نیچے وہ پانی کھانس رہے تھے۔
Isinasampay ni Lola ang damit ng asawa ko sa terrace, at sa ibaba ay inuubo siya ng tubig.
Nenek menjemur baju suamiku di teras, dan di bawah dia terbatuk-batuk memuntahkan air.
Nenek jemur baju suami saya di teres, dan di bawah dia batuk-batuk memuntahkan air.
အဘွားက ခေါင်မိုးပေါ်မှာ ခင်ပွန်းရဲ့ရှပ်အင်္ကျီကို လှန်းနေပြီး အောက်မှာ သူ ရေတွေ ချောင်းဆိုးနေတယ်။
ย่ากำลังตากเสื้อสามีฉันบนดาดฟ้า ส่วนข้างล่างเขาไอเอาน้ำออกมา
Bà đang phơi áo chồng tôi trên sân thượng, còn dưới nhà anh ấy ho ra nước.
La abuela tendía la camisa de mi esposo en la terraza y abajo él tosía agua.
A vovó estendia a camisa do meu marido no terraço e lá embaixo ele tossia água.
Mamie étendait la chemise de mon mari sur la terrasse, et en bas il toussait de l'eau.
Oma hängte auf der Dachterrasse das Hemd meines Mannes auf, und unten hustete er Wasser.
La nonna stendeva la camicia di mio marito in terrazza, e di sotto lui tossiva acqua.
Oma hing op het terras het overhemd van mijn man op, en beneden hoestte hij water op.
Farmor hängde upp min mans skjorta på terrassen, och där nere hostade han vatten.
Babcia wieszała na tarasie koszulę mojego męża, a na dole on kaszlał wodą.
Бабушка вешала на террасе рубашку моего мужа, а внизу он кашлял водой.
Babaanne terasta kocamın gömleğini asıyordu, aşağıda ise o su öksürüyordu.
كانت جدتي تنشر قميص زوجي على السطح، وفي الأسفل كان يسعل ماءً.
祖母が屋上で夫のシャツを干している間、下で夫は水を吐いて咳き込んでいた。
할머니가 옥상에서 남편 셔츠를 너는 동안, 아래층에서 남편은 물을 토하며 기침하고 있었다.
奶奶在天台晾我丈夫的衬衫时，楼下的他正咳出水来。
"""
