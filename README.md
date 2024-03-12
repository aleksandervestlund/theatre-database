> Skrevet av: Andreas Kolstad Bertelsen, Fredrik Oldeide Roos, og Aleksander Thornes Vestlund.

## Databaseprosjekt

### Krav til kjøring

Sørg for at du har lastet ned:

- Python >=3.11.

### Starting av applikasjonen

```bash
$ python main.py
```

### Valgmuligheter

Du kommer til å få tre valg, i tillegg til å avslutte applikasjonen.

- `1: Endre database`
- `2: Bestill billetter`
- `3: SQL-spørringer`

#### Endre database

Dersom du velger dette alternativet, får du fire nye valg.

- `1: Tøm databasen`. Dette alternativet produserer en helt tom `.db`-fil.
- `2: Fyll databasen med tabeller`. Dette alternativet leser `schema.sql`-filen og lager de forskjellige tabellene.
- `3: Fyll databasen med forhåndsbestemte rader`. Dette alternativet legger til alle forhåndsdefinerte rader beskrevet i prosjektbeskrivelsen.
- `4: Reserver forhåndsbestilte seter`. Dette alternativet leser `hovedscenen.txt` og `gamle-scene.txt` for å reservere setene bestemt der.

#### Bestill billetter

Her får du muligheten til å bestille billetter, der alle setene er på samme rad. Denne viser også prisen på bestillingen.

#### SQL-spørringer

Dersom du velger dette alternativet, får du fire nye valg.

- `1: Forestillinger på gitt dato`. Dette alternativet viser alle forestillinger på en brukerbestemt dato.
- `2: Navn på skuespillere`. Dette alternativet finner alle navn på alle skuespillere og hvilke roller disse spiller.
- `3: Bestselgende forestillinger`. Dette alternativet finner de bestselgende forestillingene og viser hvor mange billetter som har blitt solgt til disse.
- `4: Skuespillere i samme akt som gitt skuespiller`. Dette alternativet finner alle skuespillere som har spilt i samme akt som en brukerbestemt skuespiller.
