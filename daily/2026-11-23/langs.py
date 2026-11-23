CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
माँ की सर्जरी अभी चल रही है। वो हमारी रसोई में चाय बना रही हैं
அம்மாவின் அறுவை சிகிச்சை முடியவில்லை. அவள் சமையலறையில் டீ போடுகிறாள்
అమ్మ సర్జరీ ఇంకా ముగియలేదు. ఆమె వంటగదిలో టీ చేస్తోంది
মায়ের অস্ত্রোপচার শেষ হয়নি। সে রান্নাঘরে চা বানাচ্ছে
आईची शस्त्रक्रिया अजून संपलेली नाही. ती स्वयंपाकघरात चहा बनवतेय
امی کا آپریشن ابھی جاری ہے۔ وہ باورچی خانے میں چائے بنا رہی ہیں
Hindi Pa Tapos ang Operasyon ni Mama. Nagtitimpla Siya ng Tsaa sa Kusina
Operasi Ibu Belum Selesai. Dia Membuat Teh di Dapur Kita
Pembedahan Ibu Belum Habis. Dia Buat Teh di Dapur Kita
မေမေ့ခွဲစိတ်မှု မပြီးသေးဘူး။ သူ မီးဖိုချောင်မှာ လက်ဖက်ရည်ဖျော်နေတယ်
ผ่าตัดแม่ยังไม่เสร็จ แต่แม่กำลังชงชาในครัวเรา
Ca Mổ của Mẹ Chưa Xong. Mẹ Đang Pha Trà Trong Bếp Nhà Mình
La Cirugía de Mamá No Ha Terminado. Está Haciendo Té en Nuestra Cocina
A Cirurgia da Mãe Não Acabou. Ela Está Fazendo Chá na Nossa Cozinha
L'Opération de Maman n'Est Pas Finie. Elle Fait du Thé dans Notre Cuisine
Mamas OP Ist Nicht Vorbei. Sie Kocht Tee in Unserer Küche
L'Operazione di Mamma Non È Finita. Sta Facendo il Tè in Cucina
Mama's Operatie Is Niet Voorbij. Ze Zet Thee in Onze Keuken
Mammas Operation Är Inte Slut. Hon Kokar Te i Vårt Kök
Operacja Mamy Jeszcze Trwa. Robi Herbatę w Naszej Kuchni
Операция у Мамы Ещё Идёт. Она Заваривает Чай у Нас на Кухне
Annemin Ameliyatı Bitmedi. Mutfağımızda Çay Demliyor
عملية أمي لم تنتهِ. وهي تعدّ الشاي في مطبخنا
母の手術はまだ終わっていない。でも台所でお茶を淹れている
엄마 수술은 아직 안 끝났다. 엄마가 우리 부엌에서 차를 끓인다
妈妈的手术还没结束。她却在我们厨房泡茶
"""
E1_H = """
माँ अभी सर्जरी में हैं, और रसोई की बत्ती जल गई।
அம்மா இன்னும் அறுவை சிகிச்சையில் இருக்கிறாள், சமையலறை விளக்கு எரிந்தது.
అమ్మ ఇంకా సర్జరీలో ఉంది, వంటగది లైట్ వెలిగింది.
মা এখনও অপারেশনে, আর রান্নাঘরের বাতি জ্বলে উঠল।
आई अजून शस्त्रक्रियेत आहे, आणि स्वयंपाकघरातला दिवा लागला.
امی ابھی آپریشن میں ہیں، اور باورچی خانے کی بتی جل اٹھی۔
Nasa operasyon pa si Mama, pero bumukas ang ilaw sa kusina.
Ibu masih dioperasi, tapi lampu dapur tiba-tiba menyala.
Ibu masih dibedah, tapi lampu dapur tiba-tiba menyala.
မေမေ ခွဲစိတ်နေဆဲပါ၊ ဒါပေမယ့် မီးဖိုချောင်မီး လင်းလာတယ်။
แม่ยังอยู่ในห้องผ่าตัด แต่ไฟในครัวเพิ่งเปิดขึ้น
Mẹ vẫn đang phẫu thuật, vậy mà đèn bếp vừa bật sáng.
Mamá sigue en cirugía, y la luz de la cocina se acaba de encender.
A mãe ainda está em cirurgia, e a luz da cozinha acabou de acender.
Maman est toujours au bloc, et la lumière de la cuisine vient de s'allumer.
Mama ist noch im OP, und das Küchenlicht ging gerade an.
Mamma è ancora in sala operatoria, e la luce della cucina si è accesa.
Mama ligt nog onder het mes, en het keukenlicht ging net aan.
Mamma är fortfarande på operation, och köksljuset tändes just.
Mama jest jeszcze na operacji, a w kuchni zapaliło się światło.
Мама всё ещё на операции, а на кухне только что зажёгся свет.
Annem hâlâ ameliyatta ve mutfağın ışığı az önce yandı.
أمي ما زالت في العملية، وضوء المطبخ أُضيء للتو.
母はまだ手術中なのに、台所の電気がついた。
엄마는 아직 수술 중인데, 부엌 불이 방금 켜졌다.
妈妈还在手术中，厨房的灯却亮了。
"""

E2_T = """
मिरर रूल भाग 1: बेटी का प्रतिबिंब हाथ हिलाया। वो सो रही थी
மிரர் ரூல் பாகம் 1: மகளின் பிம்பம் கை அசைத்தது. அவள் தூங்கிக்கொண்டிருந்தாள்
మిర్రర్ రూల్ పార్ట్ 1: కూతురి ప్రతిబింబం చేయి ఊపింది. ఆమె నిద్రలో ఉంది
মিরর রুল পর্ব ১: মেয়ের প্রতিবিম্ব হাত নাড়ল। সে ঘুমিয়ে ছিল
मिरर रूल भाग 1: मुलीच्या प्रतिबिंबाने हात हलवला. ती झोपली होती
مرر رول حصہ 1: بیٹی کے عکس نے ہاتھ ہلایا۔ وہ سو رہی تھی
Mirror Rule Pt 1: Kumaway ang Repleksyon ng Anak Ko. Tulog Siya
Aturan Cermin Bag 1: Bayangan Putriku Melambai. Dia Sedang Tidur
Peraturan Cermin Bhg 1: Bayang Anak Saya Melambai. Dia Sedang Tidur
မှန်စည်းမျဉ်း အပိုင်း ၁: သမီးရဲ့ အရိပ်က လက်ဝှေ့ယမ်းတယ်။ သူ အိပ်နေတာ
กฎกระจก ตอน 1: เงาของลูกสาวโบกมือ ทั้งที่เธอหลับอยู่
Luật Gương Phần 1: Bóng Con Gái Tôi Vẫy Tay. Con Đang Ngủ
Regla del Espejo Pt 1: El Reflejo de Mi Hija Saludó. Estaba Dormida
Regra do Espelho Pt 1: O Reflexo da Minha Filha Acenou. Ela Dormia
Règle du Miroir Pt 1: Le Reflet de Ma Fille a Fait Signe. Elle Dormait
Spiegelregel Teil 1: Das Spiegelbild Meiner Tochter Winkte. Sie Schlief
Regola dello Specchio Pt 1: Il Riflesso di Mia Figlia Ha Salutato. Dormiva
Spiegelregel Deel 1: Het Spiegelbeeld van Mijn Dochter Zwaaide. Ze Sliep
Spegelregeln Del 1: Min Dotters Spegelbild Vinkade. Hon Sov
Zasada Lustra Cz. 1: Odbicie Córki Pomachało. Spała
Правило зеркала, ч. 1: Отражение дочки помахало. Она спала
Ayna Kuralı Böl. 1: Kızımın Yansıması El Salladı. Uyuyordu
قاعدة المرآة ج1: انعكاس ابنتي لوّح بيده. كانت نائمة
鏡のルール Pt1: 娘の鏡像が手を振った。娘は眠っていた
거울 규칙 1부: 딸의 거울 속 모습이 손을 흔들었다. 딸은 자고 있었다
镜子规则 第1集：女儿的倒影挥了手。她明明睡着了
"""
E2_H = """
दादी का नियम था: रात को आईने में पलक मत झपकाना।
பாட்டியின் விதி: இரவில் கண்ணாடியைப் பார்த்து கண் சிமிட்டாதே.
బామ్మ నియమం: రాత్రి అద్దంలో కనురెప్ప వేయకు.
দিদার নিয়ম: রাতে আয়নার দিকে চোখ পিটপিট করো না।
आजीचा नियम: रात्री आरशात पाहून पापणी हलवू नकोस.
دادی کا اصول: رات کو آئینے کے سامنے پلک مت جھپکنا۔
Patakaran ni Lola: huwag kumurap pabalik sa salamin sa gabi.
Aturan nenek: jangan balas berkedip pada cermin di malam hari.
Peraturan nenek: jangan berkelip balas pada cermin waktu malam.
အဘွားရဲ့စည်းမျဉ်း: ညဘက် မှန်ကို မျက်စိပြန်မမှိတ်နဲ့။
กฎของยาย: ห้ามกะพริบตาตอบกระจกตอนกลางคืน
Quy tắc của bà: đêm đến đừng chớp mắt đáp lại gương.
La regla de la abuela: nunca parpadees de vuelta al espejo de noche.
A regra da vovó: nunca pisque de volta para o espelho à noite.
La règle de grand-mère: ne cligne jamais des yeux en retour devant le miroir la nuit.
Omas Regel: Blinzle nachts niemals zum Spiegel zurück.
La regola della nonna: di notte non ricambiare mai l'ammiccamento allo specchio.
Oma's regel: knipper 's nachts nooit terug naar de spiegel.
Mormors regel: blinka aldrig tillbaka åt spegeln på natten.
Zasada babci: nigdy nie mrugaj do lustra w nocy.
Правило бабушки: никогда не моргай в ответ зеркалу ночью.
Büyükannemin kuralı: geceleri aynaya asla karşılık olarak göz kırpma.
قاعدة جدتي: لا ترمش أبدًا في وجه المرآة ليلًا.
祖母のルール：夜、鏡に瞬きを返してはいけない。
할머니의 규칙: 밤에 거울에게 눈을 깜빡여 답하지 마라.
奶奶的规矩：夜里千万别对着镜子眨眼回应。
"""

E3_T = """
मिरर रूल भाग 2: प्रतिबिंब बोला, मैं उसका ख्याल रख रहा हूँ
மிரர் ரூல் பாகம் 2: பிம்பம் சொன்னது: நான் அவளைப் பார்த்துக்கொள்கிறேன்
మిర్రర్ రూల్ పార్ట్ 2: ప్రతిబింబం అంది: నేను ఆమెను చూసుకుంటున్నాను
মিরর রুল পর্ব ২: প্রতিবিম্ব বলল, আমি ওকে দেখে রাখছি
मिरर रूल भाग 2: प्रतिबिंब म्हणाले, मी तिची काळजी घेतोय
مرر رول حصہ 2: عکس نے کہا، میں اس کا خیال رکھ رہا ہوں
Mirror Rule Pt 2: Sabi ng Repleksyon Ko, Ako ang Nag-aalaga sa Kanya
Aturan Cermin Bag 2: Bayanganku Berkata, Aku yang Menjaganya
Peraturan Cermin Bhg 2: Bayangan Saya Kata, Saya yang Jaga Dia
မှန်စည်းမျဉ်း အပိုင်း ၂: အရိပ်က ပြောတယ်၊ ကျွန်တော်သူ့ကို ပြုစုနေတယ်
กฎกระจก ตอน 2: เงาของฉันบอกว่า ฉันดูแลเธออยู่
Luật Gương Phần 2: Bóng Của Tôi Nói: Tôi Đang Chăm Sóc Con Bé
Regla del Espejo Pt 2: Mi Reflejo Dijo: Yo La Estoy Cuidando
Regra do Espelho Pt 2: Meu Reflexo Disse: Eu Estou Cuidando Dela
Règle du Miroir Pt 2: Mon Reflet a Dit: Je M'Occupe d'Elle
Spiegelregel Teil 2: Mein Spiegelbild Sagte: Ich Kümmere Mich um Sie
Regola dello Specchio Pt 2: Il Mio Riflesso Ha Detto: Mi Prendo Cura di Lei
Spiegelregel Deel 2: Mijn Spiegelbeeld Zei: Ik Zorg voor Haar
Spegelregeln Del 2: Min Spegelbild Sa: Jag Tar Hand om Henne
Zasada Lustra Cz. 2: Moje Odbicie Powiedziało: Ja się Nią Opiekuję
Правило зеркала, ч. 2: Моё отражение сказало: Я за ней присматриваю
Ayna Kuralı Böl. 2: Yansımam Dedi ki: Ona Ben Bakıyorum
قاعدة المرآة ج2: قال انعكاسي: أنا من يعتني بها
鏡のルール Pt2: 鏡の私は言った。私が娘の面倒を見ている
거울 규칙 2부: 거울 속 내가 말했다. 내가 그 아이를 돌보고 있어
镜子规则 第2集：倒影说，我在照顾她
"""
E3_H = """
आईने से मैं बाहर आई, और मेरी बेटी की आँखें खुल गईं।
கண்ணாடியிலிருந்து நான் வெளியே வந்தேன், என் மகள் கண் விழித்தாள்.
అద్దంలోంచి నేను బయటకు వచ్చాను, నా కూతురు కళ్ళు తెరిచింది.
আয়না থেকে আমি বেরিয়ে এলাম, আর আমার মেয়ে চোখ খুলল।
आरशातून मी बाहेर आले, आणि माझ्या मुलीने डोळे उघडले.
آئینے سے میں باہر آئی، اور میری بیٹی نے آنکھیں کھول دیں۔
Lumabas ako sa salamin, at dumilat ang anak ko.
Aku keluar dari cermin, dan putriku membuka mata.
Saya keluar dari cermin, dan anak saya membuka mata.
မှန်ထဲက ကျွန်မထွက်လာပြီး သမီးမျက်လုံးဖွင့်လိုက်တယ်။
ฉันก้าวออกมาจากกระจก และลูกสาวก็ลืมตา
Tôi bước ra từ tấm gương, và con gái tôi mở mắt.
Salí del espejo, y mi hija abrió los ojos.
Saí do espelho, e minha filha abriu os olhos.
Je suis sortie du miroir, et ma fille a ouvert les yeux.
Ich trat aus dem Spiegel, und meine Tochter öffnete die Augen.
Sono uscita dallo specchio, e mia figlia ha aperto gli occhi.
Ik stapte uit de spiegel, en mijn dochter opende haar ogen.
Jag klev ut ur spegeln, och min dotter öppnade ögonen.
Wyszłam z lustra, a moja córka otworzyła oczy.
Я вышла из зеркала, и моя дочь открыла глаза.
Aynadan çıktım ve kızım gözlerini açtı.
خرجتُ من المرآة، وفتحت ابنتي عينيها.
私は鏡から出てきて、娘が目を開けた。
나는 거울에서 걸어 나왔고, 딸이 눈을 떴다.
我从镜子里走了出来，女儿睁开了眼睛。
"""
