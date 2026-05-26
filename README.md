# blokkedes-imitacijas-modelis

Šajā repozitorijā ir pieejams bakalaura darba ietvaros izstrādātais blokķēdes darījumu apstrādes imitācijas modelis.

Modeļa mērķis ir analizēt, kā dažādi slodzes scenāriji ietekmē blokķēdes darījumu caurlaidspēju, darījumu apstiprināšanas laiku, mempool apjoma dinamiku un relatīvo resursu izmaksu rādītāju.

## Bakalaura darba tēma

**Blokķēžu imitācijas modeļa izstrāde darījumu apstrādes veiktspējas un resursu patēriņa analīzei**

## Projekta apraksts

Projekts realizē vienkāršotu blokķēdes darījumu apstrādes imitācijas modeli. Modelī iespējams mainīt darījumu ģenerēšanas intensitāti, bloka izmēru, bloku ģenerēšanas intervālu, simulācijas ilgumu un tīkla aizkaves robežas.

Izstrādātais modelis paredzēts kontrolētu eksperimentu veikšanai, lai salīdzinātu sistēmas darbību dažādos slodzes apstākļos, neizmantojot reālu blokķēdes tīklu.

## Galvenās funkcijas

- zemas, vidējas un augstas slodzes scenāriji;
- iespēja manuāli mainīt simulācijas parametrus;
- darījumu ģenerēšana, izmantojot varbūtisku modeli;
- vienkāršota mempool un bloku veidošanas loģika;
- tīkla aizkaves modelēšana;
- darījumu caurlaidspējas, apstiprināšanas laika, mempool apjoma un resursu izmaksu aprēķins;
- grafiskā lietotāja saskarne simulācijas palaišanai;
- simulācijas rezultātu eksportēšana CSV formātā;
- attēlu ģenerēšana bakalaura darba eksperimentālajai daļai.

## Projekta struktūra

```
.
├── config.py
├── core_model.py
├── simulation.py
├── gui.py
├── main.py
├── visualization.py
├── requirements.txt
├── results/
│   ├── simulation_step_results.csv
│   └── simulation_summary.csv
└── figures/
    ├── 3_1_darijumu_caurlaidspeja_tps.png
    ├── 3_2_videjais_apstiprinasanas_laiks.png
    ├── 3_3_mempool_dinamika.png
    └── 3_4_resursu_izmaksu_raditajs.png
├── skaitļi/
└── README.md
