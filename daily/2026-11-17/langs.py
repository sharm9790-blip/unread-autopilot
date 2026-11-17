CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
बेटी स्कूल गेट पर इंतज़ार कर रही थी। वो घर पर बीमार थी
மகள் பள்ளி வாசலில் காத்திருந்தாள். அவள் வீட்டில் நோயுற்றிருந்தாள்
కూతురు స్కూల్ గేట్ దగ్గర ఎదురుచూసింది. ఆమె ఇంట్లో అనారోగ్యంగా ఉంది
মেয়ে স্কুলের গেটে অপেক্ষা করছিল। সে বাড়িতে অসুস্থ ছিল
मुलगी शाळेच्या गेटवर वाट पाहत होती. ती घरी आजारी होती
بیٹی اسکول کے گیٹ پر انتظار کر رہی تھی۔ وہ گھر پر بیمار تھی
Naghihintay ang Anak Ko sa Gate ng Eskwela. May Sakit Siya sa Bahay
Putriku Menunggu di Gerbang Sekolah. Dia Sakit di Rumah
Anak Saya Menunggu di Pintu Pagar Sekolah. Dia Sakit di Rumah
သမီး ကျောင်းတံခါးမှာ စောင့်နေတယ်။ သူက အိမ်မှာ နေမကောင်းဘူး
ลูกสาวรออยู่หน้าประตูโรงเรียน แต่เธอป่วยอยู่ที่บ้าน
Con Gái Đợi Ở Cổng Trường. Con Đang Ốm Ở Nhà
Mi Hija Me Esperaba en la Puerta del Colegio. Estaba Enferma en Casa
Minha Filha Esperava no Portão da Escola. Estava Doente em Casa
Ma Fille M'Attendait à l'École. Elle Était Malade à la Maison
Meine Tochter Wartete am Schultor. Sie War Krank zu Hause
Mia Figlia Aspettava al Cancello della Scuola. Era Malata a Casa
Mijn Dochter Wachtte bij het Schoolhek. Ze Was Thuis Ziek
Min Dotter Väntade vid Skolporten. Hon Var Sjuk Hemma
Córka Czekała przy Bramie Szkoły. Była Chora w Domu
Дочь Ждала у Школьных Ворот. Она Болела Дома
Kızım Okul Kapısında Bekliyordu. Evde Hastaydı
ابنتي كانت تنتظر عند بوابة المدرسة. وكانت مريضة في البيت
娘が校門で待っていた。娘は家で寝込んでいた
딸이 교문 앞에서 기다렸다. 딸은 집에서 아팠다
女儿在校门口等我。她明明在家生病
"""
E1_H = """
बीमार बेटी स्कूल के गेट पर मेरा इंतज़ार कर रही थी।
நோயுற்ற என் மகள் பள்ளி வாசலில் எனக்காகக் காத்திருந்தாள்.
అనారోగ్యంగా ఉన్న నా కూతురు స్కూల్ గేట్ దగ్గర నా కోసం ఎదురుచూస్తోంది.
আমার অসুস্থ মেয়ে স্কুলের গেটে আমার জন্য অপেক্ষা করছিল।
माझी आजारी मुलगी शाळेच्या गेटवर माझी वाट पाहत होती.
میری بیمار بیٹی اسکول کے گیٹ پر میرا انتظار کر رہی تھی۔
Naghihintay sa akin ang may sakit kong anak sa gate ng eskwela.
Putriku yang sedang sakit menungguku di gerbang sekolah.
Anak saya yang sakit sedang menunggu saya di pintu pagar sekolah.
နေမကောင်းတဲ့ ကျွန်တော့်သမီး ကျောင်းတံခါးမှာ စောင့်နေတယ်။
ลูกสาวที่ป่วยของฉันรออยู่หน้าประตูโรงเรียน
Đứa con gái đang ốm của tôi đứng đợi ở cổng trường.
Mi hija enferma me esperaba en la puerta del colegio.
Minha filha doente me esperava no portão da escola.
Ma fille malade m'attendait devant le portail de l'école.
Meine kranke Tochter wartete am Schultor auf mich.
Mia figlia malata mi aspettava davanti al cancello della scuola.
Mijn zieke dochter stond me op te wachten bij het schoolhek.
Min sjuka dotter väntade på mig vid skolporten.
Moja chora córka czekała na mnie przy bramie szkoły.
Моя больная дочь ждала меня у школьных ворот.
Hasta olan kızım okul kapısında beni bekliyordu.
كانت ابنتي المريضة تنتظرني عند بوابة المدرسة.
病気のはずの娘が、校門で私を待っていた。
아픈 내 딸이 교문 앞에서 나를 기다리고 있었다.
生病的女儿正在校门口等我。
"""
E2_T = """
रॉकिंग चेयर · भाग 1: दादाजी की कुर्सी हिलती है। वो अस्पताल में हैं
ராக்கிங் நாற்காலி · பகுதி 1: தாத்தாவின் நாற்காலி ஆடுகிறது. அவர் மருத்துவமனையில்
రాకింగ్ చైర్ · పార్ట్ 1: తాతయ్య కుర్చీ ఊగుతోంది. ఆయన ఆసుపత్రిలో ఉన్నారు
রকিং চেয়ার · পর্ব ১: দাদুর চেয়ার দোলে। দাদু হাসপাতালে
रॉकिंग चेअर · भाग 1: आजोबांची खुर्ची हलते. ते हॉस्पिटलमध्ये आहेत
راکنگ چیئر · حصہ 1: دادا کی کرسی ہلتی ہے۔ وہ ہسپتال میں ہیں
Rocking Chair · Pt 1: Gumagalaw ang Upuan ni Lolo. Nasa Ospital Siya
Kursi Goyang · Pt 1: Kursi Kakek Bergoyang. Kakek Ada di Rumah Sakit
Kerusi Goyang · Pt 1: Kerusi Atuk Bergoyang. Atuk di Hospital
ချာချာလှည့်ကုလားထိုင် · အပိုင်း ၁: အဖိုး့ကုလားထိုင် လှုပ်နေတယ်။ သူက ဆေးရုံမှာ
เก้าอี้โยก · ตอนที่ 1: เก้าอี้ของตาโยกเอง แต่ตาอยู่โรงพยาบาล
Ghế Bập Bênh · Tập 1: Ghế Của Ông Tự Đung Đưa. Ông Nằm Viện
La Mecedora · Pt 1: La Silla del Abuelo Se Mece. Él Está en el Hospital
A Cadeira de Balanço · Pt 1: A Cadeira do Avô Balança. Ele Está no Hospital
Le Fauteuil à Bascule · Pt 1: Celui de Papi Bouge. Il Est à l'Hôpital
Der Schaukelstuhl · Pt 1: Opas Stuhl Schaukelt. Er Liegt im Krankenhaus
La Sedia a Dondolo · Pt 1: Quella del Nonno Dondola. Lui È in Ospedale
De Schommelstoel · Pt 1: Opa's Stoel Schommelt. Hij Ligt in het Ziekenhuis
Gungstolen · Pt 1: Morfars Stol Gungar. Han Ligger på Sjukhus
Fotel Bujany · Cz. 1: Fotel Dziadka Się Buja. Dziadek Jest w Szpitalu
Кресло-Качалка · Ч. 1: Дедушкино Кресло Качается. Он в Больнице
Sallanan Sandalye · Böl. 1: Dedemin Sandalyesi Sallanıyor. Hastanede
الكرسي الهزاز · ج1: كرسي جدي يهتز. وجدي في المستشفى
ロッキングチェア · Pt1: 祖父の椅子が揺れる。祖父は入院中
흔들의자 · 1부: 할아버지 의자가 흔들린다. 할아버지는 병원에
摇椅 · 第1集: 爷爷的椅子在摇。爷爷还在住院
"""
E2_H = """
दादाजी की कुर्सी रात 3 बजे हिलती है, जबकि दादाजी अस्पताल में हैं।
தாத்தாவின் நாற்காலி அதிகாலை 3 மணிக்கு ஆடுகிறது, தாத்தாவோ மருத்துவமனையில்.
తాతయ్య కుర్చీ రాత్రి 3 గంటలకు ఊగుతుంది, తాతయ్య ఆసుపత్రిలో ఉన్నారు.
দাদুর চেয়ার রাত ৩টায় দোলে, অথচ দাদু হাসপাতালে।
आजोबांची खुर्ची रात्री 3 वाजता हलते, आणि आजोबा हॉस्पिटलमध्ये आहेत.
دادا کی کرسی رات 3 بجے ہلتی ہے، جبکہ دادا ہسپتال میں ہیں۔
Gumagalaw ang upuan ni Lolo ng 3 AM, pero nasa ospital si Lolo.
Kursi Kakek bergoyang jam 3 pagi, padahal Kakek ada di rumah sakit.
Kerusi Atuk bergoyang pada pukul 3 pagi, sedangkan Atuk di hospital.
အဖိုးက ဆေးရုံမှာဖြစ်ပြီး ညသုံးနာရီမှာ သူ့ကုလားထိုင် လှုပ်နေတယ်။
เก้าอี้ของตาโยกตอนตีสาม ทั้งที่ตาอยู่โรงพยาบาล
Ghế của ông tự đung đưa lúc 3 giờ sáng, trong khi ông đang nằm viện.
La silla del abuelo se mece a las 3 AM, pero el abuelo está en el hospital.
A cadeira do vovô balança às 3 da manhã, mas ele está no hospital.
Le fauteuil de papi bouge à 3 h du matin, alors qu'il est à l'hôpital.
Opas Stuhl schaukelt um 3 Uhr nachts, obwohl Opa im Krankenhaus liegt.
La sedia del nonno dondola alle 3 di notte, ma il nonno è in ospedale.
Opa's stoel schommelt om 3 uur 's nachts, terwijl Opa in het ziekenhuis ligt.
Morfars stol gungar klockan 3 på natten, fast han ligger på sjukhus.
Fotel dziadka buja się o 3 w nocy, a dziadek leży w szpitalu.
Дедушкино кресло качается в 3 часа ночи, а дедушка в больнице.
Dedemin sandalyesi gece 3'te sallanıyor, oysa dedem hastanede.
كرسي جدي يهتز في الثالثة فجرًا بينما جدي في المستشفى.
祖父の椅子が午前3時に揺れる。祖父は入院しているのに。
할아버지 의자가 새벽 3시에 흔들린다. 할아버지는 병원에 계신데.
爷爷的椅子凌晨3点自己摇起来，可爷爷还在住院。
"""
E3_T = """
रॉकिंग चेयर · भाग 2: दादाजी घर आए। अस्पताल बोला, वो 3 बजे गुज़र गए
ராக்கிங் நாற்காலி · பகுதி 2: தாத்தா வீடு வந்தார். அவர் 3 மணிக்கே இறந்துவிட்டார்
రాకింగ్ చైర్ · పార్ట్ 2: తాతయ్య ఇంటికొచ్చారు. 3 గంటలకే చనిపోయారని ఆసుపత్రి చెప్పింది
রকিং চেয়ার · পর্ব ২: দাদু বাড়ি এলেন। হাসপাতাল বলল, তিনটায় মারা গেছেন
रॉकिंग चेअर · भाग 2: आजोबा घरी आले. हॉस्पिटल म्हणालं, ते 3 वाजता गेले
راکنگ چیئر · حصہ 2: دادا گھر آئے۔ ہسپتال نے کہا وہ 3 بجے چل بسے
Rocking Chair · Pt 2: Umuwi si Lolo. Sabi ng Ospital, Pumanaw Siya ng 3
Kursi Goyang · Pt 2: Kakek Pulang. Rumah Sakit Bilang Dia Wafat Jam 3
Kerusi Goyang · Pt 2: Atuk Pulang. Hospital Kata Dia Meninggal Pukul 3
ချာချာလှည့်ကုလားထိုင် · အပိုင်း ၂: အဖိုးအိမ်ပြန်လာတယ်။ ဆေးရုံက သူ ၃ နာရီမှာ ဆုံးပြီတဲ့
เก้าอี้โยก · ตอนที่ 2: ตากลับบ้านมา แต่โรงพยาบาลบอกว่าตาเสียตอนตีสาม
Ghế Bập Bênh · Tập 2: Ông Về Nhà. Bệnh Viện Báo Ông Mất Lúc 3 Giờ
La Mecedora · Pt 2: El Abuelo Volvió a Casa. Murió a las 3 AM
A Cadeira de Balanço · Pt 2: O Avô Voltou. Morreu às 3 da Manhã
Le Fauteuil à Bascule · Pt 2: Papi Est Rentré. Il Est Mort à 3 h
Der Schaukelstuhl · Pt 2: Opa Kam Heim. Er Starb um 3 Uhr
La Sedia a Dondolo · Pt 2: Il Nonno Tornò a Casa. Era Morto alle 3
De Schommelstoel · Pt 2: Opa Kwam Thuis. Hij Stierf om 3 Uur
Gungstolen · Pt 2: Morfar Kom Hem. Han Dog Klockan 3
Fotel Bujany · Cz. 2: Dziadek Wrócił. Zmarł o 3 w Nocy
Кресло-Качалка · Ч. 2: Дедушка Вернулся. Он Умер в 3 Часа Ночи
Sallanan Sandalye · Böl. 2: Dedem Eve Geldi. Saat 3'te Ölmüştü
الكرسي الهزاز · ج2: عاد جدي إلى البيت. مات في الثالثة فجرًا
ロッキングチェア · Pt2: 祖父が帰ってきた。祖父は3時に亡くなっていた
흔들의자 · 2부: 할아버지가 집에 오셨다. 3시에 돌아가셨다는데
摇椅 · 第2集: 爷爷回家了。医院说他3点就去世了
"""
E3_H = """
दादाजी घर आकर कुर्सी पर बैठे। अस्पताल ने कहा, वो 3 बजे गुज़र चुके थे।
தாத்தா வீடு வந்து நாற்காலியில் அமர்ந்தார். அவர் 3 மணிக்கே இறந்துவிட்டதாக மருத்துவமனை சொன்னது.
తాతయ్య ఇంటికొచ్చి కుర్చీలో కూర్చున్నారు. ఆయన 3 గంటలకే చనిపోయారని ఆసుపత్రి చెప్పింది.
দাদু বাড়ি এসে চেয়ারে বসলেন। হাসপাতাল বলল, তিনি তিনটায় মারা গেছেন।
आजोबा घरी येऊन खुर्चीवर बसले. हॉस्पिटल म्हणालं, ते 3 वाजताच गेले होते.
دادا گھر آ کر کرسی پر بیٹھ گئے۔ ہسپتال نے کہا وہ 3 بجے ہی چل بسے تھے۔
Umuwi si Lolo at umupo sa upuan. Sabi ng ospital, pumanaw na siya ng 3.
Kakek pulang dan duduk di kursi. Rumah sakit bilang dia sudah wafat jam 3.
Atuk pulang dan duduk di kerusi. Hospital kata dia sudah meninggal pukul 3.
အဖိုးအိမ်ပြန်လာပြီး ကုလားထိုင်မှာ ထိုင်တယ်။ ဆေးရုံက ၃ နာရီမှာပဲ ဆုံးပြီတဲ့။
ตากลับบ้านมานั่งเก้าอี้ แต่โรงพยาบาลบอกว่าตาเสียตั้งแต่ตีสาม
Ông về nhà và ngồi vào ghế. Bệnh viện nói ông đã mất lúc 3 giờ.
El abuelo volvió a casa y se sentó en la silla. El hospital dijo que murió a las 3.
O vovô voltou para casa e sentou na cadeira. O hospital disse que ele morreu às 3.
Papi est rentré et s'est assis dans le fauteuil. L'hôpital dit qu'il est mort à 3 h.
Opa kam nach Hause und setzte sich in den Stuhl. Das Krankenhaus sagte, er starb um 3.
Il nonno tornò a casa e si sedette sulla sedia. L'ospedale disse che era morto alle 3.
Opa kwam thuis en ging in de stoel zitten. Het ziekenhuis zei dat hij om 3 uur stierf.
Morfar kom hem och satte sig i stolen. Sjukhuset sa att han dog klockan 3.
Dziadek wrócił do domu i usiadł w fotelu. Szpital powiedział, że zmarł o 3.
Дедушка вернулся домой и сел в кресло. Больница сказала, что он умер в 3.
Dedem eve gelip sandalyeye oturdu. Hastane saat 3'te öldüğünü söyledi.
عاد جدي إلى البيت وجلس على الكرسي. قال المستشفى إنه مات في الثالثة.
祖父は帰宅して椅子に座った。病院は3時に亡くなったと言った。
할아버지가 집에 와서 의자에 앉았다. 병원은 3시에 돌아가셨다고 했다.
爷爷回家坐到了椅子上。医院却说他3点就去世了。
"""
