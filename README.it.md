<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/schumann-surface/readme.png" alt="Schumann Surface" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="https://mcp-tool-shop-org.github.io/schumann-surface/"><img src="https://img.shields.io/badge/landing-page-0ea5e9" alt="Landing page"></a>
  <a href="https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-ffcc4d" alt="Dataset"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.zh.md">中文</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (BR)</a></p>

# schumann-surface

Risonanza di Schumann come superficie 3D spazio-temporale con bande di eventi e un pannello di correlazione incrociata onesto e con un certo ritardo. Un mese di dati reali di una stazione ELF, presentati in modo che si possa visualizzare il ritmo giornaliero dei fulmini, le bande dei modi e l'effetto (e la mancanza di effetto) di una tempesta geomagnetica.

Stato: v1.0.0. Ottobre e giugno 2013, dati della stazione ELF di Sierra Nevada (Università di Granada), riprodotti confrontandoli con gli spettri e le curve di adattamento dei modi pubblicati dalla stazione, slot per slot; i restanti dieci mesi dell'archivio originale vengono elaborati attraverso la stessa pipeline. Il visualizzatore è un singolo file HTML autonomo con quattro modalità; disponibile all'indirizzo [pagina di destinazione](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/).

## Cosa mostra

- **Superficie**: tempo (un mese, colonne di 30 minuti) × frequenza (6–25 Hz, righe di 0,125 Hz) × ampiezza magnetica in dB rispetto a 1 pT/√Hz. Sensori NS ed EW come due fogli sovrapponibili.
- **Bande dei modi**: frequenza centrale adattata dei modi 1–3 sovrapposta alla superficie.
- **Bande degli eventi** di fronte alla superficie: indice geomagnetico Kp (ogni 3 ore, GFZ), ora locale alla stazione (calcolata dal timestamp), terremoti di magnitudo 6 o superiore (USGS).
- **Pannello di correlazione**: correlazione di Pearson r rispetto al ritardo (±24 ore) tra qualsiasi serie di dati della superficie (ampiezza del modo, frequenza del modo, potenza della banda) e qualsiasi serie di dati degli eventi, con una banda nulla del 95%, la cui dimensione del campione effettiva è corretta per l'autocorrelazione in entrambe le serie (Bartlett). Una curva all'interno della banda rappresenta un risultato nullo ed è visualizzata come tale.

## Perché la banda è 6–25 Hz

La bobina della stazione è un sensore RLC con risonanza a circa 33 Hz ed è stata calibrata dai suoi autori solo per la banda 6–25 Hz. Al di sopra di 25 Hz, lo spettro originale è dominato dalla risonanza del sensore, non dalla cavità, quindi i modi 4 e successivi non possono essere risolti con questo strumento. È necessaria una stazione a banda più ampia per questi.

## Verifica (ottobre 2013, 4464 slot per sensore)

| Confronto con i dati npz pubblicati dalla stazione | NS | EW |
|---|---|---|
| Rapporto dello spettro di ampiezza, nostro/stazione, 6–25 Hz (mediana, 5° percentile, 95° percentile) | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Frazione di saturazione per slot, correlazione | 1.000 | 1.000 |
| Frequenza centrale del modo 1, differenza mediana | +0,004 Hz | +0,008 Hz |
| Frequenza centrale del modo 2, differenza mediana | +0,000 Hz | +0,002 Hz |
| Frequenza centrale del modo 3, differenza mediana | -0,000 Hz | +0,001 Hz |
| Rapporto dell'ampiezza di picco del modo, mediana | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

La dispersione residua della frequenza è dovuta al fatto che le due implementazioni di Levenberg–Marquardt (lmfit nella stazione, SciPy qui) convergono su minimi locali diversi per una piccola percentuale di slot; il visualizzatore maschera gli adattamenti che escono dalle finestre per ciascun modo documentate.

Il verificatore è una barriera: esce con un valore diverso da zero a meno che non sia soddisfatta la condizione che ≥ 95% degli slot corrispondano entro 30 secondi, i percentili 5° e 95° del rapporto dello spettro siano compresi tra 1 ± 0,005, la differenza mediana della frequenza di ciascun modo sia inferiore a 0,02 Hz e le serie di saturazione siano correlate con un valore superiore a 0,99.

## Banda dei fulmini: modello, non misurazione

Non esiste una serie di dati globali misurati sui fulmini scaricabile liberamente per il 2013 (WWLLN richiede un abbonamento, l'archivio Blitzortung richiede l'accesso di un partecipante, la climatologia LIS/OTD della NASA è disponibile tramite Earthdata). Il visualizzatore include quindi un **programma di fulmini** come banda di modello: tre gaussiane nell'ora UTC per il Sud-est asiatico, l'Africa e le Americhe, basato su Whipple 1929, la curva di Carnegie (Harrison 2013) e la climatologia diurna LIS/OTD (Blakeslee et al. 2014). È etichettato come modello ovunque venga visualizzato. La controparte misurata è anch'essa inclusa: la media per ora UTC dell'ampiezza di ciascun modo nell'arco del mese. Vedere `docs/data-contract.md`.

## Dati e licenze

| Origine | Cosa | Licenza | Utilizzo qui |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | serie temporali grezze a 256 Hz, marzo-dicembre 2013 e gennaio-febbraio 2017 | CC BY 4.0 | input; i prodotti derivati sono di nostra proprietà e possono essere pubblicati con l'attribuzione |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | spettri a 10 minuti elaborati dalla stazione + adattamenti di Lorentz | CC BY-NC-ND 3.0 | solo per il verificatore, mai ridistribuito |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148; codice [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | formula di calibrazione e catena di elaborazione | articolo CC BY-NC-ND; codice secondo le condizioni del repository | metodo riprodotto in `scripts/process_month.py` |
| Indice Kp di GFZ Potsdam, Matzka et al. 2021 | Kp ogni 3 ore | CC BY 4.0 | banda degli eventi |
| Servizio eventi FDSN dell'USGS | terremoti | dominio pubblico | banda degli eventi |

Niente in `data/` viene salvato. L'archivio Zenodo è un singolo file zip da 26,5 GB; lo script di acquisizione legge la sua directory centrale tramite richieste di intervallo HTTP e trasmette solo il mese richiesto.

## Pipeline

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

Metodo fisso (rispecchia la catena della stazione in modo che possa essere verificato): finestre Hann di 10 secondi, sovrapposizione del 50%, FFT con zero-padding a 8192 (31,25 mHz), finestre saturate eliminate, calibrazione RLC `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f` con L = 298 kH, C = 77,75 pF, R = 320 kΩ, filtro a linea retta per la banda antropogenica, tre gaussiane più un termine lineare adattato nel dominio dell'ampiezza nell'intervallo 6,35–23,75 Hz.

## Conformità agli standard

Punteggio da 0 a 3 rispetto ai sei standard del flusso di lavoro dello studio.

| Standard | Punteggio | Evidenza |
|---|---|---|
| PIN_PER_STEP | 2 | Ogni scelta numerica (finestra, sovrapposizione, dimensione FFT, costanti di calibrazione, intervallo di adattamento, valori iniziali) è una costante con un nome definito all'inizio di `process_month.py` e viene scritta nel campo npz `method`. Non è ancora possibile riprodurre i risultati tra diverse versioni di NumPy; non sono disponibili informazioni sulle versioni delle librerie. |
| AUTORITÀ ANDON | 2 | `verify_against_granada.py` è il punto di interruzione in caso di disaccordo con gli adattamenti pubblicati dalla stazione; lo script di recupero verifica la dimensione decompressa di ogni voce zip prima di scriverla. |
| COMPENSATORI NOMINATI | 2 | Non sono presenti chiamate esterne irreversibili nella pipeline. L'unico percorso di pubblicazione è un push Git del codice sorgente; `data/` viene ignorato. Compensatore per un `viewer/index.html` difettoso: ricostruzione a partire dal file npz. |
| DECOMPOSIZIONE BASATA SU SEGRETI | 2 | Recupero, elaborazione, verifica e creazione sono quattro script, ciascuno con un compito specifico; il modello di visualizzazione non conosce la stazione e utilizza un blocco JSON indipendente dalla stazione. |
| UMANI CON CONTROLLO DELL'INCERTEZZA | 1 | Il pannello di correlazione mostra la banda nulla, che rappresenta il controllo dell'incertezza per il visualizzatore. Non è presente alcun punto di controllo umano nella pipeline stessa. Azioni correttive: fare in modo che il verificatore emetta un risultato di superamento/fallimento rispetto a una tolleranza specificata (responsabile: prossima sessione). |
| VERIFICATORE ESTERNO | 3 | Il verificatore è l'output prodotto in modo indipendente dalla stazione (codice diverso, autori diversi, lmfit rispetto a SciPy). I numeri sono riportati nella tabella precedente. |

## Modello di fiducia e di minaccia

La pipeline viene eseguita localmente da una copia del codice. Legge e scrive solo all'interno di `data/` e `viewer/`.
L'accesso alla rete avviene solo quando si richiede a uno script di recuperare dati da: Zenodo (archivio originale), Digibug (file di verifica della stazione), GFZ (Kp), USGS (terremoti). Il caricamento del set di dati utilizza il proprio account Hugging Face al di fuori di questi script. Non vengono lette o archiviate credenziali e non vengono inviati dati di telemetria; il visualizzatore è una pagina statica che carica Three.js e due font da CDN pubblici e nient'altro.
Requisiti: Python 3.11 o versione successiva con NumPy, SciPy e PyArrow, su qualsiasi sistema operativo; Node è necessario solo per la pagina di destinazione opzionale.

## Licenza

Licenza MIT per il codice. I prodotti di dati derivati riportano l'attribuzione richiesta dalle loro fonti.

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
