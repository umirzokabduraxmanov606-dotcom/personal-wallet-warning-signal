# personal-wallet-warning-signal
# 🚨 Personal Wallet Warning Signal

**Author:** Umirzok Mamatmurodovich Abduraxmanov  
**Contact:** umirzokabduraxmanov606@gmail.com | +998 99 660 9590

## 📌 Overview

**Personal Wallet Warning Signal** — bu yangi xavfsizlik tizimi bo‘lib, foydalanuvchi kriptovalyutani **shaxsiy (EOA) yoki birjaga tegishli bo‘lmagan hamyon manziliga yuborishidan oldin avtomatik ogohlantiradi.**  
Bu tizim foydalanuvchilarni, ayniqsa yangi boshlovchilarni, eng keng tarqalgan firibgarliklardan himoya qilishga mo‘ljallangan.

## ❗ Problem

Har yili minglab foydalanuvchilar tasodifan scammerlar boshqaradigan shaxsiy hamyonlarga mablag‘ yuborib, pullarini yo‘qotadilar.  
Hozirgi tizimlar (masalan, Etherscan Risk Alert) faqat tranzaksiya amalga oshgandan keyin ogohlantiradi. Bu loyiha esa **tranzaksiya amalga oshishidan oldin to‘xtatadi.**

## 🧠 Solution: Step-by-Step

1. **Address Validation** – Manzil formati, uzunligi va blockchain turini (TRC20/ERC20) tekshiradi.  
2. **Exchange Registry Check** – Manzilni ishonchli birja manzillari bazasi bilan solishtiradi.  
3. **EOA vs Custodial Detection** – Manzil shaxsiy hamyon yoki custodial ekanini aniqlaydi.  
4. **Risk Analysis** – Blacklist, phishing, scam ma’lumotlari bilan tekshiradi va xavf darajasini baholaydi.  
5. **New User Sensitivity** – Yangi akkauntlar uchun qat’iyroq qoidalar qo‘llanadi (<5 tranzaksiya bo‘lsa).  
6. **Warning & Block** –  
   - ⚠️ “Bu manzil shaxsiy yoki tasdiqlanmagan. Scam xavfi mavjud.”  
   - ❌ Cancel → Tranzaksiya bekor qilinadi  
   - ✅ Proceed → 2FA talab qilinadi va yuborishdan oldin kichik kechikish qo‘yiladi  
7. **Logging & Analytics** – Har bir harakat (manzil, xavf balli, vaqt) qayd qilinadi.

## 🛡️ Benefits

- Yangi foydalanuvchilarni scam va xatoliklardan himoya qiladi  
- Firibgarlik tranzaksiyalarini kamaytiradi  
- Kripto sanoatida yangi xavfsizlik standarti bo‘lishi mumkin

## 🔄 Next Steps

- CertiK, Chainalysis, Binance va boshqa xavfsizlik kompaniyalari bilan hamkorlik  
- Yirik birjalarga integratsiya qilish  
- API ishlab chiqish va ommaviy tizim sifatida joriy etish

---

📌 *Bu loyiha real firibgarlik tajribasiga asoslangan bo‘lib, butun dunyodagi foydalanuvchilar xavfsizligini oshirishga qaratilgan. Mualliflik huquqi saqlanadi.*
