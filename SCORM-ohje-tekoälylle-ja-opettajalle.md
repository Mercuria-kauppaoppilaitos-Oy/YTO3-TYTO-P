# SCORM 1.2 yleisohjeistus eKampus-alustalle
## Tekoalyn luettavaksi, tekninen vientiohje

Tama ohje kasittelee vain SCORM-muotoon vientia. Ohje ei ota kantaa harjoituksen pedagogiikkaan, sisaltorakenteeseen tai ulkoasuun.

Ohjetta sovelletaan tilanteissa, joissa tekoaly tai tekninen tekija muuntaa interaktiivisen sisallon SCORM-paketiksi eKampus-alustaa varten.

## 1. Peruslinjaus

- Käytä ensisijaisesti SCORM 1.2 -pakettia.
- Toteuta jokainen suoritettava osio SCO:na.
- Pida SCORM-data minimissaan mutta oikein:
  - cmi.core.lesson_status
  - cmi.core.score.raw
  - cmi.core.score.max
  - cmi.core.score.min
- Jos tarvitset jatkamisen kesken, kayta lisa-arvoina:
  - cmi.core.lesson_location
  - cmi.suspend_data

## 2. Vahimmaisrakenne paketille

Zip-paketin juuressa on oltava:

- imsmanifest.xml
- Kaikki SCO:n avaamat HTML-, JS- ja CSS-tiedostot
- Mahdolliset media- ja datatiedostot

Tarkeaa:

- Pakkaa kansion sisalto, ei ylatasokansiota.
- Varmista UTF-8-koodaus tiedostoille.
- Varmista, etta kaikki manifestissa listatut tiedostot oikeasti ovat paketissa.

## 3. Manifesti (SCORM 1.2)

Pakolliset periaatteet:

- metadata:
  - schema = ADL SCORM
  - schemaversion = 1.2
- organizations sisaltaa opiskelijalle nakyvan SCO-rakenteen
- resources sisaltaa jokaisen SCO:n tiedostot
- Jokaiselle SCO:lle adlcp:scormtype="sco"

Suositus pistekynnykselle:

- Aseta adlcp:masteryscore item-tasolle, jos haluat yhdenmukaisen lapaisyrajan.
- Pida masteryscore linjassa cmi.core.score.raw/max -logiikan kanssa.

## 4. Erillinen valikkosivu poistetaan

Monen SCO:n paketissa erillista paketin sisaisia valikkosivua ei kayteta ensisijaisena navigointina.

Periaate:

- SCORM-soitin (eKampus SCORM-aktiviteetti) hoitaa SCO-vaihdot.
- Siirtymat tehdaan soittimen TOC:n, Seuraava/Edellinen-toimintojen tai auto-continue-asetuksen kautta.
- SCO:n sisalla ei rakenneta rinnakkaista sisallysluetteloa SCO:sta SCO:hon.

Sallittu poikkeus:

- Paikalliseen kehitykseen voi olla esikatselusivu.
- Esikatselusivua ei kayteta julkaistuna aloitus-SCO:na.
- Esikatseluresurssia ei nosteta organizations-rakenteen itemiksi.

## 5. Siirtymat usean SCO:n paketissa

SCORM 1.2 ei maarita yleispatevaa API-kutsua, jolla SCO itse avaisi varmasti seuraavan SCO:n kaikissa soittimissa.

Siksi kayta tata mallia:

1. Kun opiskelija suorittaa SCO:n:
   - aseta pisteet
   - aseta tila
   - commit
2. Sulje SCO siististi:
   - LMSFinish("")
3. Anna soittimen hoitaa seuraava SCO

Tarkeaa:

- Ala tee suoraa window.location-siirtymaa SCO:sta toiseen.
- Ala rakenna paketin sisaisia linkkeja, jotka ohittavat soittimen navigoinnin.

## 6. Yksi SCO vs monta SCO:ta

### Yksi SCO (single SCO)

Kayta kun koko suoritus on yksi tekninen kokonaisuus.

Suositus:

- Alussa lesson_status = incomplete (jos tila on not attempted)
- Paivita score.raw suorituksen aikana tai lopussa
- Lopussa aseta lesson_status = passed tai completed (riippuen arviointimallista)
- LMSFinish vasta lopussa

### Monta SCO:ta (multi SCO)

Kayta kun haluat seurata osioittain etenemista.

Suositus:

- Jokainen SCO raportoi vain oman osionsa tiedot
- Vali-SCO:t:
  - lesson_status = completed tai passed (riippuen arviointisaannosta)
- Viimeinen SCO:
  - aseta kokonaisuuden tavoitetta vastaava tila (yleensa passed, jos pistekynnys tayttyy)
- Sulje kukin SCO LMSFinish-kutsulla

Huomio:

- Jos haluat pakottaa jarjestyksen, tee se soittimen asetuksilla (esim. sequential), ei sivunsisaisilla SCO-linkeilla.

## 7. Pisteiden asetus (spec-linjassa)

SCORM 1.2:ssa pisteet raportoidaan:

- cmi.core.score.raw
- cmi.core.score.max
- cmi.core.score.min

Suositukset:

- Kayta yhtenaista asteikkoa, esim. min=0, max=100.
- Pida raw aina valilla min..max.
- Tee commit pistepaivityksen jalkeen.
- Ala merkitse passed-tilaa ennen kuin pistekriteeri oikeasti tayttyy.

## 8. Etenemistiedot ja jatkaminen

Vahimmaistaso:

- lesson_status kertoo suoritustilan.

Kun tarvitaan jatkamista kesken:

- cmi.core.lesson_location:
  - lyhyt checkpoint (esim. vaihe-id)
- cmi.suspend_data:
  - laajempi tila JSON-merkkijonona
  - SCORM 1.2:ssa pituusraja on kaytannossa noin 4096 merkkiä, joten pidä data kompaktina

Kirjoitusrytmi:

- Paivita etenemisdata merkityksellisissa checkpoint-kohdissa.
- Tee LMSCommit checkpointien jalkeen.
- Ennen sulkemista tee viimeinen commit ja LMSFinish.

## 9. Automaattiset scrollaukset ja koodin kovennukset

Tama koskee SCORM-upotettua iframe-ymparistoa.

Automaattinen scrollaus:

- Scrollaa vain SCO-dokumentin sisalla.
- Kayta paikallista window.scrollTo-logiikkaa elementin sijainnin perusteella.
- Ala scrollaa parent- tai top-ikkunaa.
- Kun fokus siirretaan inputiin, kayta preventScroll-vaihtoehtoa, jotta ulkokehys ei hyppaa.
- Kunnioita prefers-reduced-motion-asetusta, jos smooth-scroll aiheuttaa haittaa.

Koodin kovennukset (SCORM-viennin kannalta):

- Aseta completion vasta eksplisiittisessa suorituskohdassa (esim. opiskelijan vahvistus), ei liian aikaisin.
- Varmista, ettei sisaltologiikka voi merkitä suoritusta valmiiksi ennen arviointiehdon tayttymista.
- Jos tehtava vaatii kaavoja tai rakenteita, validoi muutakin kuin lopputulos (esim. estä kovakoodatut oikopolut).

## 10. SCORM 1.2 statusarvot

Sallitut keskeiset lesson_status-arvot:

- not attempted
- incomplete
- completed
- passed
- failed
- browsed

Kayta niita johdonmukaisesti:

- Aloitus: incomplete (jos aiemmin not attempted)
- Keskenerainen: incomplete
- Valmis ilman lapaisylogiikkaa: completed
- Valmis lapaistynä: passed
- Valmis hylattyna: failed

## 11. API-kutsujarjestys SCO:ssa

Suositeltu minimivirta:

1. LMSInitialize("")
2. Tarvittavat LMSSetValue-kutsut
3. LMSCommit("") checkpointien jalkeen
4. LMSFinish("") kerran SCO:n paatteeksi

Varoitukset:

- LMSInitialize vain kerran per SCO-avaus.
- LMSFinish vain kerran per SCO.
- Ala jatka LMSSetValue-kutsuja LMSFinishin jalkeen.

## 12. eKampus-asetukset (toimintamalli)

Yleiset suositukset SCORM-aktiviteetin asetuksiin:

- Sisaltorakenne (TOC) naytetaan opiskelijalle, jos paketissa on useita SCO:ja.
- Auto-continue voidaan ottaa kayttoon, jos halutaan automaattinen eteneminen SCO:n sulun jalkeen.
- Suoritusseurannan ehto valitaan niin, etta se vastaa kaytettya statuslogiikkaa (esim. passed).
- Arviointimenetelma valitaan yhtenaisesti (esim. korkein piste tai viimeisin piste) organisaation kaytannon mukaan.

## 13. Yleinen tarkistuslista ennen julkaisua

- imsmanifest.xml on zipin juuressa
- Kaikki SCO:t avautuvat
- API loytyy soittimesta ja LMSInitialize onnistuu
- score.raw/max/min paivittyvat odotetusti
- lesson_status paivittyy oikeassa vaiheessa
- checkpoint-data (location/suspend_data) palautuu oikein, jos kaytossa
- LMSFinish kutsutaan hallitusti SCO:n lopussa
- SCO-vaihdot toimivat soittimen TOC:n tai auto-continue-toiminnon kautta
- Paketti toimii ilman erillista sisäista valikkosivua

## 14. Malli tekoalykehotteeksi (yleispateva)

Kayta alla olevaa rakennetta, kun pyydat tekoalya tekemaan SCORM-viennin:

- Tee SCORM 1.2 -paketti.
- Luo imsmanifest.xml, jossa on metadata ADL SCORM 1.2.
- Mallinna sisalto [YKSI_SCO tai MONTA_SCO]-mallilla.
- Jos MONTA_SCO: poista paketin sisainen SCO-valikko ja luota soittimen TOC-siirtymiin.
- Toteuta SCORM 1.2 API-wrapper: initialize, setValue, commit, finish.
- Raportoi pisteet cmi.core.score.raw/max/min.
- Raportoi tila cmi.core.lesson_status-arvolla.
- Kayta cmi.core.lesson_location ja cmi.suspend_data vain jos jatkaminen kesken on tarpeen.
- Tee automaattiset scrollaukset vain SCO-dokumentin sisalla, ei parent-ikkunaan.
- Varmista, etta completion asetetaan vasta oikeassa suorituskohdassa.
- Tuota lopuksi julkaisukelpoinen zip, jossa imsmanifest.xml on juuressa.

---

Tama ohje on tarkoitettu yleisohjeeksi eri kurssien ja eri lahteista tulevien interaktiivisten sisaltojen SCORM-muotoon vientiin eKampus-alustalle.
