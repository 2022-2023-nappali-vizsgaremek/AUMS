
<div align="center">
  <span>Táborosi Balázs, Magyar Máté, Lator Bence</span><br>
  <img src="https://user-images.githubusercontent.com/98460366/228148967-96f0d9f0-a525-43b2-b612-5abff63da560.png">
  <h1 align="center">Access And User Management System<br><br>

  ![aums](https://user-images.githubusercontent.com/98460366/236650354-10a61b17-0abd-4ddb-9ec5-6038546b8344.gif)
</h1>
</div>

<div align="center">
  
### Összefoglaló
  
A projekt célja egy egyszerű, de könnyen használható beléptető és felhasználó kezelő rendszer létrehozása.<br>Az AUMS tartalmazza ezen, és további hasznos funckiókat amelyek lényegesen hatékonyabbá tehetik egy adott felhasználói kör munkafolyamatait.
  
  <hr>
</div>
<br>

# Felhasználói folyamatok
- Bejelentkezés: A főoldalon található bejelentkezési űrlap használatával a felhasználó eljuthat a komplexebb rendszerek megtekintéséhez.
- A bejelentkezett felhasználó a jogkörőtél függően további elemekehet láthat
  - A főoldalon mindenki számára elérhető a saját adatainak megtekintése, a kijelentkezés, illetve a jelszó megváltoztatásához használható űrlap. A navigációban pedig az időbeosztás menüpont.
  - Magasabb jogkör esetében (mint pl. Admin) elérhető a menüpontok között a regisztrációs felület, kártya kezelési opciók, időbeosztás, felhasználó kezelési lehetőségek, log üzenetek megfigyelése.
- Fizikai belépés: A regisztrált felhasználó a kapott kártyát érinthető a beléptető dobozhoz, amely az ellenőrzés után lehetővé teszi számára a felhasznált környezetbe való ki és beléptetést.

<br>

# Folyamat specifikáció
### Bejelentkezés
  - Az űrlap elemei ellenőrzött valós adatokat várnak, a pontos adatok megadásáig a felhasználó hiba üzenetet kap.
  - Az első eléréshez használható admin felhasználó hozzáférhető az "admin.admin" (vagy "admin.admin@proj-aums.hu") és "admin" email-jelszó páros megadásával.
    - Más esetben a felhasználó a kapott email/felhasználónév és jelszó páros bevitelével juthat tovább (A regisztráció magasabb jogkörhöz kötött a belső környezet kialakítása érdekében).
### Kijelentkezés, Jelszó változtatás
  - A főoldalon a bejelentkezési űrlapot felváltja a felhasználói adatmegjelenítés, illetve a kijelentkezés és jelszó változtatás lehetősége.
  - A kijelentkezés gomb megnyomásával a felhasználó visszakerül a kezdő státuszba, a jogköréhez tartozó lehetőségek láthatósága megszűnik.
  - A jelszó váltás gomb megnyomásával és változtatási űrlap kerül a központba, ahol a jelenlegi és az új jelszó (és annak megerősítése) megfelelő megadásával a jelszó megváltoztatható.
### Regisztráció
  - A regisztráció egy magasabb szintű lehetőség, ennek a célja a belső (pl. céges) környezet kialakítása.
  - A menüpont kiválasztása után megjelenik a regisztrációs űrlap, a kitöltés során minden mező kitöltése kötelező.
  - A kitöltést követően a sikeres ellenőrzés után a regisztrált új felhasználó (éles rendszeren) emailben megkapja a bejelentkezéshez használható email-jelszó párost.
### Kártya kezelés
  - Ezen menüpont adja a lehetőséget, hogy az adminisztrátor összekapcsolja (vagy szétkapcsolja) a felhasználókat a fizikai kártyával.
  - Továbbá biztosítja az új kártyák felvitelét a rendszerbe, a kártyák aktiválását, törlését, módosítását és minden egyéb kártyával kapcsolatos lehetőséget.
### Időbeosztás
  - Az oldalon megtekinthető a kártya használatával generált ki- és belépési időpont párosok statisztikája az adott napokon.
### Felhasználó kezelés
  - Ezen adminisztrátori opció lehetőséget nyújt a felvitt felhasználók törlésére vagy az adatainak a szerkesztésére.
  - A törléshez a piros "X" gomb megnyomása használható, a módosítás pedig a felhasználóra való kattintáskor, előugró űrlap formájában érhető el.
### Log
  - A futási folyamatok üzeneteinek megtekintése az admin számára.
  - Az oldal lehetővé teszi az esetleges problémák kiszűrését és a futás során keletkező adatok begyűjtését/feldolgozását.

<br>

# Felhasznált rendszerek
### Szerver
  - Az éles rendszer tárolását és futtatását egy fizikai szerver végzi.
  - A szerver docker technológiát használva futtatja az elemeket, proxy segíti a domain kapcsolatokat és az irányított működést.
### Domain
  - A kezelői felület elérhető a https://proj-aums.hu/ címen keresztül.
  - Ehhez továbbá tartozik a https://pma.proj-aums.hu/ amely a phpMyAdmin felületet adja meg.
  - Illetve a https://api.proj-aums.hu/ alap megadásával érhetőek el a különböző backend API endpointok.
  - Végül a https://email.proj-aums.hu/ átirányítja a felhasználókat a belső levelezési rendszer oldalára.
### GitHub
  - A GitHub tartalmazza a projekt forráskódját, illetve az itt megtalálható action végzi az új kiadások ellenőrzését és feltöltését a szerverre.
  - Továbbá a GitHub action feladata a desktop alkalmazás ellenőrzuése és telepítő készletének létrehozása, amit Release elemként csatol a projekt oldalához.
  - A szerveren található automatikus megfigyelő észleli a github által létrehozott új kiadást és ezt frissíti a szerveren is, így mindig a legújabb verzió kerül az éles rendszerre.
### Desktop
  - Telepítás után, az indítást követően megjelenik és használhatóvá válik a frontend rendszer.
  - A desktop alkalmazás electron felhasználásával készült, multi platform lehetőséget biztosítva.
### Frontend
  - Felhasználásra került benne többek között: axios, router, bootstrap stb.
  - Vue.js felhasználásával került létrehozásra, biztosítja a projekt működéséhez szükséges műveleteket.
### Backend
  - Python flask biztosítja a backend működést.
  - Rest API rendszer kiépítése, SQL Alchemy adatbázis kezelés és ORM működés biztosítása.
  - Tartalmaz teszt folyamatokat, környezeti változókat, bcrypt felhasználásával titkosítást, email küldést...
  - A felépítése jól tagolt, model-controller-service struktúrát követ, biztosítja a bejelentkezési és jogkör védelmet...
### Hardware
  - 3D nyomtatott doboz tartalmazza a hardware eszközöket.
  - Az energia ellátást egy külső akkumulátor végzi, a státuszmegjelenítésért három LED felelős.
  - NodeMCU (Arduino WiFi) kezeli az RFID kártya és olvasó páros adatinak küldését a backend felé.

<br>

# Localhost útmutató
- A desktop alkalmazás elindítható a hozzá tartozó mappában az npm start parancs kiadásával.
- A helyi gépen történő telepítés esetében a backend mappában az app.py elindítása szükséges (elérése a localhost:5000 vagy IP:5000 páros használatával)
- A frotend mappában az npm run dev, vagy npm run build parancs kiadásával futtatható a frontend felület (elérése a localhost:5173 címen vagy --host esetében a host IP és port megadásával).
