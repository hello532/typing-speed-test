/* ui.js — language switcher (5 langs incl. RTL Arabic) + 3 color themes.
   Translates UI chrome via [data-i18n]/[data-i18n-html]; provides native
   practice-text banks via window.TR.pool(lang). Persists in localStorage.
   Does not alter SEO article/FAQ (kept English for indexing). Zero deps. */
(function(){
"use strict";

var I18N={
 en:{_name:"English",time:"Time",text:"Text",m_sentences:"Sentences",m_quotes:"Quotes",m_numbers:"Numbers",m_words:"Words",
   st_time:"Time",wpm:"WPM",accuracy:"Accuracy",r_cpm:"Chars/min",r_errors:"Errors",r_raw:"Raw WPM",
   hint:'Click here or press <b>any key</b> to start typing',btn_again:"Test again",btn_share:"Copy result",btn_copied:"Copied!",
   hist_title:"Your typing history (saved in this browser)",h_date:"Date",h_test:"Test",
   hist_empty:"No results yet — finish a test and it will appear here."},
 zh:{_name:"中文",time:"时间",text:"文本",m_sentences:"句子",m_quotes:"名言",m_numbers:"数字",m_words:"单词",
   st_time:"时间",wpm:"字/分",accuracy:"准确率",r_cpm:"字符/分",r_errors:"错误",r_raw:"原始速度",
   hint:'点击此处或按<b>任意键</b>开始打字',btn_again:"再测一次",btn_share:"复制成绩",btn_copied:"已复制！",
   hist_title:"你的打字记录（保存在此浏览器）",h_date:"日期",h_test:"测试",
   hist_empty:"还没有记录 —— 完成一次测试后会显示在这里。"},
 es:{_name:"Español",time:"Tiempo",text:"Texto",m_sentences:"Frases",m_quotes:"Citas",m_numbers:"Números",m_words:"Palabras",
   st_time:"Tiempo",wpm:"PPM",accuracy:"Precisión",r_cpm:"Caract./min",r_errors:"Errores",r_raw:"PPM bruto",
   hint:'Haz clic aquí o pulsa <b>cualquier tecla</b> para empezar',btn_again:"Repetir",btn_share:"Copiar resultado",btn_copied:"¡Copiado!",
   hist_title:"Tu historial de mecanografía (guardado en este navegador)",h_date:"Fecha",h_test:"Prueba",
   hist_empty:"Aún no hay resultados: completa una prueba y aparecerá aquí."},
 hi:{_name:"हिन्दी",time:"समय",text:"पाठ",m_sentences:"वाक्य",m_quotes:"उद्धरण",m_numbers:"संख्याएँ",m_words:"शब्द",
   st_time:"समय",wpm:"WPM",accuracy:"सटीकता",r_cpm:"वर्ण/मिनट",r_errors:"त्रुटियाँ",r_raw:"रॉ WPM",
   hint:'यहाँ क्लिक करें या <b>कोई भी कुंजी</b> दबाकर टाइप करना शुरू करें',btn_again:"फिर से टेस्ट करें",btn_share:"परिणाम कॉपी करें",btn_copied:"कॉपी हो गया!",
   hist_title:"आपका टाइपिंग इतिहास (इस ब्राउज़र में सहेजा गया)",h_date:"तारीख",h_test:"टेस्ट",
   hist_empty:"अभी तक कोई परिणाम नहीं — एक टेस्ट पूरा करें और यह यहाँ दिखेगा।"},
 ar:{_name:"العربية",time:"الوقت",text:"النص",m_sentences:"جُمل",m_quotes:"اقتباسات",m_numbers:"أرقام",m_words:"كلمات",
   st_time:"الوقت",wpm:"ك/د",accuracy:"الدقة",r_cpm:"حرف/دقيقة",r_errors:"الأخطاء",r_raw:"السرعة الخام",
   hint:'انقر هنا أو اضغط <b>أي مفتاح</b> لبدء الكتابة',btn_again:"إعادة الاختبار",btn_share:"نسخ النتيجة",btn_copied:"تم النسخ!",
   hist_title:"سجل الكتابة الخاص بك (محفوظ في هذا المتصفح)",h_date:"التاريخ",h_test:"الاختبار",
   hist_empty:"لا توجد نتائج بعد — أكمل اختبارًا وسيظهر هنا."}
};

var POOL=/*{{POOL}}*/;

(function(){
/* Round-4 UI 多语化：ja/ko/ur 补全 + id/vi/tr/th 新增（68 键全量，母语级书面调） */
var T7={
ja:{_name:"日本語",time:"時間",text:"テキスト",m_sentences:"文章",m_quotes:"名言",m_numbers:"数字",m_words:"単語",st_time:"時間",wpm:"WPM",accuracy:"正確さ",r_cpm:"文字/分",r_errors:"ミス",r_raw:"Raw WPM",hint:'ここをクリックするか、<b>任意のキー</b>を押して入力を開始します',btn_again:"もう一度",btn_share:"結果をコピー",btn_copied:"コピーしました！",hist_title:"タイピング履歴（このブラウザに保存）",h_date:"日付",h_test:"テスト",hist_empty:"まだ結果がありません。テストを完了するとここに表示されます。",resume:"クリックして再開",kbd_size:"キーボード",r_cons:"安定度",sound:"サウンド",on:"オン",off:"オフ",pb_new:"自己ベスト更新！",pb_prev:"自己ベスト",skip:"タイピングテストへ移動",input_aria:"タイピング入力",timer_aria:"残り時間",chart_aria:"WPM 推移の折れ線グラフ",width:"幅",w_std:"標準",w_wide:"ワイド",w_xwide:"超ワイド",w_fluid:"全幅",practice:"練習",p_dvorak:"Dvorak",p_onehand:"片手",p_cert:"証明書",ks_missed:"最もミスしたキー",ks_slow:"最も遅いキー",ks_clean:"安定したクリーンな入力 — 際立った弱いキーはありません。",hist_export:"進捗をエクスポート",hist_import:"インポート",hist_bad:"ファイルを読み込めませんでした。Typing.Rerivo のエクスポートファイルですか？",streak:"連続練習",day:"日",days:"日",btn_img:"画像を保存",btn_weak:"弱いキーを練習",custom_text:"カスタムテキスト",custom_use:"このテキストを使う",custom_clear:"クリア",tier_beginner:"初心者",tier_developing:"成長中",tier_average:"平均",tier_above:"平均以上",tier_fast:"高速",tier_elite:"エリート",tiern_beginner:"平均 40 WPM 未満",tiern_developing:"平均 40 WPM に近い",tiern_average:"平均 40〜50 WPM 前後",tiern_above:"平均速度以上",tiern_fast:"上位約 10% のタイピスト",tiern_elite:"上位約 1% のタイピスト",heat_cap:"弱いキーが上のキーボードでハイライトされています。",p_colemak:"Colemak"},
ko:{_name:"한국어",time:"시간",text:"텍스트",m_sentences:"문장",m_quotes:"명언",m_numbers:"숫자",m_words:"단어",st_time:"시간",wpm:"WPM",accuracy:"정확도",r_cpm:"타자/분",r_errors:"오타",r_raw:"Raw WPM",hint:'여기를 클릭하거나 <b>아무 키</b>나 눌러 입력을 시작하세요',btn_again:"다시 하기",btn_share:"결과 복사",btn_copied:"복사했어요!",hist_title:"내 타자 기록 (이 브라우저에 저장됨)",h_date:"날짜",h_test:"테스트",hist_empty:"아직 기록이 없어요 — 테스트를 완료하면 여기에 표시돼요.",resume:"클릭해서 계속하기",kbd_size:"키보드",r_cons:"안정성",sound:"소리",on:"켜짐",off:"꺼짐",pb_new:"개인 최고 기록 경신!",pb_prev:"개인 최고 기록",skip:"타자 테스트로 건너뛰기",input_aria:"타자 입력",timer_aria:"남은 시간",chart_aria:"시간별 WPM 꺾은선 차트",width:"너비",w_std:"표준",w_wide:"넓게",w_xwide:"더 넓게",w_fluid:"전체",practice:"연습",p_dvorak:"Dvorak",p_onehand:"한 손",p_cert:"인증서",ks_missed:"가장 많이 틀린 키",ks_slow:"가장 느린 키",ks_clean:"깨끗하고 고른 입력 — 눈에 띄는 약한 키가 없어요.",hist_export:"진행 상황 내보내기",hist_import:"가져오기",hist_bad:"파일을 읽을 수 없어요 — Typing.Rerivo 내보내기 파일이 맞나요?",streak:"연속 연습",day:"일",days:"일",btn_img:"이미지 저장",btn_weak:"약한 키 연습",custom_text:"사용자 지정 텍스트",custom_use:"이 텍스트 사용",custom_clear:"지우기",tier_beginner:"입문",tier_developing:"성장 중",tier_average:"평균",tier_above:"평균 이상",tier_fast:"빠름",tier_elite:"엘리트",tiern_beginner:"평균 40 WPM 이하",tiern_developing:"평균 40 WPM에 근접",tiern_average:"평균 40–50 WPM 수준",tiern_above:"평균 속도 이상",tiern_fast:"상위 약 10%의 타이피스트",tiern_elite:"상위 약 1%의 타이피스트",heat_cap:"약한 키가 위의 키보드에 강조 표시돼요.",p_colemak:"Colemak"},
ur:{_name:"اردو",time:"وقت",text:"متن",m_sentences:"جملے",m_quotes:"اقوال",m_numbers:"نمبرز",m_words:"الفاظ",st_time:"وقت",wpm:"WPM",accuracy:"درستگی",r_cpm:"حروف/منٹ",r_errors:"غلطیاں",r_raw:"خام WPM",hint:'ٹائپنگ شروع کرنے کے لیے یہاں کلک کریں یا <b>کوئی بھی کلید</b> دبائیں',btn_again:"دوبارہ آزمائیں",btn_share:"نتیجہ کاپی کریں",btn_copied:"کاپی ہو گیا!",hist_title:"آپ کی ٹائپنگ تاریخ (اس براؤزر میں محفوظ)",h_date:"تاریخ",h_test:"ٹیسٹ",hist_empty:"ابھی کوئی نتیجہ نہیں — ٹیسٹ مکمل کریں تو یہاں نظر آئے گا۔",resume:"جاری رکھنے کے لیے کلک کریں",kbd_size:"کی بورڈ",r_cons:"استحکام",sound:"آواز",on:"آن",off:"آف",pb_new:"نیا ذاتی ریکارڈ!",pb_prev:"ذاتی بہترین",skip:"ٹائپنگ ٹیسٹ پر جائیں",input_aria:"ٹائپنگ ان پٹ",timer_aria:"باقی وقت",chart_aria:"وقت کے ساتھ WPM لائن چارٹ",width:"چوڑائی",w_std:"معیاری",w_wide:"چوڑا",w_xwide:"انتہائی چوڑا",w_fluid:"مکمل",practice:"مشق",p_dvorak:"Dvorak",p_onehand:"ایک ہاتھ",p_cert:"سرٹیفکیٹ",ks_missed:"سب سے زیادہ غلط ہونے والی کلیدیں",ks_slow:"سب سے سست کلیدیں",ks_clean:"صاف اور یکساں رفتار — کوئی نمایاں کمزور کلید نہیں۔",hist_export:"پیش رفت برآمد کریں",hist_import:"درآمد کریں",hist_bad:"فائل نہیں پڑھی جا سکی — کیا یہ Typing.Rerivo کی برآمد شدہ فائل ہے؟",streak:"مسلسل مشق",day:"دن",days:"دن",btn_img:"تصویر محفوظ کریں",btn_weak:"کمزور کلیدوں کی مشق",custom_text:"اپنا متن",custom_use:"یہ متن استعمال کریں",custom_clear:"صاف کریں",tier_beginner:"ابتدائی",tier_developing:"ترقی پذیر",tier_average:"اوسط",tier_above:"اوسط سے بہتر",tier_fast:"تیز",tier_elite:"ممتاز",tiern_beginner:"اوسط 40 WPM سے کم",tiern_developing:"اوسط 40 WPM کے قریب",tiern_average:"اوسط 40–50 WPM کے لگ بھگ",tiern_above:"اوسط رفتار سے زیادہ",tiern_fast:"بہترین ~10% ٹائپسٹ",tiern_elite:"بہترین ~1% ٹائپسٹ",heat_cap:"کمزور کلیدیں اوپر کی بورڈ پر نمایاں ہیں۔",p_colemak:"Colemak"},
id:{_name:"Indonesia",time:"Waktu",text:"Teks",m_sentences:"Kalimat",m_quotes:"Kutipan",m_numbers:"Angka",m_words:"Kata",st_time:"Waktu",wpm:"WPM",accuracy:"Akurasi",r_cpm:"Karakter/mnt",r_errors:"Kesalahan",r_raw:"WPM Mentah",hint:'Klik di sini atau tekan <b>tombol apa saja</b> untuk mulai mengetik',btn_again:"Coba lagi",btn_share:"Salin hasil",btn_copied:"Tersalin!",hist_title:"Riwayat mengetik Anda (tersimpan di browser ini)",h_date:"Tanggal",h_test:"Tes",hist_empty:"Belum ada hasil — selesaikan tes dan hasilnya akan muncul di sini.",resume:"Klik untuk melanjutkan",kbd_size:"Papan Ketik",r_cons:"Konsistensi",sound:"Suara",on:"aktif",off:"mati",pb_new:"Rekor pribadi baru!",pb_prev:"Rekor pribadi",skip:"Lewati ke tes mengetik",input_aria:"Masukan ketikan",timer_aria:"Sisa waktu",chart_aria:"Grafik garis WPM dari waktu ke waktu",width:"Lebar",w_std:"Standar",w_wide:"Lebar",w_xwide:"Ekstra Lebar",w_fluid:"Penuh",practice:"Latihan",p_dvorak:"Dvorak",p_onehand:"Satu Tangan",p_cert:"Sertifikat",ks_missed:"Tombol paling sering salah",ks_slow:"Tombol paling lambat",ks_clean:"Ketikan bersih dan merata — tidak ada tombol lemah yang menonjol.",hist_export:"Ekspor progres",hist_import:"Impor",hist_bad:"File tidak dapat dibaca — apakah ini file ekspor Typing.Rerivo?",streak:"Rangkaian",day:"hari",days:"hari",btn_img:"Simpan gambar",btn_weak:"Latih tombol lemah",custom_text:"Teks khusus",custom_use:"Gunakan teks ini",custom_clear:"Hapus",tier_beginner:"Pemula",tier_developing:"Berkembang",tier_average:"Rata-rata",tier_above:"Di atas rata-rata",tier_fast:"Cepat",tier_elite:"Elit",tiern_beginner:"di bawah rata-rata 40 WPM",tiern_developing:"mendekati rata-rata 40 WPM",tiern_average:"sekitar rata-rata 40–50 WPM",tiern_above:"di atas kecepatan rata-rata",tiern_fast:"~10% pengetik teratas",tiern_elite:"~1% pengetik teratas",heat_cap:"Tombol lemah disorot pada papan ketik di atas.",p_colemak:"Colemak"},
vi:{_name:"Tiếng Việt",time:"Thời gian",text:"Văn bản",m_sentences:"Câu",m_quotes:"Danh ngôn",m_numbers:"Số",m_words:"Từ",st_time:"Thời gian",wpm:"WPM",accuracy:"Độ chính xác",r_cpm:"Ký tự/phút",r_errors:"Lỗi",r_raw:"WPM thô",hint:'Nhấp vào đây hoặc nhấn <b>phím bất kỳ</b> để bắt đầu gõ',btn_again:"Thử lại",btn_share:"Sao chép kết quả",btn_copied:"Đã sao chép!",hist_title:"Lịch sử gõ của bạn (lưu trong trình duyệt này)",h_date:"Ngày",h_test:"Bài kiểm tra",hist_empty:"Chưa có kết quả — hãy hoàn thành một bài kiểm tra và nó sẽ hiện ở đây.",resume:"Nhấp để tiếp tục",kbd_size:"Bàn phím",r_cons:"Độ ổn định",sound:"Âm thanh",on:"bật",off:"tắt",pb_new:"Kỷ lục cá nhân mới!",pb_prev:"Kỷ lục cá nhân",skip:"Chuyển đến bài kiểm tra gõ",input_aria:"Ô nhập liệu",timer_aria:"Thời gian còn lại",chart_aria:"Biểu đồ đường WPM theo thời gian",width:"Độ rộng",w_std:"Tiêu chuẩn",w_wide:"Rộng",w_xwide:"Siêu rộng",w_fluid:"Toàn màn",practice:"Luyện tập",p_dvorak:"Dvorak",p_onehand:"Một tay",p_cert:"Chứng chỉ",ks_missed:"Phím hay gõ sai nhất",ks_slow:"Phím chậm nhất",ks_clean:"Gõ đều và sạch — không có phím yếu nổi bật.",hist_export:"Xuất tiến độ",hist_import:"Nhập",hist_bad:"Không đọc được tệp — đây có phải tệp xuất của Typing.Rerivo không?",streak:"Chuỗi ngày",day:"ngày",days:"ngày",btn_img:"Lưu hình ảnh",btn_weak:"Luyện phím yếu",custom_text:"Văn bản tùy chỉnh",custom_use:"Dùng văn bản này",custom_clear:"Xóa",tier_beginner:"Mới bắt đầu",tier_developing:"Đang tiến bộ",tier_average:"Trung bình",tier_above:"Trên trung bình",tier_fast:"Nhanh",tier_elite:"Xuất sắc",tiern_beginner:"dưới mức trung bình 40 WPM",tiern_developing:"sắp đạt mức trung bình 40 WPM",tiern_average:"khoảng mức trung bình 40–50 WPM",tiern_above:"trên tốc độ trung bình",tiern_fast:"~10% người gõ nhanh nhất",tiern_elite:"~1% người gõ nhanh nhất",heat_cap:"Các phím yếu được tô sáng trên bàn phím phía trên.",p_colemak:"Colemak"},
tr:{_name:"Türkçe",time:"Süre",text:"Metin",m_sentences:"Cümleler",m_quotes:"Alıntılar",m_numbers:"Rakamlar",m_words:"Kelimeler",st_time:"Süre",wpm:"WPM",accuracy:"Doğruluk",r_cpm:"Karakter/dk",r_errors:"Hatalar",r_raw:"Ham WPM",hint:'Yazmaya başlamak için buraya tıklayın veya <b>herhangi bir tuşa</b> basın',btn_again:"Tekrar dene",btn_share:"Sonucu kopyala",btn_copied:"Kopyalandı!",hist_title:"Yazma geçmişiniz (bu tarayıcıda saklanır)",h_date:"Tarih",h_test:"Test",hist_empty:"Henüz sonuç yok — bir testi tamamladığınızda burada görünecek.",resume:"Devam etmek için tıklayın",kbd_size:"Klavye",r_cons:"Tutarlılık",sound:"Ses",on:"açık",off:"kapalı",pb_new:"Yeni kişisel rekor!",pb_prev:"Kişisel rekor",skip:"Yazma testine geç",input_aria:"Yazı girişi",timer_aria:"Kalan süre",chart_aria:"Zamana göre WPM çizgi grafiği",width:"Genişlik",w_std:"Standart",w_wide:"Geniş",w_xwide:"Ekstra Geniş",w_fluid:"Tam",practice:"Alıştırma",p_dvorak:"Dvorak",p_onehand:"Tek El",p_cert:"Sertifika",ks_missed:"En çok hata yapılan tuşlar",ks_slow:"En yavaş tuşlar",ks_clean:"Temiz ve düzenli bir performans — belirgin zayıf tuş yok.",hist_export:"İlerlemeyi dışa aktar",hist_import:"İçe aktar",hist_bad:"Dosya okunamadı — bu bir Typing.Rerivo dışa aktarımı mı?",streak:"Seri",day:"gün",days:"gün",btn_img:"Görseli kaydet",btn_weak:"Zayıf tuşları çalış",custom_text:"Özel metin",custom_use:"Bu metni kullan",custom_clear:"Temizle",tier_beginner:"Başlangıç",tier_developing:"Gelişiyor",tier_average:"Ortalama",tier_above:"Ortalamanın üstü",tier_fast:"Hızlı",tier_elite:"Elit",tiern_beginner:"40 WPM ortalamasının altında",tiern_developing:"40 WPM ortalamasına yaklaşıyor",tiern_average:"40–50 WPM ortalaması civarında",tiern_above:"ortalama hızın üstünde",tiern_fast:"en iyi ~%10 daktilograf",tiern_elite:"en iyi ~%1 daktilograf",heat_cap:"Zayıf tuşlar yukarıdaki klavyede vurgulanıyor.",p_colemak:"Colemak"},
th:{_name:"ไทย",time:"เวลา",text:"ข้อความ",m_sentences:"ประโยค",m_quotes:"คำคม",m_numbers:"ตัวเลข",m_words:"คำ",st_time:"เวลา",wpm:"WPM",accuracy:"ความแม่นยำ",r_cpm:"อักขระ/นาที",r_errors:"ข้อผิดพลาด",r_raw:"WPM ดิบ",hint:'คลิกที่นี่หรือกด<b>ปุ่มใดก็ได้</b>เพื่อเริ่มพิมพ์',btn_again:"ทดสอบอีกครั้ง",btn_share:"คัดลอกผลลัพธ์",btn_copied:"คัดลอกแล้ว!",hist_title:"ประวัติการพิมพ์ของคุณ (บันทึกในเบราว์เซอร์นี้)",h_date:"วันที่",h_test:"แบบทดสอบ",hist_empty:"ยังไม่มีผลลัพธ์ — ทำแบบทดสอบให้เสร็จแล้วจะแสดงที่นี่",resume:"คลิกเพื่อพิมพ์ต่อ",kbd_size:"คีย์บอร์ด",r_cons:"ความสม่ำเสมอ",sound:"เสียง",on:"เปิด",off:"ปิด",pb_new:"สถิติส่วนตัวใหม่!",pb_prev:"สถิติส่วนตัว",skip:"ข้ามไปยังแบบทดสอบการพิมพ์",input_aria:"ช่องป้อนข้อความ",timer_aria:"เวลาที่เหลือ",chart_aria:"กราฟเส้น WPM ตามเวลา",width:"ความกว้าง",w_std:"มาตรฐาน",w_wide:"กว้าง",w_xwide:"กว้างพิเศษ",w_fluid:"เต็มจอ",practice:"ฝึกหัด",p_dvorak:"Dvorak",p_onehand:"มือเดียว",p_cert:"ใบรับรอง",ks_missed:"ปุ่มที่พิมพ์ผิดบ่อยสุด",ks_slow:"ปุ่มที่ช้าที่สุด",ks_clean:"การพิมพ์สะอาดสม่ำเสมอ — ไม่มีปุ่มอ่อนที่โดดเด่น",hist_export:"ส่งออกความคืบหน้า",hist_import:"นำเข้า",hist_bad:"ไม่สามารถอ่านไฟล์นั้นได้ — เป็นไฟล์ส่งออกของ Typing.Rerivo หรือไม่?",streak:"ต่อเนื่อง",day:"วัน",days:"วัน",btn_img:"บันทึกภาพ",btn_weak:"ฝึกปุ่มที่อ่อน",custom_text:"ข้อความกำหนดเอง",custom_use:"ใช้ข้อความนี้",custom_clear:"ล้าง",tier_beginner:"เริ่มต้น",tier_developing:"กำลังพัฒนา",tier_average:"ค่าเฉลี่ย",tier_above:"สูงกว่าค่าเฉลี่ย",tier_fast:"เร็ว",tier_elite:"ระดับสูง",tiern_beginner:"ต่ำกว่าค่าเฉลี่ย 40 WPM",tiern_developing:"ใกล้ถึงค่าเฉลี่ย 40 WPM",tiern_average:"อยู่ราวค่าเฉลี่ย 40–50 WPM",tiern_above:"สูงกว่าความเร็วเฉลี่ย",tiern_fast:"~10% แรกของนักพิมพ์",tiern_elite:"~1% แรกของนักพิมพ์",heat_cap:"ปุ่มที่อ่อนจะถูกเน้นไว้บนคีย์บอร์ดด้านบน",p_colemak:"Colemak"}
};
for(var l in T7){var d=T7[l];if(!I18N[l])I18N[l]={};for(var k in d){I18N[l][k]=d[k];}}
})();
(function(){var R={en:"Click to resume",zh:"点击继续打字",es:"Haz clic para continuar",hi:"जारी रखने के लिए क्लिक करें",ar:"انقر للمتابعة"};for(var k in R){if(I18N[k])I18N[k].resume=R[k];}})();
(function(){var R={en:"Keyboard",zh:"键盘大小",es:"Teclado",hi:"कीबोर्ड",ar:"لوحة المفاتيح"};for(var k in R){if(I18N[k])I18N[k].kbd_size=R[k];}})();
(function(){var M={
 r_cons:{en:"Consistency",zh:"稳定性",es:"Consistencia",hi:"स्थिरता",ar:"الثبات"},
 sound:{en:"Sound",zh:"音效",es:"Sonido",hi:"ध्वनि",ar:"الصوت"},
 on:{en:"on",zh:"开",es:"sí",hi:"चालू",ar:"تشغيل"},
 off:{en:"off",zh:"关",es:"no",hi:"बंद",ar:"إيقاف"},
 pb_new:{en:"New personal best!",zh:"刷新个人最佳！",es:"¡Nuevo récord personal!",hi:"नया व्यक्तिगत सर्वश्रेष्ठ!",ar:"أفضل رقم شخصي جديد!"},
 pb_prev:{en:"Personal best",zh:"个人最佳",es:"Récord personal",hi:"व्यक्तिगत सर्वश्रेष्ठ",ar:"أفضل رقم شخصي"}
};for(var key in M){var R=M[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
/* a11y: aria-label 也跟随语言切换（[data-aria] 元素）*/
(function(){var A={
 skip:{en:"Skip to typing test",zh:"跳到打字测试",es:"Saltar a la prueba",hi:"टाइपिंग टेस्ट पर जाएँ",ar:"تخطّي إلى اختبار الكتابة"},
 input_aria:{en:"Typing input",zh:"打字输入框",es:"Campo de escritura",hi:"टाइपिंग इनपुट",ar:"حقل الكتابة"},
 timer_aria:{en:"Time remaining",zh:"剩余时间",es:"Tiempo restante",hi:"शेष समय",ar:"الوقت المتبقي"},
 chart_aria:{en:"WPM over time line chart",zh:"WPM 随时间变化折线图",es:"Gráfico de PPM en el tiempo",hi:"समय के साथ WPM रेखाचित्र",ar:"رسم بياني للسرعة عبر الزمن"}
};for(var key in A){var R=A[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
/* 打字区宽度：用户偏好 trWidth 持久化，档位与 style.css 的 .wrap.w-* 一一对应 */
(function(){var W={
 width:{en:"Width",zh:"宽度",es:"Ancho",hi:"चौड़ाई",ar:"العرض"},
 w_std:{en:"Standard",zh:"标准",es:"Estándar",hi:"मानक",ar:"قياسي"},
 w_wide:{en:"Wide",zh:"宽",es:"Ancho",hi:"चौड़ा",ar:"واسع"},
 w_xwide:{en:"X-Wide",zh:"更宽",es:"Muy ancho",hi:"बहुत चौड़ा",ar:"أوسع"},
 w_fluid:{en:"Full",zh:"全宽",es:"Total",hi:"पूरा",ar:"كامل"}
};for(var key in W){var R=W[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
/* 练习模式快捷入口（Reddit 反馈：Dvorak/单手/证书模式藏页脚找不到）*/
(function(){var P={
 practice:{en:"Practice",zh:"练习",es:"Práctica",hi:"अभ्यास",ar:"تمرين"},
 p_dvorak:{en:"Dvorak",zh:"Dvorak 键盘",es:"Dvorak",hi:"Dvorak",ar:"Dvorak"},
 p_onehand:{en:"One-Hand",zh:"单手打字",es:"Una mano",hi:"एक हाथ",ar:"يد واحدة"},
 p_cert:{en:"Certificate",zh:"打字证书",es:"Certificado",hi:"प्रमाणपत्र",ar:"شهادة"}
};for(var key in P){var R=P[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var K={
 ks_missed:{en:"Most-missed keys",zh:"最常打错的键",es:"Teclas más falladas",hi:"सबसे ज़्यादा गलत कुंजियाँ",ar:"المفاتيح الأكثر خطأً"},
 ks_slow:{en:"Slowest keys",zh:"最慢的键",es:"Teclas más lentas",hi:"सबसे धीमी कुंजियाँ",ar:"المفاتيح الأبطأ"},
 ks_clean:{en:"Clean, even run — no standout weak keys.",zh:"干净平稳，没有明显的弱键。",es:"Pulsación limpia y uniforme: sin teclas débiles destacadas.",hi:"साफ़, एकसमान प्रयास — कोई खास कमज़ोर कुंजी नहीं।",ar:"أداء نظيف ومتساوٍ — لا مفاتيح ضعيفة بارزة."}
};for(var key in K){var R=K[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var H={
 hist_export:{en:"Export progress",zh:"导出进度",es:"Exportar progreso",hi:"प्रगति निर्यात करें",ar:"تصدير التقدم"},
 hist_import:{en:"Import",zh:"导入",es:"Importar",hi:"आयात करें",ar:"استيراد"},
 hist_bad:{en:"Could not read that file — is it a Typing.Rerivo export?",zh:"无法读取该文件 —— 它是 Typing.Rerivo 导出的进度吗？",es:"No se pudo leer el archivo: ¿es una exportación de Typing.Rerivo?",hi:"वह फ़ाइल नहीं पढ़ी जा सकी — क्या यह Typing.Rerivo निर्यात है?",ar:"تعذّرت قراءة الملف — هل هو ملف تصدير من Typing.Rerivo؟"}
};for(var key in H){var R=H[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var S={
 streak:{en:"Streak",zh:"连续练习",es:"Racha",hi:"स्ट्रीक",ar:"سلسلة"},
 day:{en:"day",zh:"天",es:"día",hi:"दिन",ar:"يوم"},
 days:{en:"days",zh:"天",es:"días",hi:"दिन",ar:"أيام"}
};for(var key in S){var R=S[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var G={btn_img:{en:"Save image",zh:"保存成绩图",es:"Guardar imagen",hi:"इमेज सहेजें",ar:"حفظ الصورة"}};for(var key in G){var R=G[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var Wk={btn_weak:{en:"Practice weak keys",zh:"专练弱键",es:"Practicar teclas débiles",hi:"कमज़ोर कुंजियाँ अभ्यास",ar:"تدريب المفاتيح الضعيفة"}};for(var key in Wk){var R=Wk[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var Ct={
 custom_text:{en:"Custom text",zh:"自定义文本",es:"Texto personalizado",hi:"कस्टम पाठ",ar:"نص مخصص"},
 custom_use:{en:"Use this text",zh:"用这段文本",es:"Usar este texto",hi:"इस पाठ का उपयोग करें",ar:"استخدم هذا النص"},
 custom_clear:{en:"Clear",zh:"清除",es:"Borrar",hi:"हटाएँ",ar:"مسح"}
};for(var key in Ct){var R=Ct[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
(function(){var T={
 tier_beginner:{en:"Beginner",zh:"入门",es:"Principiante",hi:"शुरुआती",ar:"مبتدئ"},
 tier_developing:{en:"Developing",zh:"进步中",es:"En progreso",hi:"विकासशील",ar:"متطور"},
 tier_average:{en:"Average",zh:"普通",es:"Promedio",hi:"औसत",ar:"متوسط"},
 tier_above:{en:"Above average",zh:"高于平均",es:"Sobre la media",hi:"औसत से ऊपर",ar:"فوق المتوسط"},
 tier_fast:{en:"Fast",zh:"快速",es:"Rápido",hi:"तेज़",ar:"سريع"},
 tier_elite:{en:"Elite",zh:"精英",es:"Élite",hi:"विशिष्ट",ar:"نخبة"},
 tiern_beginner:{en:"below the 40 WPM average",zh:"低于 40 WPM 的平均水平",es:"por debajo de la media de 40 PPM",hi:"40 WPM के औसत से नीचे",ar:"أقل من متوسط 40 كلمة/د"},
 tiern_developing:{en:"nearing the 40 WPM average",zh:"接近 40 WPM 的平均水平",es:"cerca de la media de 40 PPM",hi:"40 WPM के औसत के करीब",ar:"يقترب من متوسط 40 كلمة/د"},
 tiern_average:{en:"around the 40–50 WPM average",zh:"处于 40–50 WPM 的平均区间",es:"en torno a la media de 40–50 PPM",hi:"40–50 WPM के औसत के आसपास",ar:"حول متوسط 40–50 كلمة/د"},
 tiern_above:{en:"above the average speed",zh:"高于平均打字速度",es:"por encima de la velocidad media",hi:"औसत गति से तेज़",ar:"أعلى من السرعة المتوسطة"},
 tiern_fast:{en:"top ~10% of typists",zh:"约前 10% 的打字者",es:"~10% más rápido",hi:"शीर्ष ~10% टाइपिस्ट",ar:"ضمن أسرع ~10%"},
 tiern_elite:{en:"top ~1% of typists",zh:"约前 1% 的打字者",es:"~1% más rápido",hi:"शीर्ष ~1% टाइपिस्ट",ar:"ضمن أسرع ~1%"},
 heat_cap:{en:"Weak keys are highlighted on the keyboard above.",zh:"较弱的按键已在上方键盘高亮显示。",es:"Las teclas débiles se resaltan en el teclado de arriba.",hi:"कमज़ोर कुंजियाँ ऊपर कीबोर्ड पर हाइलाइट की गई हैं।",ar:"المفاتيح الضعيفة مميّزة على لوحة المفاتيح أعلاه."},
 p_colemak:{en:"Colemak",zh:"Colemak",es:"Colemak",hi:"Colemak",ar:"Colemak"}
};for(var key in T){var R=T[key];for(var k in R){if(I18N[k])I18N[k][key]=R[k];}}})();
var LANGS=["en","zh","es","hi","ar","ja","ko","ur","id","vi","tr","th"];
var WIDTHS=["std","wide","xwide","fluid"];
var THEMES=[["dark","🌙"],["light","☀️"],["ocean","🌊"],["sepia","📖"],["green","🌿"]];
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}

var TR={lang:"en"};
TR.t=function(k){var d=I18N[TR.lang]||I18N.en;return (d[k]!=null?d[k]:I18N.en[k])||"";};
TR.pool=function(l){return POOL[l]||null;};
var UNITS={en:{s:"s",m:" min"},zh:{s:"秒",m:"分"},es:{s:" s",m:" min"},hi:{s:" सेकंड",m:" मिनट"},ar:{s:" ث",m:" د"},ja:{s:"秒",m:"分"},ko:{s:"초",m:"분"},ur:{s:" س",m:" منٹ"},id:{s:" dtk",m:" mnt"},vi:{s:" giây",m:" phút"},tr:{s:" sn",m:" dk"},th:{s:" วิ",m:" นาที"}};
TR.fmtDur=function(sec,l){var u=UNITS[l]||UNITS.en;return sec<60?(sec+u.s):((sec/60)+u.m);};
TR.modeLabel=function(m){return TR.t("m_"+m)||m;};
window.TR=TR;
function updateDurChips(){
  var ch=document.querySelectorAll(".chip.dur");
  for(var i=0;i<ch.length;i++){var d=parseInt(ch[i].getAttribute("data-d"),10);if(!isNaN(d))ch[i].textContent=TR.fmtDur(d,TR.lang);}
}

function translate(){
  var d=I18N[TR.lang]||I18N.en;
  var els=document.querySelectorAll("[data-i18n]");
  for(var i=0;i<els.length;i++){var k=els[i].getAttribute("data-i18n");if(d[k]!=null||I18N.en[k]!=null)els[i].textContent=TR.t(k);}
  var hs=document.querySelectorAll("[data-i18n-html]");
  for(var j=0;j<hs.length;j++){var kk=hs[j].getAttribute("data-i18n-html");hs[j].innerHTML=TR.t(kk);}
  var da=document.querySelectorAll("[data-aria]");
  for(var n=0;n<da.length;n++){var ka=da[n].getAttribute("data-aria");var av=TR.t(ka);if(av)da[n].setAttribute("aria-label",av);}
}

function setLang(l,fire,persist){
  if(LANGS.indexOf(l)<0)l="en"; TR.lang=l; if(persist!==false)ls("trLang",l);
  document.documentElement.lang=l;
  document.documentElement.dir=(l==="ar"||l==="ur")?"rtl":"ltr";
  translate();
  updateDurChips();
  if(fire)window.dispatchEvent(new Event("tr-relang"));
}
function setTheme(t){
  if(t==="dark")document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme",t);
  ls("trTheme",t);
  var btns=document.querySelectorAll(".tr-theme-btn");
  for(var i=0;i<btns.length;i++)btns[i].setAttribute("aria-pressed", btns[i].getAttribute("data-theme")===t?"true":"false");
}

function buildBar(){
  var css=document.createElement("style");
  css.textContent=
   ".tr-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:10px 12px;margin-left:auto;}"+
   ".tr-sel{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:999px;"+
     "padding:6px 30px 6px 13px;font-size:.85rem;font-weight:600;cursor:pointer;font-family:inherit;"+
     "-webkit-appearance:none;appearance:none;transition:border-color .15s,background .15s;"+
     "background-image:url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path d='M1 1l4 4 4-4' stroke='%238b8fa3' stroke-width='1.6' fill='none' stroke-linecap='round'/></svg>\");"+
     "background-repeat:no-repeat;background-position:right 12px center;}"+
   "html[dir=rtl] .tr-sel{padding:6px 13px 6px 30px;background-position:left 12px center;}"+
   ".tr-sel:hover{border-color:var(--borderhi);background-color:var(--panelhi);}"+
   ".tr-themes{display:inline-flex;gap:4px;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:3px;}"+
   ".tr-theme-btn{border:none;background:transparent;cursor:pointer;border-radius:999px;width:30px;height:28px;"+
     "font-size:.95rem;line-height:1;display:inline-flex;align-items:center;justify-content:center;transition:background .15s;padding:0;}"+
   ".tr-theme-btn:hover{background:var(--panelhi);}"+
   ".tr-theme-btn[aria-pressed=true]{background:linear-gradient(180deg,var(--accent2),var(--accent));box-shadow:0 3px 10px -4px var(--accentglow);}";
  document.head.appendChild(css);

  var bar=document.createElement("div"); bar.className="tr-bar";
  var sel=document.createElement("select"); sel.className="tr-sel"; sel.setAttribute("aria-label","Language");
  for(var i=0;i<LANGS.length;i++){var o=document.createElement("option");o.value=LANGS[i];o.textContent=I18N[LANGS[i]]._name;sel.appendChild(o);}
  sel.value=TR.lang;
  sel.addEventListener("change",function(){setLang(sel.value,true);});
  bar.appendChild(sel);
  var msel=document.createElement("select"); msel.className="tr-sel"; msel.setAttribute("aria-label","Background music");
  for(var mi=0;mi<MUSIC_STYLES.length;mi++){var mo=document.createElement("option");mo.value=MUSIC_STYLES[mi][0];mo.textContent=MUSIC_STYLES[mi][1];msel.appendChild(mo);}
  msel.value=ls("trMusic")||"off";
  msel.addEventListener("change",function(){setMusic(msel.value);});
  bar.appendChild(msel);

  var tw=document.createElement("div"); tw.className="tr-themes";
  var cur=ls("trTheme")||"dark";
  for(var k=0;k<THEMES.length;k++){
    (function(th){var btt=document.createElement("button");btt.className="tr-theme-btn";btt.setAttribute("data-theme",th[0]);
      btt.setAttribute("type","button");btt.setAttribute("aria-label",th[0]+" theme");btt.textContent=th[1];
      btt.setAttribute("aria-pressed", th[0]===cur?"true":"false");
      btt.addEventListener("click",function(){setTheme(th[0]);});tw.appendChild(btt);})(THEMES[k]);
  }
  bar.appendChild(tw);

  var header=document.querySelector("header.top");
  if(header){header.appendChild(bar);}
  else{bar.style.position="fixed";bar.style.top="12px";bar.style.right="12px";bar.style.zIndex="50";document.body.appendChild(bar);}
}

function setWidth(w){
  if(WIDTHS.indexOf(w)<0)w="std";
  var wrap=document.querySelector(".wrap");
  if(wrap){wrap.classList.remove("w-std","w-wide","w-xwide","w-fluid");wrap.classList.add("w-"+w);}
  ls("trWidth",w);
  var ch=document.querySelectorAll(".chip.width");
  for(var i=0;i<ch.length;i++){
    var on=ch[i].getAttribute("data-w")===w;
    ch[i].classList.toggle("on",on);
    ch[i].setAttribute("aria-pressed", on?"true":"false");
  }
}

/* ---------- 各国轻音乐（WebAudio 程序化生成，零版权、零音频文件）---------- */
var MUSIC_STYLES=[["off","🔇 Music"],["cn","🏮 中文"],["jp","🎐 日本"],["me","🕌 中东"],["es","💃 西班牙"],["in","🪷 印度"],["lofi","🎧 Lo-fi"]];
var SCALES={cn:[0,2,4,7,9],jp:[0,2,3,7,8],me:[0,1,4,5,7,8,11],es:[0,1,4,5,7,8,10],"in":[0,1,4,5,7,8,11],lofi:[0,3,5,7,10]};
var AC=null,master=null,musicTimer=null,curStyle="off",nextTime=0;
function mfreq(s){return 220*Math.pow(2,s/12);}
function ensureCtx(){
  if(!AC){try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return null;}
    master=AC.createGain();master.gain.value=0;
    var lp=AC.createBiquadFilter();lp.type="lowpass";lp.frequency.value=2600;lp.Q.value=0.7;
    master.connect(lp);lp.connect(AC.destination);}
  return AC;
}
function mvoice(f,t,dur,g,type){
  var o=AC.createOscillator(),ga=AC.createGain();
  o.type=type||"sine";o.frequency.value=f;
  ga.gain.setValueAtTime(0.0001,t);ga.gain.linearRampToValueAtTime(g,t+0.09);
  ga.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  o.connect(ga);ga.connect(master);o.start(t);o.stop(t+dur+0.05);
}
function mschedule(){
  if(curStyle==="off"||!AC)return;
  var sc=SCALES[curStyle]||SCALES.lofi,now=AC.currentTime;
  while(nextTime<now+1.5){
    var deg=sc[Math.floor(Math.random()*sc.length)]+12*Math.floor(Math.random()*2);
    mvoice(mfreq(deg),nextTime,1.7,0.085,"triangle");
    if(Math.random()<0.45)mvoice(mfreq(sc[0]-12),nextTime,2.6,0.045,"sine");
    nextTime+=0.82+Math.random()*0.55;
  }
}
function startMusic(style){
  curStyle=style;if(style==="off"){stopMusic();return;}
  if(!ensureCtx())return;
  if(AC.state==="suspended")AC.resume();
  master.gain.cancelScheduledValues(AC.currentTime);
  master.gain.linearRampToValueAtTime(0.14,AC.currentTime+0.7);
  nextTime=AC.currentTime+0.1;
  if(!musicTimer)musicTimer=setInterval(mschedule,500);
  mschedule();
}
function stopMusic(){
  curStyle="off";
  if(musicTimer){clearInterval(musicTimer);musicTimer=null;}
  if(master&&AC){master.gain.cancelScheduledValues(AC.currentTime);master.gain.linearRampToValueAtTime(0,AC.currentTime+0.4);}
}
function setMusic(style,persist){
  if(persist!==false)ls("trMusic",style);
  if(style==="off")stopMusic();else startMusic(style);
}

function init(){
  buildBar();
  var savedMusic=ls("trMusic");
  if(savedMusic&&savedMusic!=="off"){
    var once=function(){document.removeEventListener("pointerdown",once);document.removeEventListener("keydown",once);setMusic(savedMusic,false);};
    document.addEventListener("pointerdown",once);document.addEventListener("keydown",once);
  }
  var stored=ls("trLang");
  var l=stored||(window.__trPageLang||"en");
  setLang(l,l!=="en",!!stored);
  setTheme(ls("trTheme")||"dark");
  var wch=document.querySelectorAll(".chip.width");
  for(var i=0;i<wch.length;i++){
    (function(btn){btn.addEventListener("click",function(){setWidth(btn.getAttribute("data-w"));});})(wch[i]);
  }
  setWidth(ls("trWidth")||"std");
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
})();
;
/* ---------- R11: SEO/FAQ 折叠控制器 — 工具优先，内容按需展开 ---------- */
(function(){
  var seoEl=document.querySelector('.seo');
  var faqEl=document.querySelector('.faq');
  if(!seoEl||!faqEl)return;
  seoEl.classList.add('collapsed');
  faqEl.classList.add('collapsed');
  var btn=document.createElement('button');
  btn.className='toggle-btn'; btn.textContent='📖 阅读完整指南 ▼';
  btn.setAttribute('aria-expanded','false');
  var result=document.querySelector('#resultPanel');
  var parent=seoEl.parentNode;
  parent.insertBefore(btn,seoEl);
  var open=false;
  btn.addEventListener('click',function(){
    open=!open;
    seoEl.classList.toggle('collapsed',!open);
    faqEl.classList.toggle('collapsed',!open);
    btn.setAttribute('aria-expanded',String(open));
    btn.textContent=open?'▲ 收起指南':'📖 阅读完整指南 ▼';
    if(!open)btn.scrollIntoView({behavior:'smooth',block:'nearest'});
  });
})();;