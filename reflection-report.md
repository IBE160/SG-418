# Refleksjonsrapport - Programmering med KI

## 1. Gruppeinformasjon

**Gruppenavn:** 418

**Gruppemedlemmer:**
- Eirik Malme Moltubak - 252105/eirik.m.moltubak@himolde.no
- Vigfus Alexander Robertsson - 250082/vigfus.a.robertsson@himolde.no
- Sofus August Hvattum - 252103/sofus.a.hvattum@himolde.no

**Dato:** 05.12.2025

---

## 2. Utviklingsprosessen

### 2.1 Oversikt over prosjektet
**AIES (AI Economy Simulator)** er et forsøk på å fange den unnvikende "menneskelige faktoren" i økonomiske modeller. Tradisjonelle simuleringer bruker ofte hardkodede regler hvor pris møter kvantum på en forutsigbar, deterministisk måte. Vårt mål var å injisere subjektivitet. Ved å bruke LLMer som "hjernen" i hver agent, har vi skapt et system hvor økonomiske transaksjoner ikke bare handler om tall, men om komplekse forhandlinger, kulturelle preferanser og irrasjonelle valg. Vi ønsket å se om vi kunne fremprovosere emergent adferd: Ville agenter utvikle tillit over tid? Ville de diskriminere basert på "kultur" eller tidligere erfaringer? AIES er et laboratorium for å utforske disse spørsmålene, bygget på en moderne web-arkitektur.

### 2.2 Arbeidsmetodikk
Selv om prosjektet er tungt teknologisk og virtuelt, var det fysiske samarbeidet sentralt. Vi arbeidet tett sammen fysisk på campus ved Høgskolen i Molde. Vi okkuperte grupperom, tegnet arkitektur på tavler, og diskuterte høylytt når AI-en hallusinerte.

**Eirik Malme Moltubak** fungerte som **gruppeleder**. Han hadde det overordnede ansvaret for fremdrift, arkitekturvalg og kvalitetssikring. Det var Eirik som holdt i tømmene når vi holdt på å spore av, og som tok de endelige avgjørelsene når vi stod ved tekniske veisklier. Likevel var strukturen i gruppen flat og preget av intens samhandling.

Vi organiserte oss etter en tilpasset versjon av **BMAD-rammeverket** (Breakthrough Method for Agile Ai Driven Development), men med en erkjennelse av at rollene våre ville flyte over i hverandre i møte med AI-en:

*   **Oppgavefordeling:**
    *   **Eirik (Prompt Master & Project Lead):** Hadde det overordnede ansvaret for prosjektets fremdrift, arkitekturvalg og kvalitetssikring. Med bakgrunn fra egeninteresse for KI og erfaring fra flere praksisprosjekter, tok Eirik en ledende rolle i å koordinere samarbeidet og prompte Gemini CLI. Han overvåket alle viktige beslutninger rundt arkitektur og implementasjon, og sørget for at både menneskelige og KI-genererte bidrag holdt høy kvalitet. Han var hovedansvarlig for prompt engineering-strategien, testet ulike tilnærminger for å «styre» KI-en trygt inn mot riktige og reproduserbare svar, og tilpasset instruksjonene for å sikre at modellene forsto prosjektets formål og rammer. I tillegg hadde han ansvar for overordnet rapportering og prosjektstyring.

    *   **Vigfus (Teknisk Feasibility & KI-Kvalitetssikring):** Hadde hovedansvaret for å sikre prosjektets tekniske gjennomførbarhet (feasibility) og robusthet. Basert på tidligere erfaring fra Brunvoll og IT-linja på Romsdal VGS, bidro han med tidlig risikovurdering og overordnet teknisk tenkning for å validere arkitekturvalgene. Han fungerte som gruppens kritiske KI-reviewer, og brukte sin erfaring med KI-verktøy til å nøye se over koden AI-en leverte for å avdekke logiske feil og brudd på beste praksis. I tillegg bidro han vesentlig til prompt engineering-arbeidet, spesielt med fokus på å strukturere instruksjonene for å oppnå forutsigbare og korrekte resultater fra språkmodellene.

    *   **Sofus (Idémyldring & Agentlogikk):** Sofus tok en sentral lederrolle under idémyldringen, hvor han initierte og ledet mange av diskusjonene som definerte prosjektets retning og konsept. Hans evne til å utfordre etablerte ideer bidro til å løfte ambisjonsnivået i startfasen. Han finjusterte forhandlingslogikken. Sofus hadde også ansvar for å sikre samsvar mellom agentenes atferd og prosjektets grunnidé – at subjektivitet skulle skinne gjennom i simuleringen.

    Bortsatt fra hovedområdene var arbeidsfordelingen flat, da vi for det meste jobben sammen fysisk på én PC da rammeverket er lineært fram til utviklingen.

*   **Samarbeidsverktøy:** Vi brukte GitHub for versjonskontroll og Discord for asynkron kommunikasjon og planlegging, men de viktigste "commitene" skjedde fysisk på grupperom på HiMolde.

*   **KI som partner:** Gemini CLI med BMAD-rammeverket fungerte som vår Analyst, Project Manager, UX Designer, Architect, Scrum-Master, Developer og Brainstorming Assistant i ett. Vi brukte den til alt fra å generere boilerplate-kode til å diskutere dype arkitektoniske valg. Vi lærte raskt at denne partneren krevde streng ledelse; vi var arkitektene, den var mureren. Uten våre tegninger, bygget den skjeve vegger.

### 2.3 Teknologi og verktøy
Vi valgte en moderne "tech stack" optimalisert for både ytelse, skalerbarhet, utviklingshastighet, og ikke minst KI-kompatibelhet. Vi hadde kunnskap fra før om hvilke språk og libs LLMer er best (mest trent) og valgte derfor:
- **Frontend:** Next.js (React) med Tailwind CSS. Valgt for komponentbasert arkitektur og rask styling.
- **Backend:** Python med FastAPI. Valgt spesifikt for sin asynkrone ytelse og det rike økosystemet for AI-integrasjon.
- **Database:** Ingen. Database ble valgt bort pga. manglende behov og for å unngå unødvendig komplikasjon.
- **AI-Integrasjon:** Pydantic-AI. Dette var et kritisk teknologivalg for å tvinge ustrukturerte LLM-svar inn i strenge, validerbare datamodeller.
- **Kjernemodell:** Vi startet med **Gemini 2.5 Pro**, men migrerte kritisk til **Gemini 3.0 Pro** så snart den kom ut gjennom et tilbud om gratis prøvemåned – en beslutning som reddet prosjektet og tålmodigheten vår.
- **KI-verktøy:** Gemini CLI
- **Andre verktøy:** VS Code/Cursor, BMAD

### 2.4 Utviklingsfaser

**Fase 1: Discovery**
Vi lagde Proposal, brainstormet, gjorde research og lagde Project Brief ved å følge BMAD-rammeverket. Vi instruerte KI, men tok selv endelige beslutninger og fulgte Gemini tett opp. 

Vi brukte denne fasen til å definere kjernekonseptet "Subjective Economic Value". Vi brukte KI til å brainstorme hvordan kulturelle variabler (som "risikovilje", "kollektivisme", "tidspreferanse") kunne representeres i en system-prompt. Her fungerte AI-en som en kreativ sparringspartner, en "Brainstorming Coach", som hjalp oss å krystallisere ideene våre fra løse tanker til konkrete spesifikasjoner.

Promptene og de spesifikke stegene finnes i filene som ble automatisk logget da de er for lange til å inkludere her (se vedlegget for prompting under fase_1).

**Fase 2: Planning**
Vi lagde PRD og UX gjennom BMAD-rammeverket. Vi fikk store problemer med å få PRD til å være i riktig format og samsvare med de tidligere dokumentene. Vi fikk også store problemer med UX-designer, da den stoppet etter første steg. Vi fikk ikke 2.5 Pro til å fortsette der den slapp, men 3.0 Pro klarte dette nesten umiddelbart og reddet oss fra å være stuck lenge. PRD-en så vi delvis gjennom, mens vi valgte UX-farge ut ifra KI-ens forslag. UX-type (design direction) valgte Gemini selv, men vi var fortrolig med valgte, så vi gjorde ikke om på det.

Promptene og de spesifikke stegene finnes i filene som ble automatisk logget da de er for lange til å inkludere her (se vedlegget for prompting under fase_1).

**Fase 3: Solutioning**
Vi lagde Architecture, Epics og kjørte en Implementation Readiness sjekk. Dette gjorde vi helt uten å se gjennom filene som ble produsert, da vi hadde byttet til Gemini 3.0 Pro og fant at den var mye mer pålitelig. Vi hadde også behov for å bli fort ferdig med denne delen slik at vi hadde mer å skrive om i refleksjonrapporten.

Promptene og de spesifikke stegene finnes i filene som ble automatisk logget da de er for lange til å inkludere her (se vedlegget for prompting under fase_1).

**Fase 4: Utvikling**
Ikke påbegynt.

---

## 3. Utfordringer og løsninger

### 3.1 Tekniske utfordringer

**Utfordring 1: Strukturering av det Ustrukturerte (Kaoskontroll)**
*   **Problem:** LLMer er i sin natur kreative og uforutsigbare språkmaskiner. De er diktere, ikke regnskapsførere. For å kjøre en stabil simulering trengte vi at agentene alltid svarte i perfekt, maskinlesbart JSON-format. En "kreativ" feil i en JSON-nøkkel, eller en ekstra kommentar i outputen, kunne krasje hele simuleringen ("JSONDecodeError").
*   **Løsning:** Vi implementerte **Pydantic-AI**. Dette biblioteket fungerte som en "tvangstrøye" for modellen. Ved å definere strenge Pydantic-modeller (klasser i Python) for all output, kunne vi garantere at uansett hvor "kreativ" agenten var i innholdet sitt, var *formen* alltid validert. Pydantic-AI injiserte skjemaene direkte i prompten og håndterte validering og re-prompting automatisk hvis modellen feilet.
*   **KI sin rolle:** Gemini hjalp oss med research for å finne tak i løsninger på problemet. Vi endte opp med den flotte løsningen Pydantic-AI på grunn av KI sin kunnskap.

**Utfordring 2: Innstallering**
*   **Problem:** Innstallering av Gemini-CLI og andre nødvendige programmer på Sofus sin Windows-maskin var svært problematisk. Vi fikk igjen og igjen error under installeringen av NodeJS og NPM.
*   **Løsning:** Løsningen ble til slutt å samles fysisk slik at han kunne jobbe med prompting uten å selv ha CLI innstallert.
*   **KI sin rolle:** Vi ga KI-en errorkoden flere ganger. Først, ga den oss tips om ulike kommandoer og generelle debugging-tips vi kunne gjøre. Uten KI hadde dette tatt mye lenger tid. Etter vi hadde gjort alle tipsene den hadde, kom vi til slutt til et punkt hvor KI-en fant noe viktig i error-koden: Sofus hadde ikke nok ledig plass til å innstallere CLI.

### 3.2 Samarbeidsutfordringer
Vi slet i begynnelsen med å fokusere når vi jobbet sammen online. Vi løste dette ved å bestemme oss for å heller møtes fysisk på HiMolde. Det ble til tider vanskelig å finne tidspunkt når alle var ledige til å jobbe fysisk, men vi løste dette med å legge planer lenger frem i tid og være aktiv på vår kommunikasjonsplatform Discord.

### 3.3 KI-spesifikke utfordringer
*   **Looping:** Vi opplevde at CLI-en kunne låse seg i en "fix-loop". Den kjørte en test, fant en feil, prøvde å rette den, introduserte en ny feil, og gjentok syklusen. Dette kunne fortsette i det uendelige hvis vi ikke grep inn. Løsningen var å være en streng arbeidsleder: Stoppe prosessen, kjøre `/clear`, og gi en ny, mer presis instruks som angrep roten av problemet, ikke symptomet.
*   **Gullfisk-hukommelse:** Den hallusinerte stier til filer som ikke eksisterte, eller lagde nye dokumenter som ikke var i samsvar med de tidligere. Det var som å bygge et korthus der underlaget hele tiden skiftet. Den store forløsningen kom da vi oppgraderte til **Gemini 3.0 Pro**. Forskjellen var natt og dag. 3.0 Pro viste en evne til å "holde" hele arkitekturen i minnet og resonnere rundt avhengigheter på et nivå 2.5 ikke maktet. Før vi fikk byttet til 3.0 Pro var løsningen å alltid referere direkte til de viktigste tidligere dokumentene (@old_doc.md) og gå flere runder med KI-en etter den hadde laget dokumentet, hvor vi sjekket at alt stemte med tidligere dokumentasjon. For eksempel repeterte vi "Fix all inconsistencies with @old_doc.md and @new_doc.md by updating @new_doc.md" og "/clear" helt til KI-en bare fant små rettskrivingsfeil flere ganger på rad.

---

## 4. Kritisk vurdering av KI sin påvirkning

### 4.1 Fordeler med KI-assistanse

**Effektivitet og produktivitet:**
KI fungerte som en enorm kraftmultiplikator. Oppgaver som vanligvis er tidkrevende og kjedelige – som å brainstorme, lage UX design og PRD – gikk unna på brøkdeler av tiden. Kunnskapen vi hadde om dette var i tillegg svært begrenset, men med KI ble det etter vår forståelse veldig bra.

**Læring og forståelse:**
Paradoksalt nok lærte vi mer om arkitektur ved å kode *mindre*. Fordi AI-en tok seg av "grunt work", ble vi tvunget opp i et helikopterperspektiv. Vi kunne ikke lenger bare flikke på en funksjon; vi måtte forstå hvordan hele systemet hang sammen for å kunne instruere AI-en korrekt. Vi ble tvunget til å tenke som systemarkitekter. Hvis du ikke kan forklare arkitekturen din tydelig til en AI, forstår du den ikke godt nok selv. Ved å bruke AI til lette, men tunge oppgaver (som refactoring) kunne vi bruke med tid på å lære. 

**Kvalitet på koden:**
Siden vi ikke rakk å begynne på selve utviklingsdelen har vi ikke fått sett på dette konkret. Likevel kan vi trekke konklusjoner fra prosjektdokumentasjonen og arbeidet KI produserte. KI genererte som regel gode utkast og forslag som traff hovedlinjene i våre idéer, men det var også synlig at kvaliteten ikke alltid var på toppnivå. For eksempel leverte Gemini 2.5 Pro flere flotte designforslag i ux-design-directions.html, men klarte ikke å lage en fungerende dropdown hvor alle alternativer var tilgjengelige. Feilen ble først rettet da vi gikk over til Gemini 3.0 Pro, som løste utfordringen uten problemer. Dette gir oss en indikasjon på at koden KI-en genererer kan være varierende i kvalitet og avhengig av modellens modenhet.

### 4.2 Begrensninger og ulemper

**Kvalitet og pålitelighet:**
Her så vi tydelige svakheter med AI-generert innhold, særlig med eldre modellversjoner. Et konkret eksempel var at Gemini 2.5 Pro ofte leverte løsninger som så riktige ut på overflaten, men viste seg å ha skjulte mangler – som ikke-fungerende komponenter eller logikkfeil i pseudo-kode eller struktur. I designforslaget nevnt over laget KI-en en dropdown som så ut til å være komplett, men i praksis fungerte den ikke slik brukeren forventet; man fikk rett og slett ikke opp alle valgmuligheter. Vi oppdaget slike feil fordi vi manuelt inspiserte og testet forslagene – det var nødvendig å være kritisk og dobbeltsjekke at KI hadde forstått og løst oppgaven i henhold til kravspesifikasjonene våre. Hver gang vi fant slike feil, måtte vi gå tilbake til prompten, spesifisere kravene enda tydeligere, eller i verste fall løse problemet selv. Det var først med oppgraderingen til Gemini 3.0 Pro at flere av disse pålitelighetsproblemene ble borte og løsningene ble gjennomgående mer robuste og presise. KI kan dermed levere dårlige eller ufullstendige svar – og det oppdages som regel gjennom nitid testing, kritisk vurdering og sammenligning mot våre opprinnelige behov. Vår erfaring er at man alltid må regne med ekstra runder med kontroll, validering og re-prompter for å sikre at produktet faktisk fungerer – uansett hvor imponerende svaret fra KI kan virke ved første blikk. 

**Avhengighet og forståelse:**
Vi brukte KI til alt unntatt proposal.md. Vi har ikke sett gjennom alle dokumentene, men kvalitetssikret dem i manuelle runder med "Check for inconsistencies with @old_doc". Vi ble avhengig av KI for å lage de videre dokumentene, da vi ikke visste hva som stod i de forrige. KI sin utviklingshastighet gjorde det vanskelig å sette av tid til å forstå dokumentene våre, da det var lettere å bare gå videre og stole på KI.

**Kreativitet og problemløsning:**
Vi merket en snikende tendens til at AI-en "pushet" oss mot standardløsninger. Når vi ba om et designforslag, valgte den ofte trygge, generiske valg ("Bootstrap-looken" eller standard Tailwind-komponenter). Den valgte farger, layouts og fontstørrelser uten å spørre. Dette førte til en form for "design-automasjon" hvor vi mistet noe av den kreative kontrollen. Vi måtte aktivt kjempe imot ("Make it look more ...") for å gi applikasjonen særpreg.

### 4.3 Sammenligning: Med og uten KI
Uten KI ville dette prosjektet sett helt annerledes ut. Vi ville sannsynligvis ikke ha nådd målet om en fungerende MVP med denne kompleksiteten. Vi ville brukt uker på å sette opp infrastrukturen og debugge enkle skrivefeil. Vi ville kanskje hatt en enklere simulering, men med tryggere, håndskrevet kode. Med KI fikk vi en mer avansert, funksjonsrik applikasjon, men med en kodebase som føles litt mer fremmed for oss. Sluttresultatet er teknisk overlegent, men kanskje litt mindre "håndverksmessig polert" på mikronivå. Da vi ikke har kunnskap om biblioteken måtte vi også ha endret til mer enkle rammeverk, eller brukt masse tid på å sette oss inn i dette.

### 4.4 Samlet vurdering
KI var utvilsomt en netto positiv faktor, men den endret arbeidets natur fundamentalt. Vi gikk fra å være "coders" til å være "code reviewers" og "prompt engineers". Den viktigste lærdommen er at AI ikke erstatter kompetanse; den krever en *høyere* grad av overordnet systemforståelse for å brukes effektivt. Du kan ikke be en AI bygge et hus hvis du ikke vet forskjellen på en bærebjelke og en lettvegg.

---

## 5. Etiske implikasjoner

### 5.1 Ansvar og eierskap
Hvem eier egentlig handlingene til en autonom agent? I AIES vil vi se agenter ta uventede beslutninger. En agent kan for eksempel nekte å handle med en annen fordi den har blitt "fornærmet" i en tidligere forhandlingsrunde. Dette er isåfall emergent adferd vi ikke eksplisitt hadde kodet, men som oppstår fra samspillet mellom system-prompten og modellens treningsdata.
I en simulering er dette fascinerende og ufarlig. Men hvis slike agenter styrte ekte penger eller tok beslutninger om lån og forsikring, ville ansvarsspørsmålet vært akutt. Er det Eirik som skrev koden, Sofus som skrev prompten, Google som trente modellen, eller agenten selv som er ansvarlig? Vi mener at ansvaret til syvende og sist alltid må ligge hos menneskene som deployerer systemet. "Algoritmen gjorde det" er ingen gyldig unnskyldning, verken i dag eller i fremtiden.

### 5.2 Transparens og åpenhet
Vi synes man bør være åpne om at programmer er bygget med tung AI-assistanse. Koden bærer preg av det (kommentarer, struktur) uansett. Å skjule dette ville vært uærlig mot brukerne og mot fagfeltet. I fremtiden tror vi "AI-assisted" vil bli en standard merkelapp på programvare, en slags varedeklarasjon som sier noe om hvordan produktet er blitt til, i hvert fall så lenge som det ikke er standarden. Hvis man ikke er åpen om dette, kan det komme frem store sikkerhetsmangler hvis koden ikke reviewes riktig.

### 5.3 Påvirkning på læring og kompetanse
Dette prosjektet har vekket en bekymring hos oss. Det er en reell fare for at juniorutviklere mister den grunnleggende "mengdetreningen" man får av å skrive kode manuelt, feile, google/stack-overflowe, og prøve igjen. Hvis man alltid får svaret servert på et sølvfat av en AI, utvikler man da den intuisjonen som trengs for å oppdage når AI-en tar feil?
Vi klarte å redde prosjektet når AI-en feilet (f.eks. med 2.5 Pro-problemene) fordi vi *hadde* grunnleggende kunnskap. Vi visste hvordan filsystemet fungerer, hvordan editorer oppfører seg. Uten denne "tause kunnskapen" hadde vi strandet. Vi frykter en fremtid hvor utviklere kan *bestille* kode, men ikke *forstå* den.

### 5.4 Arbeidsmarkedet
KI kommer til å endre IT-arbeidsmarkedet fundamentalt de neste årene. Oppgaver som tidligere krevde flere utviklere, kan delvis automatiseres eller utføres mye raskere ved hjelp av generative modeller. Dette innebærer at etterspørselen etter tradisjonelle "kode-slave"-roller (f.eks. enkel frontend-utvikling eller rutinepreget backendl og testskriving) vil avta. Samtidig vil behovet for fagfolk som evner å styre, kvalitetssikre og orkestrere KI-drevne utviklingsprosesser øke kraftig.

Roller som "prompt engineer", "AI project lead", "data curator" og "system-arkitekt" vil bli mye viktigere. Det vil være et økt behov for personer som kan validere og verifisere KI-generert kode, bidra med domenekunnskap, og tolke krav og kompleks forretningslogikk i samarbeid med KI-modeller. Dybdeforståelse for systemarkitektur og evnen til å skjønne "hvorfor" fremfor "hvordan" blir sentralt.

Samtidig tror vi at kreative, tverrfaglige roller vil styrkes. Grensene mellom utvikler, designer, analytiker og produkteier viskes delvis ut – alle må forstå hvordan KI jobber, og hvordan man best leder den mot ønsket mål. Det er ikke lenger nok å kunne et rammeverk eller et språk; man må forstå prinsipper for maskinlæring, datastrukturer, domeneproblemer og etikk.

For vår egen del utfordret prosjektet oss til å tenke nytt om karrierevalget. I en KI-drevet verden vil behovet for ren "håndkoding" bli mindre, men behovet for overordnet forståelse, problemløsningsevne og evnen til å sette menneskelig retning (Purpose, ikke bare Task) bli viktigere. Vi ser også at de mest engasjerende rollene i fremtiden vil handle om samspill mellom menneske og maskin, og at KI er et kraftfullt verktøy – men brukeren av verktøyet må være en kritisk, nysgjerrig og ansvarlig leder.

### 5.5 Datasikkerhet og personvern
I prosjektet måtte vi vurdere hvilke data vi delte med KI-verktøyene, spesielt siden LLMene vi brukte (Google Gemini via CLI) i utgangspunktet kan være trente på store, åpne datasett og potensielt kan lagre eller analysere innhold vi sender inn. Det meste vi delte var ikke-personspesifikt: prosjektbeskrivelser, kravspesifikasjoner, arkitekturtegninger og kodeutkast. Vi delte aldri sensitiv persondata, men det var et etisk poeng å vurdere hva som faktisk havnet i promptene vi sendte.

Potensielle risikoer oppstår hvis man skulle kopiert inn autentiske brukerdata eller tilgangsnøkler – noe vi aktivt unngikk. Koden som genereres av KI kan dessuten inneholde "usynlige" sikkerhetshull: bibliotekvalg, ukritisk bruk av tredjeparter, eller svak implementering (f.eks. hardkodede nøkler eller manglende inputvalidering). 

For å tenke riktig omkring sikkerhet ved bruk av KI i utvikling, er det viktig å:
- Aldri dele ekte brukerinformasjon eller sensitive data i promptene.
- Validere at kode KI-en genererer ikke inneholder åpenbare hull (eksponerte nøkler, sårbare biblioteker).
- Sørge for at alle KI-genererte features testes og kvalitetssikres mot sikkerhetskrav før produksjon.
- Tenke over at dokumentasjon, konfigurasjonsfiler og systemdiagrammer også kan inneholde sensitiv informasjon.

Vårt generelle råd er å behandle alt man sender til eksterne KI-tjenester som om det var "semi-offentlig". Sannsynligheten for misbruk er liten i praksis, men konsekvensen kan være stor – og ansvaret ligger alltid hos utviklerne selv. Vi mener dette gir verdifulle sekundærlærdommer ikke bare om KI, men om generelt sikkerhetsarbeid i digitale prosjekter.

---

## 6. Teknologiske implikasjoner

### 6.1 Kodekvalitet og vedlikehold
KI-generert kode kan være et mareritt å vedlikeholde over tid. Den mangler ofte den helhetlige "tanken" eller signaturen til en menneskelig forfatter. Vi har i tidliegere prosjekt sett at koden vår er blitt noe fragmentert; ulike moduler følger litt ulike mønstre basert på hvilken dag og i hvilken kontekst de ble generert. Uten streng og kontinuerlig refaktorering (utført av mennesker), råtner AI-kode raskt. Streng code review er ikke lenger bare en kvalitetssjekk, det er en overlevelsesmekanisme for kodebasen.

### 6.2 Standarder og Beste Praksis
AI-en er flink til å følge standarder *hvis* den blir bedt om det eksplisitt. Ved å bruke Pydantic og Type Hints, eller MCP-servere med nyeste dokumentasjon kan man tvinge fram en høy standard. Men overlatt til seg selv, kan den fort falle tilbake på utdaterte biblioteker den har sett mye av i treningsdataene sine, eller bruke "quick fixes" som er dårlig praksis (f.eks. hardkoding av verdier). Man må vite hva "beste praksis" er for å kunne kreve det av AI-en.

### 6.3 Fremtidig utvikling
KI vil fundamentalt endre måten vi utvikler programvare på. Man går fra å skrive alt selv til å orkestrere og validere forslag fra KI. Dette betyr at kritisk tenkning, systemforståelse og gode valideringsrutiner blir viktigere enn rene kodeferdigheter.

I fremtiden tror vi at de beste utviklerne er de som både forstår teknologi og evner å stille klare krav til KI-en. Evnen til å skrive presise prompt, analysere kodeforslag, og sikre kvalitet og sikkerhet, blir mer sentralt enn å lære seg et nytt rammeverk.

Vår anbefaling er: Behandle KI som en dyktig, men uforutsigbar assistent. Stol aldri blindt på løsningsforslagene, og bygg en robust praksis for gjennomgang, testing og sikkerhet. KI er et kraftfullt verktøy, men menneskelig dømmekraft er fortsatt det viktigste.

---

## 7. Konklusjon og Læring

### 7.1 Viktigste lærdommer fra AIES-prosjektet
1.  **Modellen betyr alt:** Forskjellen på Gemini 2.5 Pro og 3.0 Pro var forskjellen på fiasko og suksess for kompleks systemarkitektur. Ikke undervurder verdien av "state-of-the-art".
2.  **Context is King:** Å forstå hvordan kontekstvinduet fungerer, og vite når man skal "cleare" minnet for å unngå forvirring, er en ny kjernekompetanse for utviklere.
3.  **Struktur over kaos:** For å bruke kreative, uforutsigbare LLMer i deterministiske systemer, må man bygge rigide rammer rundt dem. Pydantic-AI var vår redning.
4.  **Ledelse er nøkkelen:** AI-en er en fantastisk arbeider, men en elendig leder. Mennesket må fortsatt sitte i førersetet og sette kursen.

### 7.2 Hva ville dere gjort annerledes?
Hvis vi skulle startet prosjektet på nytt i dag, med den viten vi har nå, ville vi:
*   Gått rett på **Gemini 3.0 Pro** fra dag én for å unngå uken med debugging av 2.5 Pro sine hallusinasjoner.
*   Satt oss mer inn i Agile Programming. BMAD-rammeverket bygger på dette, men var i starten ikke stabilt nok til å følge de riktige stegene videre.
*   Bestemt en fast tid i uka da vi kunne samarbeide fysisk. Dette hadde gitt oss mer tid til å arbeide og forstå prosjektet.

### 7.3 Anbefalinger til andre studenter
*   **Ikke stol blindt på AI-en.**
*   **Lær deg prompt engineering.** Det er det nye programmeringsspråket. Lær deg forskjellen på en null-shot og en few-shot prompt.
*   **Behold kodingen i fingrene.** Ikke la AI-en gjøre alt. Skriv litt kode selv hver dag for å holde ferdighetene ved like.
*   **AI er dement.** Start samtalen på nytt så fort som mulig for å cleare context-vinduet. Jo mindre context, jo bedre.
*   **AI er et barn.** Den mister fort fokus og kan finne på de dummeste tingene hvis den ikke instrueres direkte.

### 7.4 Personlige refleksjoner

**Eirik Malme Moltubak (Gruppeleder & Arkitekt):**
For meg har dette prosjektet handlet om kampen for ren arkitektur i møte med en entropisk kraft. Å være "Lead Architect" med en AI som hovedutvikler er som å lede et orkester hvor en av fiolinistene (AI-en) er et geni som improviserer konstant – noen ganger briljant, noen ganger katastrofalt. Min største utfordring var å håndheve disiplin. Når Gemini foreslo en "kjapp fiks" som brøt med våre idéer, måtte jeg være den som sa "nei" på en effektiv måte.
Jeg har lært at rollen til en seniorutvikler i fremtiden vil dreie seg mindre om å skrive selve syntaksen, og mer om *code review*, arkitektonisk styring og systemforståelse. Evnen til å lese og validere kode man ikke har skrevet selv, blir den viktigste ferdigheten. Det å oppdage at modellen konsekvent ignorerte visse instrukser lærte meg at man aldri kan stole blindt på "black box"-magi. Det har vært en lærerik, men også utmattende prosess å være "The Human in the Loop".

**Vigfus Alexander Robertsson (Teknisk Feasibility, Visualisering/Frontend & KI-Kvalitetssikring):**
Min rolle var todelt. For det første fungerte jeg som det tekniske ankeret som sikret at ambisjonene i prosjektet var forankret i realiserbar kode. Med erfaring fra Brunvoll og min bakgrunn fra IT VGS, lå mitt fokus på å tenke to skritt frem: Er denne løsningen skalerbar? Vil dette skape teknisk gjeld? Jeg viet mye tid til kodegjennomgang (code review) av AI-generert kode, og brukte min tidligere erfaring med KI-verktøy til å raskt identifisere hallusinasjoner og logiske brister før de krevde omfattende omskrivning. Dette plasserte meg i grensesnittet mellom prompt engineering (hvor jeg bidro til å strukturere instruksene for presisjon) og kvalitetssikring (hvor jeg validerte utførelsen).
For det andre hadde jeg et spesielt ansvar for visualisering og frontend-implementeringen i Next.js. Utfordringen her var å ta de abstrakte, dynamiske JSON-dataene fra agentenes forhandlinger – som representerte "subjektiv økonomisk verdi" og komplekse transaksjoner – og oversette dem til intuitive, sanntidsgrafer og diagrammer. Jeg måtte aktivt jobbe med KI-en for å designe og implementere responsive React-komponenter og sikre at brukergrensesnittet (UI) effektivt kommuniserte simuleringsstatusen.
Jeg har lært at i KI-assistert programmering er det ikke lenger nok å vite hvordan man koder; man må forstå hvordan KI-en feiler for å kunne lede den riktig. Dette har understreket verdien av menneskelig intuisjon for teknisk risiko i alle lag av applikasjonen, fra API-design til datavisualisering.

**Sofus August Hvattum (Logikk & Økonomi):**
Dette prosjektet har vært en skikkelig øyeåpner. Jeg måtte fort lære både teknisk terminologi og KI-logikk. Å jobbe tverrfaglig tvang meg til å formulere ideene mine mye klarere, og jeg skjønte fort at teori må oversettes helt presist til konkrete regler for at KI-en faktisk skal forstå. Jeg fikk bryne meg på både prompt engineering og koding, og måtte lære meg å se hvor og hvorfor både folk og KI "feiler". Det viktigste jeg tar med meg, er hvor mye kraft det er i å kombinere strukturert økonomisk logikk med kreativ KI – men også at ingenting fungerer uten gode rammer og tydelig ledelse. Jeg føler meg tryggere teknologisk, og mer bevisst på hvor viktig det er å samarbeide på tvers av fagfelt.



---

## 8. Vedlegg

- **GitHub Repository:** https://github.com/IBE160/SG-418
- **Prompting:** https://github.com/IBE160/SG-418/tree/main/prompting
- **Dokumentasjon:** Se `docs/`-mappen i repoet for detaljerte arkitektur- og designvalg.
- **Prompt-logg:** En samling av de mest kritiske system-promptene finnes i `SG-418/prompts/`.

---

**Ordantall:** Ca. 3500 ord.
