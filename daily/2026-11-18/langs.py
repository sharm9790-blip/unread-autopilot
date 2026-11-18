CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
भाई सेना से घर आया। वो अभी भी बॉर्डर पर है
அண்ணன் ராணுவத்திலிருந்து வந்தான். அவன் இன்னும் எல்லையில் இருக்கிறான்
అన్న ఆర్మీ నుంచి ఇంటికి వచ్చాడు. అతను ఇంకా బోర్డర్‌లోనే ఉన్నాడు
ভাই সেনা থেকে বাড়ি এলো। সে এখনও সীমান্তে
भाऊ सैन्यातून घरी आला. तो अजूनही सीमेवर आहे
بھائی فوج سے گھر آیا۔ وہ ابھی بھی سرحد پر ہے
Umuwi ang Kuya Galing Army. Nasa Border Pa Rin Siya
Kakakku Pulang dari Militer. Dia Masih di Perbatasan
Abang Pulang dari Tentera. Dia Masih di Sempadan
အစ်ကို စစ်တပ်က အိမ်ပြန်လာတယ်။ သူက နယ်စပ်မှာ ရှိနေဆဲ
พี่ชายกลับจากกองทัพ แต่เขายังอยู่ที่ชายแดน
Anh Trai Về Nhà Từ Quân Đội. Anh Vẫn Ở Biên Giới
Mi Hermano Volvió del Ejército. Sigue en la Frontera
Meu Irmão Voltou do Exército. Ele Ainda Está na Fronteira
Mon Frère Est Rentré de l'Armée. Il Est Toujours à la Frontière
Mein Bruder Kam von der Armee Heim. Er Ist Noch an der Grenze
Mio Fratello È Tornato dall'Esercito. È Ancora al Confine
Mijn Broer Kwam Thuis van het Leger. Hij Is Nog aan de Grens
Min Bror Kom Hem från Armén. Han Är Kvar vid Gränsen
Brat Wrócił z Wojska. Wciąż Jest na Granicy
Брат Вернулся из Армии. Он Всё Ещё на Границе
Abim Askerden Geldi. O Hâlâ Sınırda
عاد أخي من الجيش. لكنه ما زال على الحدود
兄が軍から帰ってきた。彼はまだ国境にいる
오빠가 군대에서 돌아왔다. 그는 아직 국경에 있다
哥哥从部队回家了。他还在边境
"""

E1_H = """
भाई आज रात सेना से घर आया, पर उसका कप्तान कहता है वो बॉर्डर पर है।
அண்ணன் இன்றிரவு ராணுவத்திலிருந்து வந்தான், ஆனால் அவன் எல்லையில் இருப்பதாக கேப்டன் சொல்கிறார்.
అన్న ఈ రాత్రి ఆర్మీ నుంచి వచ్చాడు, కానీ అతను బోర్డర్‌లో ఉన్నాడని కెప్టెన్ అంటున్నాడు.
ভাই আজ রাতে সেনা থেকে এলো, কিন্তু ক্যাপ্টেন বলছেন সে সীমান্তে।
भाऊ आज रात्री सैन्यातून आला, पण कॅप्टन म्हणतो तो सीमेवर आहे.
بھائی آج رات فوج سے آیا، مگر کپتان کہتا ہے وہ سرحد پر ہے۔
Umuwi si Kuya ngayong gabi, pero sabi ng kapitan nasa border pa siya.
Kakakku pulang malam ini, tapi kaptennya bilang dia masih di perbatasan.
Abang saya pulang malam ini, tapi kapten kata dia masih di sempadan.
အစ်ကို ဒီညအိမ်ပြန်လာတယ်၊ ဒါပေမဲ့ ဗိုလ်မှူးက သူ နယ်စပ်မှာရှိတယ်လို့ ပြောတယ်။
คืนนี้พี่ชายกลับบ้าน แต่กัปตันบอกว่าเขายังอยู่ที่ชายแดน
Tối nay anh trai về nhà, nhưng đại úy nói anh vẫn ở biên giới.
Mi hermano llegó esta noche, pero su capitán dice que sigue en la frontera.
Meu irmão chegou hoje à noite, mas o capitão diz que ele está na fronteira.
Mon frère est rentré ce soir, mais son capitaine dit qu'il est à la frontière.
Mein Bruder kam heute Nacht heim, doch sein Hauptmann sagt, er sei an der Grenze.
Mio fratello è tornato stanotte, ma il capitano dice che è al confine.
Mijn broer kwam vanavond thuis, maar zijn kapitein zegt dat hij aan de grens is.
Min bror kom hem i natt, men hans kapten säger att han är vid gränsen.
Brat wrócił dziś w nocy, ale jego kapitan mówi, że jest na granicy.
Брат вернулся сегодня ночью, но его капитан говорит, что он на границе.
Abim bu gece geldi ama komutanı hâlâ sınırda olduğunu söylüyor.
عاد أخي الليلة، لكن قائده يقول إنه ما زال على الحدود.
今夜兄が帰ってきたが、隊長は彼がまだ国境にいると言う。
오늘 밤 오빠가 돌아왔는데, 대위는 그가 아직 국경에 있다고 한다.
今晚哥哥回家了,可队长说他还在边境。
"""

E2_T = """
Pt 1: कोई मेरे बच्चे का हाथ थामता है। पति सो रहे हैं
Pt 1: யாரோ என் குழந்தையின் கையைப் பிடிக்கிறார்கள். கணவர் தூங்குகிறார்
Pt 1: ఎవరో నా బిడ్డ చేయి పట్టుకుంటున్నారు. భర్త నిద్రపోతున్నాడు
Pt 1: কেউ আমার বাচ্চার হাত ধরে। স্বামী ঘুমিয়ে আছে
Pt 1: कोणीतरी माझ्या बाळाचा हात धरतं. नवरा झोपलाय
Pt 1: کوئی میرے بچے کا ہاتھ تھامتا ہے۔ شوہر سو رہے ہیں
Pt 1: May Humahawak sa Kamay ng Baby Ko. Tulog ang Asawa Ko
Pt 1: Ada yang Memegang Tangan Bayiku. Suamiku Tertidur
Pt 1: Ada yang Pegang Tangan Bayi Saya. Suami Saya Tidur
Pt 1: တစ်ယောက်က ကျွန်မကလေးလက်ကို ကိုင်တယ်။ ခင်ပွန်း အိပ်နေတယ်
Pt 1: มีคนจับมือลูกฉัน สามีฉันหลับอยู่
Pt 1: Ai Đó Nắm Tay Con Tôi. Chồng Tôi Đang Ngủ
Pt 1: Alguien Sostiene la Mano de Mi Bebé. Mi Marido Duerme
Pt 1: Alguém Segura a Mão do Meu Bebê. Meu Marido Dorme
Pt 1: Quelqu'un Tient la Main de Mon Bébé. Mon Mari Dort
Pt 1: Jemand Hält die Hand Meines Babys. Mein Mann Schläft
Pt 1: Qualcuno Tiene la Mano del Mio Bimbo. Mio Marito Dorme
Pt 1: Iemand Houdt de Hand van Mijn Baby Vast. Mijn Man Slaapt
Pt 1: Någon Håller Min Bebis Hand. Min Man Sover
Pt 1: Ktoś Trzyma Rączkę Mojego Dziecka. Mąż Śpi
Pt 1: Кто-то Держит Руку Моего Малыша. Муж Спит
Pt 1: Biri Bebeğimin Elini Tutuyor. Eşim Uyuyor
Pt 1: شخص ما يمسك يد طفلي. زوجي نائم
Pt 1: 誰かが赤ちゃんの手を握る。夫は眠っている
Pt 1: 누군가 아기 손을 잡는다. 남편은 자고 있다
Pt 1: 有人握着我宝宝的手。丈夫睡着了
"""

E2_H = """
हर रात कोई पालने की सलाखों से मेरे बच्चे का हाथ थामता है।
ஒவ்வொரு இரவும் யாரோ தொட்டில் கம்பிகள் வழியாக என் குழந்தையின் கையைப் பிடிக்கிறார்கள்.
ప్రతి రాత్రి ఎవరో ఊయల ఊచల నుంచి నా బిడ్డ చేయి పట్టుకుంటారు.
প্রতি রাতে কেউ দোলনার শিকের ফাঁক দিয়ে আমার বাচ্চার হাত ধরে।
दररोज रात्री कोणीतरी पाळण्याच्या गजांतून माझ्या बाळाचा हात धरतं.
ہر رات کوئی جھولے کی سلاخوں سے میرے بچے کا ہاتھ تھامتا ہے۔
Gabi-gabi may humahawak sa kamay ng baby ko mula sa crib.
Setiap malam ada yang memegang tangan bayiku lewat jeruji boksnya.
Setiap malam ada yang pegang tangan bayi saya melalui palang katil bayi.
ညတိုင်း တစ်ယောက်က ခြေတံရိုးကြားက ကျွန်မကလေးလက်ကို ကိုင်တယ်။
ทุกคืนมีคนจับมือลูกฉันผ่านซี่เปล
Mỗi đêm có ai đó nắm tay con tôi qua song cũi.
Cada noche alguien sostiene la mano de mi bebé a través de los barrotes de la cuna.
Toda noite alguém segura a mão do meu bebê pelas grades do berço.
Chaque nuit, quelqu'un tient la main de mon bébé à travers les barreaux du lit.
Jede Nacht hält jemand die Hand meines Babys durch die Gitterstäbe.
Ogni notte qualcuno tiene la mano del mio bambino tra le sbarre della culla.
Elke nacht houdt iemand de hand van mijn baby vast door de spijlen.
Varje natt håller någon min bebis hand genom spjälorna.
Co noc ktoś trzyma rączkę mojego dziecka przez szczebelki łóżeczka.
Каждую ночь кто-то держит руку моего малыша сквозь прутья кроватки.
Her gece biri bebeğimin elini beşik parmaklıklarından tutuyor.
كل ليلة يمسك شخص ما يد طفلي من بين قضبان السرير.
毎晩、誰かがベビーベッドの柵越しに赤ちゃんの手を握る。
매일 밤 누군가 아기 침대 창살 사이로 아기 손을 잡는다.
每晚都有人透过婴儿床栏杆握住我宝宝的手。
"""

E3_T = """
Pt 2: पति को पता था। वो उसे बच्चे का हाथ देता है
Pt 2: கணவருக்குத் தெரியும். அவர் அதற்கு குழந்தையின் கையைக் கொடுக்கிறார்
Pt 2: భర్తకు తెలుసు. అతను దానికి బిడ్డ చేయి ఇస్తున్నాడు
Pt 2: স্বামী জানত। সে ওকে বাচ্চার হাত দেয়
Pt 2: नवऱ्याला माहीत होतं. तो त्याला बाळाचा हात देतो
Pt 2: شوہر کو پتا تھا۔ وہ اسے بچے کا ہاتھ دیتا ہے
Pt 2: Alam ng Asawa Ko. Ibinibigay Niya ang Kamay ng Baby
Pt 2: Suamiku Tahu. Dia Memberikan Tangan Bayi
Pt 2: Suami Saya Tahu. Dia Beri Tangan Bayi Kepadanya
Pt 2: ခင်ပွန်းသိတယ်။ သူက ကလေးလက်ကို ပေးနေတာ
Pt 2: สามีรู้ เขายื่นมือลูกให้มัน
Pt 2: Chồng Tôi Biết. Anh Ấy Đưa Tay Con Cho Nó
Pt 2: Mi Marido Lo Sabía. Le Da la Mano de la Bebé
Pt 2: Meu Marido Sabia. Ele Dá a Mão da Bebê a Ela
Pt 2: Mon Mari Savait. Il Lui Donne la Main du Bébé
Pt 2: Mein Mann Wusste Es. Er Gibt Ihm die Babyhand
Pt 2: Mio Marito Sapeva. Gli Dà la Manina della Bimba
Pt 2: Mijn Man Wist het. Hij Geeft Het Haar Handje
Pt 2: Min Man Visste. Han Ger Den Hennes Hand
Pt 2: Mąż Wiedział. Daje Temu Rączkę Dziecka
Pt 2: Муж Знал. Он Отдаёт Ему Руку Малышки
Pt 2: Eşim Biliyordu. Ona Bebeğin Elini Veriyor
Pt 2: زوجي كان يعرف. إنه يعطيه يد الطفلة
Pt 2: 夫は知っていた。赤ちゃんの手を差し出していた
Pt 2: 남편은 알고 있었다. 아기 손을 내어주고 있었다
Pt 2: 丈夫早就知道。他把宝宝的手递给了它
"""

E3_H = """
पालने के नीचे से किसी ने बच्चे का हाथ खींचा और पति बोला: उसे पकड़ने दो।
தொட்டிலுக்கு அடியில் ஏதோ குழந்தையின் கையை இழுத்தது, கணவர் சொன்னார்: விடு.
ఊయల కింద ఏదో బిడ్డ చేయి లాగింది, భర్త అన్నాడు: పట్టుకోనివ్వు.
দোলনার নিচে কিছু বাচ্চার হাত টানল, স্বামী বলল: ধরতে দাও।
पाळण्याखाली काहीतरी बाळाचा हात ओढतं आणि नवरा म्हणाला: धरू दे.
جھولے کے نیچے کسی نے بچے کا ہاتھ کھینچا اور شوہر بولا: پکڑنے دو۔
May humila sa kamay ng baby mula sa ilalim ng crib, sabi ng asawa ko: hayaan mo.
Sesuatu di bawah boks menarik tangan bayiku dan suamiku bilang: biarkan.
Sesuatu di bawah katil bayi tarik tangan bayi dan suami saya kata: biarkan.
ခြေတံရိုးအောက်က တစ်ခုက ကလေးလက်ကို ဆွဲတယ်၊ ခင်ပွန်းက ပြောတယ်- ကိုင်ခွင့်ပေးလိုက်။
มีบางอย่างใต้เปลดึงมือลูก สามีบอกว่า ปล่อยให้มันจับ
Có thứ dưới cũi kéo tay con, và chồng tôi nói: cứ để nó nắm.
Algo bajo la cuna tiró de la mano de mi bebé y mi marido dijo: déjalo.
Algo sob o berço puxou a mão do bebê e meu marido disse: deixa.
Quelque chose sous le lit a tiré la main du bébé, et mon mari a dit : laisse-le.
Etwas unter dem Bett zog an der Babyhand, und mein Mann sagte: lass es.
Qualcosa sotto la culla ha tirato la mano della bimba e mio marito ha detto: lascia.
Iets onder het bedje trok aan de hand van mijn baby en mijn man zei: laat maar.
Något under spjälsängen drog i bebisens hand och min man sa: låt den.
Coś pod łóżeczkiem pociągnęło rączkę dziecka, a mąż powiedział: pozwól mu.
Что-то под кроваткой потянуло руку малыша, а муж сказал: пусть держит.
Beşiğin altındaki bir şey bebeğin elini çekti, eşim dedi ki: bırak tutsun.
شيء تحت السرير شدّ يد الطفلة وقال زوجي: دعيه.
ベビーベッドの下の何かが赤ちゃんの手を引き、夫は言った。握らせておけ。
침대 아래의 무언가가 아기 손을 당기자 남편이 말했다. 잡게 둬.
婴儿床下有东西拉住宝宝的手,丈夫说:让它握着。
"""

