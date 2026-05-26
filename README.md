# blokkedes-imitacijas-modelis

Šajā repozitorijā ir ietverts blokķēdes darījumu apstrādes simulācijas modeļa pirmkods, kas izstrādāts bakalaura darba ietvaros.

Simulācijas modeļa mērķis ir analizēt, kā dažādi sistēmas slodzes scenāriji ietekmē blokķēdes darījumu caurlaidspēju, apstiprināšanas laiku, mempool dinamiku un relatīvās resursu izmaksas.

## Darba tēma

**Blokķēdes simulācijas modeļa izstrāde darījumu apstrādes veiktspējas un resursu patēriņa analīzei**

## Galvenā funkcionalitāte

Simulācijas modelis ļauj mainīt šādus parametrus:

- darījumu ģenerēšanas ātrums;
- bloka lielums;
- bloka ģenerēšanas intervāls;
- simulācijas ilgums;
- tīkla aizkaves diapazons.

Modelis ģenerē šādus izejas rādītājus:

- darījumu caurlaidspēja;
- vidējais apstiprināšanas laiks;
- mempool lieluma dinamika;
- relatīvās resursu izmaksas rādītājs.

## Projekta struktūra

```
.
├── app_main.py
├── core_model.py
├── simulacija_ui.py
├── test_app.py
├── prasības.txt
├── rezultāti/
├── skaitļi/
└── README.md
