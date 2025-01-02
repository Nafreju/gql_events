U N I V E R Z I T A   O B R A N Y
Fakulta vojenských technologií, Katedra informatiky a kybernetických operací



ZÁPOČTOVÁ PRÁCE (ZP)
Analýza informačních zdrojů (IZ)

UML modelování
Slovník kybernetické bezpečnosti


Týmová práce
Zpracoval:	Tým 3: Michal Bureš, Nikola Sedláčková, Raymond Whitehead
Datum:	2.1.2025
 
Obsah
Seznam obrázků	2
Seznam tabulek	2
1. Popis struktur Událostí	3
2. Use case Výuka	5
3. Use case Meeting	6
4. Class diagram Event	8
5. Rozvoj slovníku kybernetické bezpečnosti	9
6. Závěr	10
Seznam obrázků
Obrázek 1 use case výuka	6
Obrázek 2 use case meeting	7
Obrázek 3 class Event	9

Seznam tabulek 
Tabulka 1 Přidělené pojmy slovníku	3

 
1. Popis struktur Událostí
Events v nově vytvářeném informačním systému reprezentují jakékoliv reálné události, které jsou součástí života na Univerzitě obrany. Například díky tomuto modulu lze v systému reprezentovat hodiny výuky, slavnostní vyřazení, státní závěrečné zkoušky, zkoušky z předmětu. Hlavním modulem, od kterého se odvíjí ostatní moduly, je EventModel. Každá událost v informačním systému má svůj určitý typ, který je samostatným modelem EventTypeModel. Například, pokud má student v rozvrhu seminář v rámci předmětu Analýza informačních zdrojů, tak název události je stejný jako název předmětu a typ události neboli eventtype je SEM. Zároveň jelikož je předmět součástí semestru, tak Event má svoji nadřazenou událost, klíč masterevent, který má v tomto případě druh události určen jako Semestr.
Každý model v systému musí být vytvořitelný, upravitelný, editovatelný i smazatelný (invalidní).
Níže je vypsán seznam modelů a jejich atributů.

EventModel
-	Účel: Reprezentuje událost
-	Atributy:
o	id – UUID – unikátní identifikátor
o	name – název události v češtině
o	name_en – název události v angličtině
o	valid – událost smazat nelze – je cizím klíčem jiných
o	created – datum a čas vytvoření události
o	lastchange – datum a čas poslední změny události
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil událost
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil událost
o	startdate – datum a čas začátku události
o	enddate – datum a čas konce události
o	masterevent_id – cizí klíč, odkazující na nadřazenou událost, ke které tato událost patří
o	eventtype_id – cizí klíč, odkazující na typ události
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva

EventTypeModel
-	Účel: Reprezentuje typ události
-	Atributy:
o	id – UUID – unikátní identifikátor
o	name – název typu události v češtině
o	name_en – název typu události v angličtině
o	valid – boolean, indikuje, zda je typ události smazán nebo ne
o	created – datum a čas vytvoření typu události
o	lastchange – datum a čas poslední změny typu události
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil typ události
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil typ události
o	category_id – cizí klíč na kategorii událostí, ke které typ patří
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	events – vztah, který definuje seznam událostí tohoto typu (vztah k EventModel)
o	category – vztah, který definuje kategorii tohoto typu události (vztah k EventCategoryModel)

EventCategoryModel
-	Účel: Reprezentuje kategorii událostí
-	Atributy: 
o	id – UUID – unikátní identifikátor
o	name – název kategorie události v češtině
o	name_en – název kategorie události v angličtině
o	valid – boolean, indikuje, zda je kategorie události smazána nebo ne
o	created – datum a čas vytvoření kategorie události
o	lastchange – datum a čas poslední změny kategorie události
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil kategorii události
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil kategorii události
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	eventtypes – vztah k modelu EventTypeModel, který definuje seznam typů událostí spadajících do této kategorie.

EventGroupModel
-	Účel: Reprezentuje vztah mezi událostí a skupinou typu N:N
-	Atributy: 
o	id – UUID – unikátní identifikátor
o	event_id – cizí klíč odkazující na událost, která je přiřazena ke skupině
o	group_id – UUID cizí klíč odkazující na skupinu, která je přiřazena k události
o	created – datum a čas vytvoření záznamu
o	lastchange – datum a čas poslední změny záznamu
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil záznam
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil záznam
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	event – vztah k modelu EventModel, který odkazuje na přiřazenou událost
o	group – komentovaný vztah k modelu GroupModel, který by odkazoval na přiřazenou skupinu (zatím zakomentováno)

InvitationTypeModel
-	Účel: Reprezentuje typ pozvánky na událost
-	Atributy:
o	id – UUID – unikátní identifikátor
o	name – název typu pozvánky na událost v češtině
o	name_en – název typu pozvánky na událost v angličtině
o	valid – boolean, indikuje, zda je typ pozvánky smazán nebo ne
o	created – datum a čas vytvoření typu pozvánky
o	lastchange – datum a čas poslední změny typu pozvánky
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil typ pozvánky
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil typ pozvánky
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	presences – vztah k modelu PresenceModel, který definuje přítomnosti podle typu pozvánky

PresenceModel
-	Účel: Reprezentuje vztah mezi událostí a uživatelem, včetně informací o přítomnosti a typu pozvánky
-	Atributy:
o	id – UUID – unikátní identifikátor
o	event_id – cizí klíč odkazující na událost, která je přiřazena uživateli
o	user_id – UUID cizí klíč odkazující na uživatele přiřazeného k události
o	invitationtype_id – cizí klíč odkazující na typ pozvánky, který byl přiřazen uživateli pro danou událost
o	presencetype_id – cizí klíč odkazující na typ přítomnosti, který byl přiřazen uživateli pro danou událost
o	created – datum a čas vytvoření záznamu
o	lastchange – datum a čas poslední změny záznamu
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil záznam
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil záznam
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	event – vztah k modelu EventModel, který odkazuje na událost přiřazenou uživateli
o	invitationtype – vztah k modelu InvitationTypeModel, který odkazuje na typ pozvánky přiřazený uživateli
o	presencetype – vztah k modelu PresenceTypeModel, který odkazuje na typ přítomnosti uživatele na události

PresenceTypeModel
-	Účel: Reprezentuje typ přítomnosti uživatele na události
-	Atributy:
o	id – UUID – unikátní identifikátor
o	name – název typu přítomnosti (např. přítomen, dovolená)
o	name_en – název typu přítomnosti v angličtině
o	valid – boolean, indikuje, zda je typ přítomnosti smazán nebo ne
o	created – datum a čas vytvoření záznamu
o	lastchange – datum a čas poslední změny záznamu
o	createdby – UUID cizí klíč, identifikátor uživatele, který vytvořil typ přítomnosti
o	changedby – UUID cizí klíč, identifikátor uživatele, který změnil typ přítomnosti
o	rbacobject – UUID cizí klíč na uživatele nebo skupinu určující přístupová práva
o	presences – vztah k modelu PresenceModel, který definuje přítomnosti podle tohoto typu přítomnosti
2. Use case Výuka

 
Obrázek 1 use case výuka
Aktéři: 
1.	Organizátor: Osoba, která zahajuje, plánuje a stanovuje výuku (může jít o profesora, vedoucího katedry nebo administrátora).
2.	Student: Každý student univerzity, který se účastní výuky.
3.	Systém: Software nebo systém, který automatizuje změny v rozvrhu výuky.
4.	Garant předmětu: Osoba, vysokoškolský pedagog, který zodpovídá za zajištění výuky konkrétního předmětu.
Případy užití: 
1.	Zobrazit rozvrh – Umožňuje zobrazit jednotlivé předměty v rámci dne, týdne nebo měsíce pro studenta, organizátora nebo garanta předmětu.
2.	Zobrazit výuku – Umožňuje zobrazit jednotlivý předmět v rámci dne, týdne nebo měsíce pro studenta, organizátora nebo garanta předmětu.
3.	Zapsat se na výuku – Umožňuje studentovi přihlásit se na výuku. 
4.	Odhlásit se z výuky – Umožňuje studentovi odhlásit se z výuky.
5.	Naplánovat výuku – Organizátor zahájí plánování nové výuky.
6.	Upravit výuku – Umožňuje organizátorovi nebo garantovi předmětu změnit čas, datum, místo výuky.
7.	Aktualizace výuky – Umožňuje systému provést změny v systému a zobrazit nejaktuálnější informace o výuce.
8.	Zrušit výuku – Organizátor nebo garant předmětu může zrušit naplánovanou výuku, pokud je to nutné.
3. Use case Meeting
 
Obrázek 2 use case meeting
Aktéři
1.	Organizátor: Osoba, která zahajuje, plánuje a stanovuje program schůzky (může jít o profesora, vedoucího katedry nebo administrátora).
2.	Účastník: Každý, kdo se účastní schůzky, například student, profesor, externí host nebo jiní členové univerzity.
3.	Podpůrný personál: Zajišťuje logistické a technické aspekty schůzky, jako je rezervace místností, zasílání připomínek a technická podpora.
4.	Systém: Software nebo systém, který automatizuje akce jako zasílání připomínek

Případy užití
1.	Naplánovat schůzku: Organizátor zahájí plánování nové schůzky.
2.	Zrušit schůzku: Organizátor nebo podpůrný personál může zrušit naplánovanou schůzku, pokud je to nutné.
3.	Upravit podrobnosti schůzky: Umožňuje organizátorovi nebo podpůrnému personálu změnit čas, datum, místo nebo seznam účastníků schůzky.
4.	Odeslat připomenutí: Systém nebo podpůrný personál zasílá připomínky účastníkům ohledně nadcházejících schůzek.
5.	Připojit se ke schůzce: Účastníci se připojí k osobní nebo online schůzce.
6.	Stanovit program schůzky: Organizátor stanoví a sdílí program schůzky.
7.	Technická podpora: Podpůrný personál poskytuje technickou pomoc pro virtuální schůzky (např. řešení problémů s připojením).
8.	Pozvat externího hosta: Organizátor může pozvat externího hosta k účasti na schůzce.
9.	Požádat o schůzku: Účastník může požádat o schůzku s organizátorem, například pro účely poradenství nebo projektové konzultace.
10.	Potvrdit účast: Účastníci potvrzují svou účast na schůzce.
11.	Odeslat zpětnou vazbu ke schůzce: Účastníci mohou po skončení schůzky poskytnout zpětnou vazbu, aby zlepšili budoucí schůzky.
4. Class diagram Event
Diagram tříd reprezentuje Událost v systému. Třídy obsahují atributy zmíněné výše. Každá třída má atributy changed by a created by, které odkazují na uživatele, který dané akce provedl. Třídy User a Group jsou součástí řešení jiného týmu a implementaci jsou označeny jako tzv. federační třídy. Z tohoto důvodu jsou ponechány prázdné.
 
Obrázek 3 class Event
5. Rozvoj slovníku kybernetické bezpečnosti 
Pojmy ze zadání zmíněné v následující tabulce ve sloupci Concept ENG byly doplněny do Slovníku kybernetické bezpečnosti (Cyber Security Glossary) pod přihlášeným uživatelem Team03.
5.1 Přidělené pojmy týmu 1
Poř	Area	Concept ENG	Počet DEFINIC	Datum splnění
1	8	Blockchain Security	 3	 17.12.2024
2	8	Blue teaming	 3	 17.12.2024
3	1	Bring your own device (BYOD)	 3	 19.12.2024
4	1	Bug	 3	 17.12.2024
5	4	Campaign	 1	 19.12.2024
6	9	CAPTCHA	 3	 17.12.2024
7	6	Cleartext Transmission of Sensitive Information	 1	 17.12.2024

6. Závěr
6.1 Zhodnocení a závěr UML modelování
Na základě zadání zápočtové práce do předmětu Analýza informačních zdrojů byly vytvořeny diagramy případu užití pro výuku a schůzku. Dále byl doplněn diagram tříd události, která tvoří stěžejní část informačního systému korespondující s reálnými událostmi v prostředí Univerzity obrany. Dále byly diagramy doplněny do repozitáře https://github.com/Nafreju/gql_events/tree/main.
6.2 Zhodnocení a závěr doplňování slovníku
Na základě zadání zápočtové práce do předmětu Analýza informačních zdrojů byly do Slovníku kybernetické bezpečnosti (Cyber Security Glossary) doplněny pojmy pod přihlášeným uživatelem Team03. Navzdory tomu, že při víceslovném pojmenování byl nalezen pouze jeden zdroj, nedošlo k rozšíření zdrojů slovníku, nýbrž byly využity již zdroje existující.



 

