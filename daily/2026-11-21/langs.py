CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
मेरे पति ऊपर से फोन कर रहे हैं। वे मेरे बगल में खड़े हैं
என் கணவர் மாடியிலிருந்து அழைக்கிறார். அவர் என் அருகிலேயே நிற்கிறார்
నా భర్త పై అంతస్తు నుంచి ఫోన్ చేస్తున్నారు. ఆయన నా పక్కనే ఉన్నారు
আমার স্বামী ওপর থেকে ফোন করছে। সে তো আমার পাশেই দাঁড়িয়ে
माझे पती वरून फोन करत आहेत. ते माझ्या शेजारीच उभे आहेत
میرے شوہر اوپر سے فون کر رہے ہیں۔ وہ میرے ساتھ کھڑے ہیں
Tumatawag ang Asawa Ko Mula sa Itaas. Nasa Tabi Ko Siya
Suamiku Menelepon dari Lantai Atas. Dia Berdiri di Sampingku
Suami Saya Telefon dari Tingkat Atas. Dia Berdiri di Sebelah Saya
ကျွန်မခင်ပွန်း အပေါ်ထပ်ကခေါ်နေတယ်။ သူက ကျွန်မဘေးမှာရပ်နေတယ်
สามีโทรมาจากชั้นบน แต่เขายืนอยู่ข้างฉัน
Chồng Tôi Gọi Điện Từ Trên Lầu. Anh Ấy Đang Đứng Cạnh Tôi
Mi Esposo Llama Desde Arriba. Está de Pie a Mi Lado
Meu Marido Liga do Andar de Cima. Ele Está ao Meu Lado
Mon Mari Appelle d'en Haut. Il Est Debout à Côté de Moi
Mein Mann Ruft von Oben An. Er Steht Neben Mir
Mio Marito Chiama dal Piano di Sopra. È Accanto a Me
Mijn Man Belt Van Boven. Hij Staat Naast Me
Min Man Ringer Från Övervåningen. Han Står Bredvid Mig
Mąż Dzwoni z Góry. Stoi Obok Mnie
Муж Звонит Сверху. Он Стоит Рядом Со Мной
Kocam Üst Kattan Arıyor. Yanımda Duruyor
زوجي يتصل من الطابق العلوي. وهو واقف بجانبي
夫が2階から電話してくる。でも彼は私の隣にいる
남편이 위층에서 전화해요. 그런데 바로 제 옆에 있어요
老公从楼上打来电话。可他就站在我身边
"""
E1_H = """
मेरे पति ऊपर से मुझे फोन कर रहे हैं।
என் கணவர் மாடியிலிருந்து எனக்கு அழைக்கிறார்.
నా భర్త పై అంతస్తు నుంచి నాకు ఫోన్ చేస్తున్నారు.
আমার স্বামী ওপর থেকে আমাকে ফোন করছে।
माझे पती वरून मला फोन करत आहेत.
میرے شوہر اوپر سے مجھے فون کر رہے ہیں۔
Tumatawag sa akin ang asawa ko mula sa itaas.
Suamiku menelepon dari lantai atas.
Suami saya menelefon dari tingkat atas.
ကျွန်မခင်ပွန်း အပေါ်ထပ်ကနေ ကျွန်မကို ဖုန်းခေါ်နေတယ်။
สามีโทรหาฉันจากชั้นบน
Chồng tôi đang gọi điện từ trên lầu.
Mi esposo me llama desde arriba.
Meu marido está me ligando do andar de cima.
Mon mari m'appelle d'en haut.
Mein Mann ruft mich von oben an.
Mio marito mi chiama dal piano di sopra.
Mijn man belt me van boven.
Min man ringer mig från övervåningen.
Mój mąż dzwoni do mnie z góry.
Муж звонит мне сверху.
Kocam beni üst kattan arıyor.
زوجي يتصل بي من الطابق العلوي.
夫が2階から私に電話してきている。
남편이 위층에서 저에게 전화하고 있어요.
老公正从楼上给我打电话。
"""
E2_T = """
लोरी Pt 1: कोई मेरे बच्चे को लोरी सुना रहा है। माँ की आवाज़ नहीं है
தாலாட்டு Pt 1: என் குழந்தைக்கு யாரோ பாடுகிறார்கள். அம்மாவுக்கு குரலே இல்லை
లాలి Pt 1: నా బిడ్డకు ఎవరో పాడుతున్నారు. అమ్మకు గొంతు లేదు
ঘুমপাড়ানি Pt 1: কেউ আমার শিশুকে গান শোনাচ্ছে। মায়ের কণ্ঠ নেই
अंगाई Pt 1: कोणीतरी माझ्या बाळाला गाणे म्हणतंय. आईला आवाजच नाही
لوری Pt 1: کوئی میرے بچے کو لوری سنا رہا ہے۔ امی کی آواز نہیں ہے
Oyayi Pt 1: May Umaawit sa Baby Ko. Walang Boses si Mama
Lagu Nina Bobo Pt 1: Ada yang Menyanyi untuk Bayiku. Ibu Tak Punya Suara
Lagu Dodoi Pt 1: Ada yang Menyanyi untuk Bayi Saya. Ibu Tiada Suara
ညည်းတွားသီချင်း Pt 1: ကျွန်မကလေးကို တစ်ယောက်ယောက်သီဆိုပေးနေတယ်။ အမေ့မှာ အသံမရှိဘူး
เพลงกล่อม Pt 1: มีใครร้องเพลงกล่อมลูกฉัน แต่แม่ไม่มีเสียง
Hát Ru Pt 1: Ai Đó Hát Cho Con Tôi. Mẹ Tôi Mất Giọng
Nana Pt 1: Alguien Le Canta a Mi Bebé. Mamá No Tiene Voz
Cantiga de Ninar Pt 1: Alguém Canta para Meu Bebê. Mamãe Perdeu a Voz
Berceuse Pt 1: Quelqu'un Chante pour Mon Bébé. Maman N'a Plus de Voix
Wiegenlied Pt 1: Jemand Singt für Mein Baby. Mama Hat Keine Stimme
Ninna Nanna Pt 1: Qualcuno Canta al Mio Bambino. Mamma Non Ha Voce
Wiegenlied Pt 1: Iemand Zingt voor Mijn Baby. Mama Heeft Geen Stem
Vaggvisa Pt 1: Någon Sjunger för Min Bebis. Mamma Har Ingen Röst
Kołysanka Pt 1: Ktoś Śpiewa Mojemu Dziecku. Mama Nie Ma Głosu
Колыбельная Pt 1: Кто-то Поёт Моему Малышу. У Мамы Нет Голоса
Ninni Pt 1: Biri Bebeğime Şarkı Söylüyor. Annemin Sesi Yok
تهويدة Pt 1: أحدهم يغني لطفلي. وأمي بلا صوت
子守唄 Pt 1: 誰かが赤ちゃんに歌っている。母は声を失ったのに
자장가 Pt 1: 누군가 아기에게 노래해요. 엄마는 목소리가 없는데
摇篮曲 Pt 1: 有人给我的宝宝唱歌。妈妈早已失声
"""
E2_H = """
कोई मेरे बच्चे को गा रहा है, पर माँ की आवाज़ चली गई है।
என் குழந்தைக்கு யாரோ பாடுகிறார்கள், ஆனால் அம்மாவுக்கு குரல் இல்லை.
నా బిడ్డకు ఎవరో పాడుతున్నారు, కానీ అమ్మకు గొంతు లేదు.
কেউ আমার শিশুর জন্য গান গাইছে, অথচ মায়ের কণ্ঠ নেই।
कोणीतरी माझ्या बाळासाठी गात आहे, पण आईला आवाज नाही.
کوئی میرے بچے کے لیے گا رہا ہے، مگر امی کی آواز نہیں ہے۔
May umaawit sa baby ko, pero walang boses si Mama.
Ada yang menyanyi untuk bayiku, tapi Ibu tak punya suara.
Ada yang menyanyi untuk bayi saya, tetapi Ibu tiada suara.
ကျွန်မကလေးအတွက် တစ်ယောက်ယောက် သီဆိုနေတယ်၊ ဒါပေမယ့် အမေ့မှာ အသံမရှိဘူး။
มีใครบางคนร้องเพลงให้ลูกฉัน แต่แม่ไม่มีเสียง
Có ai đó đang hát cho con tôi, nhưng mẹ tôi đã mất giọng.
Alguien le canta a mi bebé, pero mamá no tiene voz.
Alguém canta para meu bebê, mas mamãe perdeu a voz.
Quelqu'un chante pour mon bébé, mais maman n'a plus de voix.
Jemand singt für mein Baby, aber Mama hat keine Stimme.
Qualcuno canta al mio bambino, ma mamma non ha voce.
Iemand zingt voor mijn baby, maar mama heeft geen stem.
Någon sjunger för min bebis, men mamma har ingen röst.
Ktoś śpiewa mojemu dziecku, ale mama nie ma głosu.
Кто-то поёт моему малышу, но у мамы нет голоса.
Biri bebeğime şarkı söylüyor ama annemin sesi yok.
أحدهم يغني لطفلي، لكن أمي بلا صوت.
誰かが赤ちゃんに歌っているが、母は声を失っている。
누군가 아기에게 노래하고 있는데, 엄마는 목소리가 없어요.
有人在给我的宝宝唱歌，可妈妈已经失声了。
"""
E3_T = """
लोरी Pt 2: माँ की आवाज़ लौट आई। मेरे बच्चे के होंठ हिल रहे थे
தாலாட்டு Pt 2: அம்மாவின் குரல் திரும்பியது. என் குழந்தையின் உதடுகள் அசைந்தன
లాలి Pt 2: అమ్మ గొంతు తిరిగొచ్చింది. నా బిడ్డ పెదవులు కదిలాయి
ঘুমপাড়ানি Pt 2: মায়ের কণ্ঠ ফিরে এল। আমার শিশুর ঠোঁট নড়ছিল
अंगाई Pt 2: आईचा आवाज परत आला. माझ्या बाळाचे ओठ हलत होते
لوری Pt 2: امی کی آواز واپس آ گئی۔ میرے بچے کے ہونٹ ہل رہے تھے
Oyayi Pt 2: Bumalik ang Boses ni Mama. Gumagalaw ang Labi ng Baby Ko
Lagu Nina Bobo Pt 2: Suara Ibu Kembali. Bibir Bayiku Bergerak
Lagu Dodoi Pt 2: Suara Ibu Kembali. Bibir Bayi Saya Bergerak
ညည်းတွားသီချင်း Pt 2: အမေ့အသံပြန်လာတယ်။ ကျွန်မကလေးရဲ့နှုတ်ခမ်း လှုပ်နေတယ်
เพลงกล่อม Pt 2: เสียงแม่กลับมา และริมฝีปากลูกฉันขยับตาม
Hát Ru Pt 2: Giọng Mẹ Đã Trở Lại. Môi Con Tôi Mấp Máy
Nana Pt 2: A Mamá Le Volvió la Voz. Mi Bebé Movía los Labios
Cantiga de Ninar Pt 2: A Voz da Mamãe Voltou. Os Lábios do Bebê Se Moviam
Berceuse Pt 2: La Voix de Maman Est Revenue. Les Lèvres de Mon Bébé Bougeaient
Wiegenlied Pt 2: Mamas Stimme Kam Zurück. Die Lippen Meines Babys Bewegten Sich
Ninna Nanna Pt 2: La Voce di Mamma È Tornata. Le Labbra del Bimbo Si Muovevano
Wiegenlied Pt 2: Mama's Stem Kwam Terug. De Lippen van Mijn Baby Bewogen
Vaggvisa Pt 2: Mammas Röst Kom Tillbaka. Min Bebis Läppar Rörde Sig
Kołysanka Pt 2: Głos Mamy Wrócił. Usta Mojego Dziecka Się Poruszały
Колыбельная Pt 2: Голос Мамы Вернулся. Губы Малыша Двигались
Ninni Pt 2: Annemin Sesi Geri Geldi. Bebeğimin Dudakları Kıpırdıyordu
تهويدة Pt 2: عاد صوت أمي. وكانت شفتا طفلي تتحركان
子守唄 Pt 2: 母の声が戻った。赤ちゃんの唇が動いていた
자장가 Pt 2: 엄마 목소리가 돌아왔다. 아기의 입술이 움직였다
摇篮曲 Pt 2: 妈妈的声音回来了。宝宝的嘴唇在动
"""
E3_H = """
लोरी के साथ कभी गुनगुनाना मत।
தாலாட்டுக்கு பதிலாக ஒருபோதும் முணுமுணுக்காதே.
లాలికి ఎప్పుడూ తిరిగి హమ్ చేయకు.
ঘুমপাড়ানি গানের সঙ্গে কখনো গুনগুন কোরো না।
अंगाईला कधीही गुणगुणत उत्तर देऊ नका.
لوری کے ساتھ کبھی گنگنانا مت۔
Huwag kang hu-hum pabalik sa oyayi.
Jangan pernah bersenandung membalas lagu nina bobo.
Jangan sekali-kali bersenandung membalas lagu dodoi.
ညည်းတွားသီချင်းကို ဘယ်တော့မှ ပြန်မညည်းနဲ့။
อย่าฮัมตอบเพลงกล่อมเด็ดขาด
Đừng bao giờ ngân nga đáp lại bài hát ru.
Nunca tararees de vuelta a la nana.
Nunca cantarole de volta a cantiga de ninar.
Ne fredonne jamais en réponse à la berceuse.
Summe niemals zum Wiegenlied zurück.
Non canticchiare mai in risposta alla ninna nanna.
Neurie nooit terug op het wiegenlied.
Nynna aldrig tillbaka till vaggvisan.
Nigdy nie nuć w odpowiedzi na kołysankę.
Никогда не подпевай колыбельной.
Ninniye asla mırıldanarak karşılık verme.
لا تدندن أبدًا ردًا على التهويدة.
子守唄に鼻歌で応えてはいけない。
자장가에 절대 따라 흥얼거리지 마세요.
千万别对着摇篮曲哼回去。
"""
