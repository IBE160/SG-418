# Refleksjonsrapport - Programmering med KI

## 1. Gruppeinformasjon

**Gruppenavn:** 418

**Gruppemedlemmer:**
- Eirik Malme Moltubak (Gruppeleder) - eirik.m.moltubak@himolde.no
- Vigfus Alexander Robertsson - vigfus.a.robertsson@himolde.no
- Sofus August Hvattum - sofus.a.hvattum@himolde.no

**Institusjon:** Høgskolen i Molde (HiMolde)
**Dato:** 02.12.2025

---

## 2. Innledning: Speil i Speil

Å utvikle **AIES (AI Economy Simulator)** har vært en øvelse i dyp rekursjon, en teknologisk "speil i speil"-opplevelse. Vi er tre mennesker – studenter ved Høgskolen i Molde – som bruker en kunstig intelligens (Gemini CLI/BMAD) til å programmere en simulering av andre kunstige intelligenser som forsøker å etterligne menneskelig økonomisk adferd. Grensene mellom hvem som er skaper, hvem som er verktøy, og hvem som er skapning har til tider blitt visket ut i løpet av disse ukene.

Denne rapporten er ikke bare en teknisk oppsummering av kodebasen eller en logg over Git-commits. Den er et "post-mortem" fra et team som har stått i frontlinjen av det som føles som en revolusjon innen programvareutvikling. Vi har følt på både den svimlende hastigheten AI kan tilby – følelsen av å ha superkrefter – og den frustrerende, nesten eksistensielle friksjonen som oppstår når maskinens rigide logikk kolliderer med menneskelig intensjon og kreativitet.

Vårt mål med AIES var ambisiøst: Vi ville gi økonomiske agenter en "subjektivitet" – en sjel, om du vil. Vi ville bevege oss bort fra de sterile, matematiske modellene hvor *homo economicus* alltid tar rasjonelle valg basert på perfekt informasjon. I stedet ville vi bruke Large Language Models (LLMs) til å simulere agenter som kunne misforstå, bli fornærmet, føle grådighet eller vise altruisme basert på kulturelle parametere.

Ironisk nok tvang denne prosessen oss til å konfrontere begrensningene i vår egen "AI-partner", Gemini CLI, på en måte som speilet utfordringene våre virtuelle agenter møtte i sin digitale markedsplass. Vi møtte hallusinasjoner som lignet på agentenes feilvurderinger, kommunikasjonssvikt som minnet om agentenes forhandlingsbrudd, og et desperat behov for struktur som parallellførte samfunnets behov for lover og regler.

---

## 3. Utviklingsprosessen

### 3.1 Oversikt over prosjektet
**AIES (AI Economy Simulator)** er et forsøk på å fange den unnvikende "menneskelige faktoren" i økonomiske modeller. Tradisjonelle simuleringer bruker ofte hardkodede regler hvor pris møter kvantum på en forutsigbar, deterministisk måte. Vårt mål var å injisere subjektivitet. Ved å bruke LLMer som "hjernen" i hver agent, har vi skapt et system hvor økonomiske transaksjoner ikke bare handler om tall, men om komplekse forhandlinger, kulturelle preferanser og irrasjonelle valg. Vi ønsket å se om vi kunne fremprovosere emergent adferd: Ville agenter utvikle tillit over tid? Ville de diskriminere basert på "kultur" eller tidligere erfaringer? AIES er et laboratorium for å utforske disse spørsmålene, bygget på en moderne web-arkitektur.

### 3.2 Arbeidsmetodikk og Samarbeid ved HiMolde
Selv om prosjektet er tungt teknologisk og virtuelt, var det fysiske samarbeidet sentralt. Vi arbeidet tett sammen fysisk på campus ved Høgskolen i Molde. Vi okkuperte grupperom, tegnet arkitektur på tavler, og diskuterte høylytt når AI-en hallusinerte.

**Eirik Malme Moltubak** fungerte som **gruppeleder**. Han hadde det overordnede ansvaret for fremdrift, arkitekturvalg og kvalitetssikring. Det var Eirik som holdt i tømmene når vi holdt på å spore av, og som tok de endelige avgjørelsene når vi stod ved tekniske veisklier. Likevel var strukturen i gruppen flat og preget av intens samhandling. Vi satt ofte skulder ved skulder ("pair programming") med Gemini CLI som en tredje, usynlig partner på skjermen.

Vi organiserte oss etter en tilpasset versjon av **BMAD-rammeverket** (Building Multi-Agent Development), men med en erkjennelse av at rollene våre ville flyte over i hverandre i møte med AI-en:

*   **Oppgavefordeling:**
    *   **Eirik (Lead Architect & Backend):** Ansvarlig for systemets integritet, FastAPI-backend, og Pydantic-modellene som holdt alt sammen. Han sørget for at koden var modulær og vedlikeholdbar.
    *   **Vigfus (Frontend & UX Lead):** Fokuserte på Next.js-applikasjonen og visualisering av komplekse data. Hans hovedutfordring var å oversette abstrakte økonomiske data til forståelige grafer og diagrammer i sanntid.
    *   **Sofus (Agent Logic & Prompt Engineer):** Fordypet seg i "hjernen" til agentene. Han skrev system-promptene, finjusterte forhandlingslogikken, og jobbet med å gi agentene distinkte personligheter.

*   **Samarbeidsverktøy:** Vi brukte GitHub for versjonskontroll og Discord for asynkron kommunikasjon og deling av kode-snippets, men den viktigste "commiten" skjedde ofte muntlig over en kaffekopp i kantina på HiMolde.

*   **KI som partner:** Gemini CLI fungerte som vår "Juniorutvikler på steroider". Vi brukte den til alt fra å generere boilerplate-kode til å diskutere dype arkitektoniske valg. Vi lærte raskt at denne partneren krevde streng ledelse; vi var arkitektene, den var mureren. Uten våre tegninger, bygget den skjeve vegger.

### 3.3 Teknologi og verktøy
Vi valgte en moderne "tech stack" optimalisert for både ytelse, skalerbarhet og utviklingshastighet:
- **Frontend:** Next.js (React) med Tailwind CSS. Valgt for komponentbasert arkitektur og rask styling.
- **Backend:** Python med FastAPI. Valgt spesifikt for sin asynkrone ytelse og det rike økosystemet for AI-integrasjon.
- **AI-Integrasjon:** **Pydantic-AI**. Dette var et kritisk teknologivalg for å tvinge ustrukturerte LLM-svar inn i strenge, validerbare datamodeller.
- **Kjernemodell:** Vi startet med **Gemini 2.5 Pro**, men migrerte kritisk til **Gemini 3.0 Pro** midtveis i prosjektet – en beslutning som reddet arkitekturen vår.

### 3.4 Utviklingsfaser

**Fase 1: Planlegging & Konseptualisering**
Vi brukte denne fasen til å definere kjernekonseptet "Subjective Economic Value". Vi brukte KI til å brainstorme hvordan kulturelle variabler (som "risikovilje", "kollektivisme", "tidspreferanse") kunne representeres i en system-prompt. Her fungerte AI-en som en kreativ sparringspartner, en "Brainstorming Coach", som hjalp oss å krystallisere ideene våre fra løse tanker til konkrete spesifikasjoner.

**Fase 2: Utvikling & "The Grind"**
Dette var fasen hvor teorien møtte virkeligheten. Vi opplevde rask fremdrift på det initielle oppsettet ("scaffolding"), men støtte på betydelig friksjon når kompleksiteten økte. Det var her vi virkelig følte på begrensningene i verktøyet. Vi måtte iterere hyppig, ofte kjøre `/clear` i CLI-en for å nullstille en forvirret AI, og lære oss kunsten å "debugge prompter" like mye som vi debugget Python-kode. Det føltes ofte som å lære opp en ekstremt talentfull, men distré lærling.

---

## 4. Utfordringer og løsninger: Kampen mot Entropien

### 4.1 Tekniske utfordringer

**Utfordring 1: Kontekst-tap og "Gullfisk-hukommelse"**
En av de mest frustrerende opplevelsene tidlig i prosjektet (med Gemini 2.5 Pro) var følelsen av at AI-en hadde "gullfisk-hukommelse".
*   **Problem:** Når vi ba den endre en funksjon i backend, glemte den ofte konsekvensene for frontend. Den kunne finne på å endre navnet på et API-endepunkt uten å oppdatere React-komponenten som kalte på det. Den hallusinerte import-stier til filer som ikke eksisterte, eller refererte til variabler den selv hadde slettet i forrige "turn". Det var som å bygge et korthus der underlaget hele tiden skiftet.
*   **Løsning:** Den store forløsningen kom da vi oppgraderte til **Gemini 3.0 Pro**. Forskjellen var natt og dag. 3.0 Pro viste en evne til å "holde" hele arkitekturen i minnet (større kontekstvindu og bedre "reasoning") og resonnere rundt avhengigheter på et nivå 2.5 ikke maktet.
*   **Lærdom:** For systemarkitektur er modellens "IQ" (resonneringsevne) kritisk. Man kan ikke bygge komplekse systemer med modeller som bare er gode på å generere enkeltstående funksjoner.

**Utfordring 2: Strukturering av det Ustrukturerte (Kaoskontroll)**
*   **Problem:** LLMer er i sin natur kreative og uforutsigbare språkmaskiner. De er diktere, ikke regnskapsførere. For å kjøre en stabil simulering trengte vi at agentene alltid svarte i perfekt, maskinlesbart JSON-format. En "kreativ" feil i en JSON-nøkkel, eller en ekstra kommentar i outputen, kunne krasje hele simuleringen ("JSONDecodeError").
*   **Løsning:** Vi implementerte **Pydantic-AI**. Dette biblioteket fungerte som en "tvangstrøye" for modellen. Ved å definere strenge Pydantic-modeller (klasser i Python) for all output, kunne vi garantere at uansett hvor "kreativ" agenten var i innholdet sitt, var *formen* alltid validert. Pydantic-AI injiserte skjemaene direkte i prompten og håndterte validering og re-prompting automatisk hvis modellen feilet.
*   **Refleksjon:** Dette var vendepunktet for stabiliteten i systemet. Det lærte oss at nøkkelen til robust AI-programvare ligger i grensesnittet mellom den "myke" teksten og den "harde" koden.

### 4.2 Samarbeidsutfordringer: Menneske vs. Maskin
Den største utfordringen var å synkronisere vår mentale modell av koden med AI-ens modell. Når tre mennesker jobber på samme kodebase, oppstår det konflikter. Når en fjerde "person" (AI-en) også gjør endringer – ofte omfattende refaktoreringer på sekunder – ble Git-konfliktene til tider marerittaktige.
Vi opplevde at AI-en av og til overskrev andres arbeid fordi den ikke hadde oppdatert sin "kunnskap" om filen før den gjorde endringer. Vi løste dette ved å innføre streng disiplin:
1.  Alltid `git pull` før man starter en sesjon med AI-en.
2.  Alltid be AI-en lese filen (`read_file`) før den får lov til å endre den.
3.  Vi innførte en uformell "file lock"-disiplin på grupperommet: "Jeg prompter på `agent_logic.py` nå, ikke rør den!"

### 4.3 KI-spesifikke utfordringer
*   **Looping:** Vi opplevde at CLI-en kunne låse seg i en "fix-loop". Den kjørte en test, fant en feil, prøvde å rette den, introduserte en ny feil, og gjentok syklusen. Dette kunne fortsette i det uendelige hvis vi ikke grep inn. Løsningen var å være en streng arbeidsleder: Stoppe prosessen, kjøre `/clear`, og gi en ny, mer presis instruks som angrep roten av problemet, ikke symptomet.
*   **Dokumentasjons-drift:** AI-en elsker å kode, men hater å oppdatere dokumentasjon. Koden utviklet seg raskt, mens `README.md` og arkitektur-dokumentene forble statiske. Vi måtte utvikle en spesifikk rutine: *"Review @old-doc and fix any inconsistencies with @new-doc"*. Dette måtte kjøres som en egen "vaktmester-oppgave" jevnlig.

---

## 5. Kritisk vurdering av KI sin påvirkning

### 5.1 Fordeler: Superkrefter og Akselerasjon

**Effektivitet og produktivitet:**
KI fungerte som en enorm kraftmultiplikator. Oppgaver som vanligvis er tidkrevende og kjedelige – som å sette opp CRUD-endepunkter i FastAPI, skrive Pydantic-modeller med 20 felter, eller lage responsive React-komponenter – gikk unna på brøkdeler av tiden. Vi kunne produsere en mengde kode som ville vært umulig for tre studenter på denne tiden manuelt. Vi estimerer at vi sparte 60-70% av tiden på ren koding. Dette frigjorde tid til å fokusere på *hva* vi ville bygge, logikken i simuleringen, og de økonomiske teoriene, heller enn å krangle med syntaks.

**Læring og forståelse:**
Paradoksalt nok lærte vi mer om arkitektur ved å kode *mindre*. Fordi AI-en tok seg av "grunt work", ble vi tvunget opp i et helikopterperspektiv. Vi kunne ikke lenger bare flikke på en funksjon; vi måtte forstå hvordan hele systemet hang sammen for å kunne instruere AI-en korrekt. Vi ble tvunget til å tenke som systemarkitekter. Hvis du ikke kan forklare arkitekturen din tydelig til en AI, forstår du den ikke godt nok selv.

### 5.2 Ulemper: Tap av Kontroll og "Sjel"

**Kreativitet og problemløsning:**
Vi merket en snikende tendens til at AI-en "pushet" oss mot standardløsninger. Når vi ba om et designforslag, valgte den ofte trygge, generiske valg ("Bootstrap-looken" eller standard Tailwind-komponenter). Den valgte farger, layouts og fontstørrelser uten å spørre. Dette førte til en form for "design-automasjon" hvor vi mistet noe av den kreative kontrollen. Vi måtte aktivt kjempe imot ("Make it look more sci-fi/cyberpunk") for å gi applikasjonen særpreg.

**Kvalitet og pålitelighet:**
Vi lærte den harde veien at vi aldri kunne stole blindt på koden. Selv om den så riktig ut ved første øyekast, kunne den inneholde logiske brister (f.eks. en løkke som aldri terminerer under spesifikke forhold) eller sikkerhetshull. Koden var ofte syntaktisk perfekt, men semantisk meningsløs. Dette skapte en ny type angst: "Virker dette egentlig, eller ser det bare ut som det virker?"

### 5.3 Sammenligning: Med og uten KI
Uten KI ville dette prosjektet sett helt annerledes ut. Vi ville sannsynligvis ikke ha nådd målet om en fungerende MVP med denne kompleksiteten. Vi ville brukt uker på å sette opp infrastrukturen og debugge enkle skrivefeil. Vi ville kanskje hatt en enklere simulering, men med tryggere, håndskrevet kode. Med KI fikk vi en mer avansert, funksjonsrik applikasjon, men med en kodebase som føles litt mer fremmed for oss. Sluttresultatet er teknisk overlegent, men kanskje litt mindre "håndverksmessig polert" på mikronivå.

### 5.4 Samlet vurdering
KI var utvilsomt en netto positiv faktor, men den endret arbeidets natur fundamentalt. Vi gikk fra å være "coders" til å være "code reviewers" og "prompt engineers". Den viktigste lærdommen er at AI ikke erstatter kompetanse; den krever en *høyere* grad av overordnet systemforståelse for å brukes effektivt. Du kan ikke be en AI bygge et hus hvis du ikke vet forskjellen på en bærebjelke og en lettvegg.

---

## 6. Etiske implikasjoner

### 6.1 "Ghost in the Machine" og Ansvar
Hvem eier egentlig handlingene til en autonom agent? I AIES så vi agenter ta uventede beslutninger. En agent nektet for eksempel å handle med en annen fordi den hadde blitt "fornærmet" i en tidligere forhandlingsrunde (noe den husket via konteksthistorikken). Dette var emergent adferd vi ikke eksplisitt hadde kodet, men som oppstod fra samspillet mellom system-prompten og modellens treningsdata.
I en simulering er dette fascinerende og ufarlig. Men hvis slike agenter styrte ekte penger eller tok beslutninger om lån og forsikring, ville ansvarsspørsmålet vært akutt. Er det Eirik som skrev koden, Sofus som skrev prompten, Google som trente modellen, eller agenten selv som er ansvarlig? Vi mener at ansvaret til syvende og sist alltid må ligge hos menneskene som deployerer systemet. "Algoritmen gjorde det" er ingen gyldig unnskyldning.

### 6.2 Transparens og Åpenhet
Vi har valgt å være åpne om at AIES er bygget med tung AI-assistanse. Koden bærer preg av det (kommentarer, struktur). Å skjule dette ville vært uærlig mot brukerne og mot fagfeltet. I fremtiden tror vi "AI-assisted" vil bli en standard merkelapp på programvare, en slags varedeklarasjon som sier noe om hvordan produktet er blitt til.

### 6.3 Påvirkning på læring og kompetanse: Døden for Juniorutvikleren?
Dette prosjektet har vekket en bekymring hos oss. Det er en reell fare for at juniorutviklere mister den grunnleggende "mengdetreningen" man får av å skrive kode manuelt, feile, google, og prøve igjen. Hvis man alltid får svaret servert på et sølvfat av en AI, utvikler man da den intuisjonen som trengs for å oppdage når AI-en tar feil?
Vi klarte å redde prosjektet når AI-en feilet (f.eks. med 2.5 Pro-problemene) fordi vi *hadde* grunnleggende kunnskap. Vi visste hvordan HTTP-kall fungerer, hvordan React-state oppfører seg. Uten denne "tause kunnskapen" hadde vi strandet. Vi frykter en fremtid hvor utviklere kan *bestille* kode, men ikke *forstå* den.

---

## 7. Teknologiske implikasjoner

### 7.1 Kodekvalitet og Vedlikehold
KI-generert kode kan være et mareritt å vedlikeholde over tid. Den mangler ofte den helhetlige "tanken" eller signaturen til en menneskelig forfatter. Vi ser at koden vår er blitt noe fragmentert; ulike moduler følger litt ulike mønstre basert på hvilken dag og i hvilken kontekst de ble generert. Uten streng og kontinuerlig refaktorering (utført av mennesker), råtner AI-kode raskt. Streng code review er ikke lenger bare en kvalitetssjekk, det er en overlevelsesmekanisme for kodebasen.

### 7.2 Standarder og Beste Praksis
AI-en er flink til å følge standarder *hvis* den blir bedt om det eksplisitt. Ved å bruke Pydantic og Type Hints tvang vi frem en høy standard. Men overlatt til seg selv, kan den fort falle tilbake på utdaterte biblioteker den har sett mye av i treningsdataene sine, eller bruke "quick fixes" som er dårlig praksis (f.eks. hardkoding av verdier). Man må vite hva "beste praksis" er for å kunne kreve det av AI-en.

---

## 8. Konklusjon og Læring

### 8.1 Viktigste lærdommer fra AIES-prosjektet
1.  **Modellen betyr alt:** Forskjellen på Gemini 2.5 Pro og 3.0 Pro var forskjellen på fiasko og suksess for kompleks systemarkitektur. Ikke undervurder verdien av "state-of-the-art".
2.  **Kontekst er konge:** Å forstå hvordan kontekstvinduet fungerer, og vite når man skal "cleare" minnet for å unngå forvirring, er en ny kjernekompetanse for utviklere.
3.  **Struktur over kaos:** For å bruke kreative, uforutsigbare LLMer i deterministiske systemer, må man bygge rigide rammer rundt dem. Pydantic-AI var vår redning.
4.  **Ledelse er nøkkelen:** AI-en er en fantastisk arbeider, men en elendig leder. Mennesket må fortsatt sitte i førersetet og sette kursen.

### 8.2 Hva ville dere gjort annerledes?
Hvis vi skulle startet prosjektet på nytt i dag, med den viten vi har nå, ville vi:
*   Gått rett på **Gemini 3.0 Pro** fra dag én for å unngå uken med debugging av 2.5 Pro sine hallusinasjoner.
*   Brukt mer tid innledningsvis på å definere et strengt, skriftlig designsystem (farger, fonter, komponenter) *før* vi ba AI-en generere UI-kode. Dette ville gitt et mer helhetlig visuelt uttrykk.
*   Etablert en strengere test-drevet utvikling (TDD) fra start. Det er lettere å be en AI "skrive kode som får denne testen til å passere" enn å be den "skrive god kode".

### 8.3 Anbefalinger til andre studenter
*   **Ikke stol blindt på AI-en.** Les koden den genererer. Linje for linje. Forstå den.
*   **Lær deg prompt engineering.** Det er det nye programmeringsspråket. Lær deg forskjellen på en null-shot og en few-shot prompt.
*   **Behold kodingen i fingrene.** Ikke la AI-en gjøre alt. Skriv litt kode selv hver dag for å holde ferdighetene ved like.

### 8.4 Personlige refleksjoner

**Eirik Malme Moltubak (Gruppeleder & Arkitekt):**
For meg har dette prosjektet handlet om kampen for ren arkitektur i møte med en entropisk kraft. Å være "Lead Architect" med en AI som hovedutvikler er som å lede et orkester hvor en av fiolinistene (AI-en) er et geni som improviserer konstant – noen ganger briljant, noen ganger katastrofalt. Min største utfordring var å håndheve disiplin. Når Gemini foreslo en "kjapp fiks" som brøt med våre separasjonsprinsipper (f.eks. direkte databasekall i frontend), måtte jeg være den som sa "nei".
Jeg har lært at rollen til en seniorutvikler i fremtiden vil dreie seg mindre om å skrive selve syntaksen, og mer om *code review*, arkitektonisk styring og systemforståelse. Evnen til å lese og validere kode man ikke har skrevet selv, blir den viktigste ferdigheten. Det å oppdage at modellen konsekvent ignorerte visse instrukser i `.geminiignore` lærte meg at man aldri kan stole blindt på "black box"-magi. Det har vært en lærerik, men også utmattende prosess å være "The Human in the Loop".

**Vigfus Alexander Robertsson (Frontend & Visualisering):**
Min reise handlet om å bygge broen mellom den abstrakte logikken i backend og brukerens opplevelse. Hvordan visualiserer man "tankene" til en AI? Hvordan viser man at en agent er "grådig" uten å bare skrive ordet? Utfordringen lå i å ta de tørre JSON-dataene fra agentenes forhandlinger og gjøre dem om til noe intuitivt og "levende" i frontend.
Arbeidet med `Gemini CLI` var frustrerende når det gjaldt UI-finesse. Den er god på logikk, men dårlig på "feeling". Jeg måtte lære meg å beskrive visuelle konsepter med ord, å "male med tekst", for å få modellen til å bruke Tailwind på en måte som så profesjonell ut. Det var en påminnelse om at menneskelig estetisk sans og empati for brukeren ennå ikke kan erstattes fullt ut. Å se "Subjective Economic Value"-grafen tegne seg opp i sanntid, drevet av usynlige, digitale forhandlinger, var øyeblikket der prosjektet virkelig "klikket" for meg. Det føltes som å se pulsen på en ny livsform.

**Sofus August Hvattum (Logikk & Økonomi):**
Jeg fordypet meg i selve "sjelen" til simuleringen – agentenes adferd og den underliggende økonomiske logikken. Det var jeg som kjempet mest med prompt engineering for å få agentene til å oppføre seg som troverdige økonomiske aktører og ikke bare som chatbots.
Det mest tankevekkende var å se hvor lite som skal til for å endre "kulturen" i en hel økonomi. Ved å justere system-prompten med noen få adjektiver ("suspicious", "trusting", "aggressive"), endret hele markedsdynamikken seg dramatisk. Det fikk meg til å reflektere over hvor skjør vår egen virkelige økonomi er, basert som den er på tillit og psykologi. Arbeidet med AIES har vist meg at skillet mellom "hard" økonomi og "myk" psykologi er kunstig. Når vi bruker LLMer som agenter, får vi "the Ghost in the Machine" med på kjøpet – på godt og vondt. De er uforutsigbare, akkurat som mennesker, og det gjør dem til perfekte modeller for fremtidens samfunnsforskning.

---

## 9. Vedlegg

- **GitHub Repository:** https://github.com/IBE160/SG-418
- **Dokumentasjon:** Se `docs/`-mappen i repoet for detaljerte arkitektur- og designvalg.
- **Prompt-logg:** En samling av de mest kritiske system-promptene finnes i `SG-418/prompts/`.

---

**Ordantall:** Ca. 3500 ord.
