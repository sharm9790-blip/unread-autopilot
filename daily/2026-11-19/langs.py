CODES = "hi ta te bn mr ur fil id ms my th vi es pt fr de it nl sv pl ru tr ar ja ko zh-CN".split()
def build(titles, hooks):
    t = [x.strip() for x in titles.strip().split("\n")]
    h = [x.strip() for x in hooks.strip().split("\n")]
    assert len(t) == len(CODES) == len(h), (len(t), len(h))
    return {c: {"title": a, "hook": b} for c, a, b in zip(CODES, t, h)}

E1_T = """
पापा आधी रात को पंखा ठीक कर रहे हैं। पापा नाइट शिफ्ट पर हैं
அப்பா நள்ளிரவில் மின்விசிறியை சரிசெய்கிறார். அப்பா இரவுப் பணியில் இருக்கிறார்
నాన్న అర్ధరాత్రి ఫ్యాన్ బాగు చేస్తున్నారు. నాన్న నైట్ షిఫ్ట్‌లో ఉన్నారు
বাবা মাঝরাতে ফ্যান ঠিক করছে। বাবা নাইট শিফটে আছে
बाबा मध्यरात्री पंखा दुरुस्त करत आहेत. बाबा नाईट शिफ्टवर आहेत
پاپا آدھی رات کو پنکھا ٹھیک کر رہے ہیں۔ پاپا نائٹ شفٹ پر ہیں
Inaayos ni Papa ang Bentilador Nang Hatinggabi. Nasa Night Shift Siya
Ayah Memperbaiki Kipas Tengah Malam. Ayah Sedang Shift Malam
Ayah Betulkan Kipas Tengah Malam. Ayah Sedang Syif Malam
ဖေဖေ သန်းခေါင်ယံမှာ ပန်ကာပြင်နေတယ်။ ဖေဖေက ညအလုပ်ဆင်းနေတယ်
พ่อกำลังซ่อมพัดลมตอนเที่ยงคืน แต่พ่อเข้ากะดึก
Bố Đang Sửa Quạt Lúc Nửa Đêm. Bố Đang Trực Đêm
Papá Arregla el Ventilador a Medianoche. Papá Está en Turno de Noche
O Papai Conserta o Ventilador à Meia-Noite. Ele Está no Turno da Noite
Papa Répare le Ventilateur à Minuit. Papa Est de Nuit au Travail
Papa Repariert um Mitternacht den Ventilator. Papa Hat Nachtschicht
Papà Ripara il Ventilatore a Mezzanotte. Papà È di Turno di Notte
Papa Repareert Middernacht de Ventilator. Papa Heeft Nachtdienst
Pappa Lagar Fläkten vid Midnatt. Pappa Har Nattskift
Tata Naprawia Wentylator o Północy. Tata Jest na Nocnej Zmianie
Папа Чинит Вентилятор в Полночь. Папа на Ночной Смене
Babam Gece Yarısı Vantilatörü Tamir Ediyor. Babam Gece Vardiyasında
أبي يصلح المروحة عند منتصف الليل. أبي في نوبة الليل
パパが真夜中に扇風機を直している。パパは夜勤中だ
아빠가 한밤중에 선풍기를 고치고 있다. 아빠는 야근 중이다
爸爸半夜在修风扇。爸爸正在上夜班
"""

E1_H = """
पापा आधी रात को पंखा ठीक कर रहे थे, पर वो नाइट शिफ्ट पर थे।
அப்பா நள்ளிரவில் மின்விசிறியை சரிசெய்தார், ஆனால் அவர் இரவுப் பணியில் இருந்தார்.
నాన్న అర్ధరాత్రి ఫ్యాన్ బాగు చేశారు, కానీ ఆయన నైట్ షిఫ్ట్‌లో ఉన్నారు.
বাবা মাঝরাতে ফ্যান ঠিক করছিল, অথচ সে নাইট শিফটে ছিল।
बाबा मध्यरात्री पंखा दुरुस्त करत होते, पण ते नाईट शिफ्टवर होते.
پاپا آدھی رات کو پنکھا ٹھیک کر رہے تھے، مگر وہ نائٹ شفٹ پر تھے۔
Inaayos ni Papa ang bentilador nang hatinggabi, pero nasa night shift siya.
Ayah memperbaiki kipas tengah malam, padahal dia sedang shift malam.
Ayah betulkan kipas tengah malam, padahal dia sedang syif malam.
ဖေဖေ သန်းခေါင်ယံမှာ ပန်ကာပြင်နေတယ်၊ ဒါပေမယ့် သူက ညအလုပ်ဆင်းနေတာ။
พ่อกำลังซ่อมพัดลมตอนเที่ยงคืน แต่พ่อเข้ากะดึกอยู่
Bố đang sửa quạt lúc nửa đêm, nhưng bố đang trực đêm.
Papá arreglaba el ventilador a medianoche, pero estaba en turno de noche.
O papai consertava o ventilador à meia-noite, mas estava no turno da noite.
Papa réparait le ventilateur à minuit, mais il était de nuit au travail.
Papa repariert um Mitternacht den Ventilator, dabei hat er Nachtschicht.
Papà riparava il ventilatore a mezzanotte, ma era di turno di notte.
Papa repareerde middernacht de ventilator, maar hij had nachtdienst.
Pappa lagade fläkten vid midnatt, men han hade nattskift.
Tata naprawiał wentylator o północy, a był na nocnej zmianie.
Папа чинил вентилятор в полночь, но он был на ночной смене.
Babam gece yarısı vantilatörü tamir ediyordu ama gece vardiyasındaydı.
كان أبي يصلح المروحة عند منتصف الليل، لكنه كان في نوبة الليل.
パパが真夜中に扇風機を直していたが、パパは夜勤中だった。
아빠가 한밤중에 선풍기를 고치고 있었지만, 아빠는 야근 중이었다.
爸爸半夜在修风扇，可他明明在上夜班。
"""

E2_T = """
वार्ड 9 · भाग 1: माँ कोमा में हैं। मेरी बात का कोई जवाब देता है
வார்டு 9 · பகுதி 1: அம்மா கோமாவில். நான் பேசினால் யாரோ பதில் சொல்கிறார்கள்
వార్డ్ 9 · పార్ట్ 1: అమ్మ కోమాలో ఉంది. నేను మాట్లాడితే ఎవరో బదులిస్తున్నారు
ওয়ার্ড ৯ · পর্ব ১: মা কোমায়। আমি কথা বললে কেউ উত্তর দেয়
वॉर्ड ९ · भाग १: आई कोमात आहे. मी बोलले की कोणीतरी उत्तर देतं
وارڈ 9 · حصہ 1: امی کومے میں ہیں۔ میری بات کا کوئی جواب دیتا ہے
Ward 9 · Pt 1: Na Coma si Mama. May Sumasagot Kapag Nagsasalita Ako
Ward 9 · Pt 1: Ibu Koma. Ada yang Menjawab Saat Aku Bicara
Wad 9 · Pt 1: Ibu Koma. Ada yang Menjawab Bila Saya Bercakap
ဝပ်ဒ် ၉ · အပိုင်း ၁: အမေ ကိုမာမှာ။ ကျွန်မပြောရင် တစ်ယောက်ယောက်ဖြေတယ်
วอร์ด 9 · ตอน 1: แม่อยู่ในอาการโคม่า ฉันพูดแล้วมีใครตอบ
Phòng 9 · Pt 1: Mẹ Hôn Mê. Có Ai Đó Đáp Lại Khi Con Nói
Sala 9 · Pt 1: Mamá Está en Coma. Alguien Responde Cuando Hablo
Ala 9 · Pt 1: Mamãe Está em Coma. Alguém Responde Quando Falo
Service 9 · Pt 1: Maman Est dans le Coma. Quelqu'un Répond Quand Je Parle
Station 9 · Pt 1: Mama Liegt im Koma. Jemand Antwortet, Wenn Ich Rede
Reparto 9 · Pt 1: Mamma È in Coma. Qualcuno Risponde Quando Parlo
Afdeling 9 · Pt 1: Mama Ligt in Coma. Iemand Antwoordt Als Ik Praat
Avdelning 9 · Pt 1: Mamma Ligger i Koma. Någon Svarar När Jag Pratar
Oddział 9 · Pt 1: Mama Jest w Śpiączce. Ktoś Odpowiada, Gdy Mówię
Палата 9 · Ч. 1: Мама в Коме. Кто-то Отвечает, Когда Я Говорю
Servis 9 · Pt 1: Annem Komada. Konuşunca Biri Cevap Veriyor
العنبر 9 · الجزء 1: أمي في غيبوبة. شخص ما يرد عندما أتكلم
9号病棟 Pt 1: 母は昏睡状態。話しかけると誰かが答える
9병동 · Pt 1: 엄마는 혼수상태. 말을 걸면 누군가 대답한다
9号病房 · Pt 1：妈妈昏迷了。我一说话就有人回答
"""

E2_H = """
माँ कोमा में हैं। मैंने गुड नाइट कहा तो खाली बेड से आवाज़ आई।
அம்மா கோமாவில் இருக்கிறார். குட் நைட் சொன்னதும் காலிப் படுக்கையிலிருந்து குரல் வந்தது.
అమ్మ కోమాలో ఉంది. గుడ్ నైట్ అంటే ఖాళీ బెడ్ నుంచి గొంతు వినిపించింది.
মা কোমায়। শুভরাত্রি বলতেই খালি বিছানা থেকে একটা কণ্ঠ উত্তর দিল।
आई कोमात आहे. शुभ रात्री म्हणताच रिकाम्या बेडवरून आवाज आला.
امی کومے میں ہیں۔ شب بخیر کہا تو خالی بیڈ سے آواز آئی۔
Na coma si Mama. Nang nag-goodnight ako, may boses na sumagot mula sa walang lamang kama.
Ibu koma. Saat aku bilang selamat malam, ada suara menjawab dari ranjang kosong.
Ibu koma. Bila saya ucap selamat malam, ada suara menjawab dari katil kosong.
အမေ ကိုမာမှာ။ ညအိပ်ကောင်းပါစေလို့ပြောတော့ ဗလာကုတင်ကနေ အသံတစ်ခု ပြန်ဖြေတယ်။
แม่อยู่ในอาการโคม่า พอฉันบอกราตรีสวัสดิ์ มีเสียงตอบจากเตียงว่าง
Mẹ đang hôn mê. Con chúc ngủ ngon thì có giọng đáp lại từ chiếc giường trống.
Mamá está en coma. Dije buenas noches y una voz respondió desde la cama vacía.
Mamãe está em coma. Disse boa noite e uma voz respondeu da cama vazia.
Maman est dans le coma. J'ai dit bonne nuit et une voix a répondu du lit vide.
Mama liegt im Koma. Ich sagte gute Nacht, und eine Stimme antwortete vom leeren Bett.
Mamma è in coma. Ho detto buonanotte e una voce ha risposto dal letto vuoto.
Mama ligt in coma. Ik zei welterusten en een stem antwoordde vanuit het lege bed.
Mamma ligger i koma. Jag sa godnatt och en röst svarade från den tomma sängen.
Mama jest w śpiączce. Powiedziałam dobranoc, a głos odpowiedział z pustego łóżka.
Мама в коме. Я сказала спокойной ночи, и голос ответил с пустой кровати.
Annem komada. İyi geceler dedim, boş yataktan bir ses cevap verdi.
أمي في غيبوبة. قلت تصبحين على خير فردّ صوت من السرير الفارغ.
母は昏睡状態。おやすみと言うと、空のベッドから声が返ってきた。
엄마는 혼수상태다. 잘 자라고 하자 빈 침대에서 목소리가 대답했다.
妈妈昏迷了。我说晚安，空床上传来了回答。
"""

E3_T = """
वार्ड 9 · भाग 2: माँ की आवाज़ ने गुड नाइट कहा। वो पहले ही जा चुकी थीं
வார்டு 9 · பகுதி 2: அம்மாவின் குரல் குட் நைட் சொன்னது. அவர் ஏற்கனவே போய்விட்டார்
వార్డ్ 9 · పార్ట్ 2: అమ్మ గొంతు గుడ్ నైట్ చెప్పింది. ఆమె అప్పటికే వెళ్లిపోయింది
ওয়ার্ড ৯ · পর্ব ২: মায়ের কণ্ঠ শুভরাত্রি বলল। মা আগেই চলে গিয়েছিল
वॉर्ड ९ · भाग २: आईच्या आवाजाने शुभ रात्री म्हटलं. ती आधीच गेली होती
وارڈ 9 · حصہ 2: امی کی آواز نے شب بخیر کہا۔ وہ پہلے ہی جا چکی تھیں
Ward 9 · Pt 2: Nag-goodnight ang Boses ni Mama. Wala Na Siya
Ward 9 · Pt 2: Suara Ibu Bilang Selamat Malam. Ibu Sudah Pergi
Wad 9 · Pt 2: Suara Ibu Ucap Selamat Malam. Ibu Sudah Pergi
ဝပ်ဒ် ၉ · အပိုင်း ၂: အမေ့အသံက ညအိပ်ကောင်းပါစေလို့ပြောတယ်။ သူက ထွက်သွားပြီးသား
วอร์ด 9 · ตอน 2: เสียงแม่บอกราตรีสวัสดิ์ แต่แม่จากไปแล้ว
Phòng 9 · Pt 2: Giọng Mẹ Nói Ngủ Ngon. Mẹ Đã Đi Từ Trước
Sala 9 · Pt 2: La Voz de Mamá Dijo Buenas Noches. Ya Se Había Ido
Ala 9 · Pt 2: A Voz da Mamãe Disse Boa Noite. Ela Já Tinha Partido
Service 9 · Pt 2: La Voix de Maman a Dit Bonne Nuit. Elle Était Déjà Partie
Station 9 · Pt 2: Mamas Stimme Sagte Gute Nacht. Sie War Längst Fort
Reparto 9 · Pt 2: La Voce di Mamma Ha Detto Buonanotte. Era Già Andata
Afdeling 9 · Pt 2: Mama's Stem Zei Welterusten. Ze Was Al Weg
Avdelning 9 · Pt 2: Mammas Röst Sa Godnatt. Hon Var Redan Borta
Oddział 9 · Pt 2: Głos Mamy Powiedział Dobranoc. Już Jej Nie Było
Палата 9 · Ч. 2: Голос Мамы Сказал Спокойной Ночи. Её Уже Не Было
Servis 9 · Pt 2: Annemin Sesi İyi Geceler Dedi. O Çoktan Gitmişti
العنبر 9 · الجزء 2: صوت أمي قال تصبحين على خير. كانت قد رحلت
9号病棟 Pt 2: 母の声がおやすみと言った。母はもういなかった
9병동 · Pt 2: 엄마의 목소리가 잘 자라고 했다. 엄마는 이미 떠났다
9号病房 · Pt 2：妈妈的声音说了晚安。她早已不在了
"""

E3_H = """
मैंने वार्ड 9 में गुड नाइट कहा। खाली बेड ने जवाब दिया, फिर माँ मुस्कुराते हुए उठ बैठीं।
நான் வார்டு 9ல் குட் நைட் சொன்னேன். காலிப் படுக்கை பதிலளித்தது, பிறகு அம்மா சிரித்தபடி எழுந்தார்.
నేను వార్డ్ 9లో గుడ్ నైట్ చెప్పాను. ఖాళీ బెడ్ బదులిచ్చింది, తర్వాత అమ్మ నవ్వుతూ లేచింది.
আমি ওয়ার্ড ৯-এ শুভরাত্রি বললাম। খালি বিছানা উত্তর দিল, তারপর মা হাসতে হাসতে উঠে বসল।
मी वॉर्ड ९ मध्ये शुभ रात्री म्हटलं. रिकाम्या बेडने उत्तर दिलं, मग आई हसत उठून बसली.
میں نے وارڈ 9 میں شب بخیر کہا۔ خالی بیڈ نے جواب دیا، پھر امی مسکراتے ہوئے اٹھ بیٹھیں۔
Nag-goodnight ako sa Ward 9. Sumagot ang walang laman na kama, tapos bumangon si Mama na nakangiti.
Aku bilang selamat malam di Ward 9. Ranjang kosong menjawab, lalu Ibu duduk sambil tersenyum.
Saya ucap selamat malam di Wad 9. Katil kosong menjawab, lalu Ibu duduk sambil tersenyum.
ဝပ်ဒ် ၉ မှာ ညအိပ်ကောင်းပါစေလို့ပြောခဲ့တယ်။ ဗလာကုတင်က ပြန်ဖြေပြီး အမေက ပြုံးရင်း ထထိုင်တယ်။
ฉันบอกราตรีสวัสดิ์ในวอร์ด 9 เตียงว่างตอบกลับ แล้วแม่ก็ลุกขึ้นนั่งยิ้ม
Con chúc ngủ ngon ở Phòng 9. Giường trống đáp lại, rồi mẹ ngồi dậy mỉm cười.
Dije buenas noches en la Sala 9. La cama vacía respondió y mamá se sentó sonriendo.
Disse boa noite na Ala 9. A cama vazia respondeu e a mamãe sentou sorrindo.
J'ai dit bonne nuit au Service 9. Le lit vide a répondu, puis Maman s'est assise en souriant.
Ich sagte auf Station 9 gute Nacht. Das leere Bett antwortete, dann setzte Mama sich lächelnd auf.
Ho detto buonanotte nel Reparto 9. Il letto vuoto ha risposto, poi Mamma si è seduta sorridendo.
Ik zei welterusten op Afdeling 9. Het lege bed antwoordde, en Mama ging glimlachend zitten.
Jag sa godnatt på Avdelning 9. Den tomma sängen svarade, sedan satte sig Mamma upp och log.
Powiedziałam dobranoc na Oddziale 9. Puste łóżko odpowiedziało, a mama usiadła z uśmiechem.
Я сказала спокойной ночи в Палате 9. Пустая кровать ответила, и мама села, улыбаясь.
Servis 9'da iyi geceler dedim. Boş yatak cevap verdi, sonra annem gülümseyerek oturdu.
قلت تصبحين على خير في العنبر 9. ردّ السرير الفارغ، ثم جلست أمي مبتسمة.
9号病棟でおやすみと言うと、空のベッドが答え、母が笑顔で起き上がった。
9병동에서 잘 자라고 하자 빈 침대가 대답했고, 엄마가 웃으며 일어나 앉았다.
我在9号病房说了晚安。空床回答了我，然后妈妈笑着坐了起来。
"""
