# Skupni prevozi – Platforma za deljenje prevozov


### 1. Identifikacija problema in opis rešitve

**Problem:**  
Veliko ljudi se vsak dan vozi na podobne relacije (služba, šola, dogodki), vendar avtomobile pogosto uporabljajo sami. To povzroča prometne zastoje, povečano porabo goriva in dodatne stroške.

**Rešitev:**  
Skupni prevozi je spletna aplikacija, ki omogoča uporabnikom, da objavijo svoje vožnje in jih delijo z drugimi. S tem se zmanjšajo stroški prevoza, poveča ekološka učinkovitost in spodbuja sodelovanje med uporabniki.

**Ciljna skupina:**  
Dijaki, študenti, zaposleni in vsi, ki redno opravljajo podobne poti in želijo prihraniti pri prevozu.

---

### 2. Analiza trga

**Velikost trga:**  
Veliko ljudi se dnevno vozi na podobne lokacije, kar predstavlja veliko priložnost za uporabo takšne platforme.

**Konkurenčna analiza:**

- **Obstoječe rešitve:** BlaBlaCar, prevozi.org  
- **Prednosti Skupni prevozi:** Enostaven uporabniški vmesnik, ni potrebe po registraciji z osebnimi podatki tretjih strani, fokusirano na lokalne prevoze.  
- **Slabosti konkurentov:** Kompleksnejši postopki, manj primeren za vsakodnevne poti.

---

### 3. SWOT analiza

**PREDNOSTI (S):**
- Enostavno dodajanje in iskanje voženj
- Uporabniški sistem z možnostjo vpogleda v lastne in tuje vožnje
- Pregleden vmesnik

**SLABOSTI (W):**
- Trenutno ni sistema za ocenjevanje voznikov/sopotnikov
- Brez integracije z zemljevidi

**PRILOŽNOSTI (O):**
- Možnost integracije z mobilno aplikacijo ali obvestili
- Razširitev na šole, podjetja, dogodke

**GROŽNJE (T):**
- Konkurenčne platforme z večjim dosegom
- Potencialni pomisleki glede zasebnosti in varnosti

---

### 4. Poslovni model in finančni plan

**Prihodki:**
- Aplikacija je brezplačna, v prihodnosti možna uvedba oglaševanja ali naročnin za dodatne funkcije (npr. prioritetno prikazovanje voženj).

**Stroški:**
- Gostovanje, razvoj, vzdrževanje aplikacije
- Morebitna promocija na dogodkih ali socialnih omrežjih

**Strategija pridobivanja uporabnikov:**
- Promocija med študenti, šolami, skupnostmi in na forumih
- Sodelovanje z organizatorji dogodkov ali šolami za spodbujanje uporabe

---

### 5. Pitch predstavitev

Predstavitev bo prikazala, kako lahko uporabnik doda svojo vožnjo, pregleda vožnje drugih in kontaktira sopotnike. Poudarek bo na enostavni uporabi, varčnosti in ekološki vrednosti.

---


### 1. Flask osnove

- Uporaba Flask frameworka z dobro strukturo projekta (views, templates, static, forms)
- Prijava, registracija, odjava in zaščita poti (login required)
- Predloge ustvarjene z Jinja templating sistemom
- Posamezne HTML strani (moje vožnje, vse vožnje, dodaj vožnjo)
- Obvladovanje napak (npr. neprijavljen dostop)

---

### 2. Uporabniški sistem

- Registracija, prijava in odjava z uporabo sej (session)
- Preverjanje edinstvenosti uporabniškega imena
- Validacija obrazcev (npr. prazna polja)
- Sejni sistem preprečuje dostop neavtentificiranim uporabnikom

---

### 3. Interakcija z bazo

- Uporaba TinyDB za shranjevanje uporabnikov in voženj
- Možnost dodajanja voženj s podatki (začetek, destinacija, datum, ura, cena, telefonska)
- Prikaz samo svojih ali tujih voženj
- Odstranjevanje lastnih voženj (z zaščito pred brisanjem tujih)

---



---

## Zaključek

Skupni prevozi omogočajo uporabnikom enostavno objavo in iskanje prevozov, s čimer prispevajo k varčevanju, večji povezanosti in ekološki ozaveščenosti. Projekt združuje sodoben spletni razvoj z uporabno rešitvijo za vsakodnevne potrebe.
