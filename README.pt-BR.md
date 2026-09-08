<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
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

Ressonância de Schumann como uma superfície 3D tempo-frequência com faixas de eventos e um painel de correlação cruzada honesto e com atraso. Um mês de dados reais de uma estação ELF, apresentados de forma que uma pessoa possa visualizar o ritmo diário dos relâmpagos, as faixas de modo e o que uma tempestade geomagnética faz e não faz.

Status: v1.0.0. Outubro e junho de 2013, da estação ELF de Sierra Nevada (Universidade de Granada), reproduzido em relação aos espectros e ajustes de modo publicados pela própria estação, slot a slot; os dez meses restantes do arquivo bruto estão sendo processados pela mesma linha de produção. O visualizador é um único arquivo HTML autocontido com quatro modos; disponível em [página inicial](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/).

## O que ele mostra

- **Superfície**: tempo (um mês, colunas de 30 minutos) × frequência (6–25 Hz, linhas de 0,125 Hz) × amplitude magnética em dB em relação a 1 pT/√Hz. Sensores NS e EW como duas camadas empilháveis.
- **Faixas de modo**: frequência central ajustada dos modos 1–3 sobre a superfície.
- **Faixas de eventos** em frente à superfície: índice geomagnético Kp (a cada 3 horas, GFZ), hora local na estação (calculada a partir do carimbo de data/hora), terremotos M6+ (USGS).
- **Painel de correlação**: Pearson r em relação ao atraso (±24 h) entre qualquer série de superfície (amplitude do modo, frequência do modo, potência da banda) e qualquer série de eventos, com uma banda nula de 95%, cujo tamanho efetivo da amostra é corrigido para autocorrelação em ambas as séries (Bartlett). Uma curva dentro da banda é um resultado nulo e é exibida como tal.

## Por que a banda é de 6–25 Hz

A bobina da estação é um sensor RLC com ressonância próxima a 33 Hz e calibrada por seus autores apenas para 6–25 Hz. Acima de 25 Hz, o espectro bruto é dominado pela ressonância do sensor, e não pela cavidade, portanto, os modos 4 e superiores não podem ser resolvidos com este instrumento. Uma estação de banda mais ampla é necessária para eles.

## Verificação (outubro de 2013, 4464 slots por sensor)

| Verificação em relação ao npz publicado pela estação | NS | EW |
|---|---|---|
| Relação do espectro de amplitude, nosso/estação, 6–25 Hz (mediana, p5, p95) | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| Fração de saturação por slot, correlação | 1.000 | 1.000 |
| Frequência central do modo 1, diferença da mediana | +0,004 Hz | +0,008 Hz |
| Frequência central do modo 2, diferença da mediana | +0,000 Hz | +0,002 Hz |
| Frequência central do modo 3, diferença da mediana | −0,000 Hz | +0,001 Hz |
| Relação da amplitude de pico do modo, mediana | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

O desvio residual da frequência é devido às duas implementações de Levenberg-Marquardt (lmfit na estação, SciPy aqui) convergindo para mínimos locais diferentes em alguns por cento dos slots; o visualizador mascara os ajustes que deixam as janelas por modo documentadas.

O verificador é um portão: ele sai com um valor diferente de zero, a menos que ≥ 95% dos slots correspondam em 30 segundos, os percentis 5º e 95º da relação do espectro estejam dentro de 1 ± 0,005, a diferença da frequência mediana de cada modo seja inferior a 0,02 Hz e as séries de saturação se correlacionem acima de 0,99.

## Faixa de relâmpagos: modelo, não medição

Não existe nenhuma série global de relâmpagos medida e disponível publicamente para 2013 (WWLLN é por assinatura, o arquivo Blitzortung requer um login de participante, a climatologia LIS/OTD da NASA está disponível no Earthdata). O visualizador, portanto, carrega um **cronograma de chaminé** como uma faixa de modelo: três gaussianas na hora UTC para o Sudeste Asiático, África e as Américas, após Whipple 1929, a curva de Carnegie (Harrison 2013) e a climatologia diurna LIS/OTD (Blakeslee et al. 2014). É rotulado como um modelo sempre que é exibido. O equivalente medido também está incorporado: a média por hora UTC da amplitude de cada modo ao longo do mês. Veja `docs/data-contract.md`.

## Dados e licenças

| Fonte | O que | Licença | Uso aqui |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | série temporal bruta de 256 Hz, março–dezembro de 2013 e janeiro–fevereiro de 2017 | CC BY 4.0 | entrada; os produtos derivados são de nossa autoria para publicação com atribuição |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | espectros de 10 minutos processados pela estação + ajustes de Lorentzian | CC BY-NC-ND 3.0 | somente verificador, nunca redistribuído |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148; código [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | fórmula de calibração e cadeia de processamento | artigo CC BY-NC-ND; código de acordo com seu repositório | método reproduzido em `scripts/process_month.py` |
| Índice Kp do GFZ Potsdam, Matzka et al. 2021 | Kp a cada 3 horas | CC BY 4.0 | faixa de eventos |
| Serviço de eventos FDSN do USGS | terremotos | domínio público | faixa de eventos |

Nada em `data/` é confirmado. O arquivo Zenodo é um único arquivo zip de 26,5 GB; o script de busca lê seu diretório central por meio de solicitações de intervalo HTTP e transmite apenas o mês solicitado.

## Linha de produção

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

Método fixo (espelha a cadeia da estação para que possa ser verificado): janelas Hann de 10 segundos, 50% de sobreposição, FFT com preenchimento zero para 8192 (31,25 mHz), janelas saturadas descartadas, calibração RLC `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f` com L = 298 kH, C = 77,75 pF, R = 320 kΩ, filtro de linha reta da banda antropogênica, três Lorentzianas mais um termo linear ajustado no domínio da amplitude em 6,35–23,75 Hz.

## Conformidade com os padrões

Pontuação de 0–3 em relação aos seis padrões de fluxo de trabalho do estúdio.

| Padrão | Pontuação | Evidência |
|---|---|---|
| PIN_PER_STEP | 2 | Cada opção numérica (janela, sobreposição, tamanho da FFT, constantes de calibração, banda de ajuste, sementes) é uma constante nomeada no início de `process_month.py` e é gravada no campo npz `method`. Ainda não é possível reproduzir os resultados em diferentes versões do NumPy; não há registro das versões da biblioteca. |
| AUTORIDADE_ANDON | 2 | `verify_against_granada.py` é o ponto de interrupção em caso de divergência com os ajustes publicados da estação; o script de recuperação verifica o tamanho descomprimido de cada entrada do arquivo zip antes de gravar. |
| COMPENSADORES_NOMEADOS | 2 | Não há chamadas externas irreversíveis no fluxo de trabalho. O único caminho de publicação é um envio (push) para o Git do código-fonte; `data/` é ignorado. Compensador para um `viewer/index.html` problemático: reconstruir a partir do arquivo npz. |
| DECOMPOSIÇÃO_POR_SEGREDOS | 2 | Recuperar, processar, verificar e construir são quatro scripts, cada um com uma tarefa; o modelo de visualização não tem conhecimento da estação e utiliza um bloco JSON independente da estação. |
| HUMANOS_COM_LIMITAÇÃO_DE_INCERTEZA | 1 | O painel de correlação mostra a banda nula, que é o limite de incerteza para o visualizador. Não há nenhum ponto de verificação humano no próprio fluxo de trabalho. Correção: fazer com que o verificador emita um resultado de aprovação/reprovação com base em uma tolerância definida (responsável: próxima sessão). |
| VERIFICADOR_EXTERNO | 3 | O verificador é a saída produzida de forma independente pela própria estação (código diferente, autores diferentes, lmfit vs SciPy). Números na tabela acima. |

## Modelo de confiança e ameaças

O fluxo de trabalho é executado localmente a partir de um checkout. Ele lê e grava apenas em `data/` e `viewer/`.
O acesso à rede ocorre apenas quando você solicita que um script recupere dados: Zenodo (arquivo bruto), Digibug (arquivos de verificação da estação), GFZ (Kp), USGS (terremotos). O upload do conjunto de dados usa seu próprio login do Hugging Face fora desses scripts. Nenhuma credencial é lida ou armazenada, nenhum dado de telemetria é enviado e o visualizador é uma página estática que carrega o Three.js e duas fontes de CDNs públicas, e nada mais.
Requisitos: Python 3.11 ou mais recente com NumPy, SciPy e PyArrow, em qualquer sistema operacional; o Node é necessário apenas para a página de destino opcional.

## Licença

Licença MIT para o código. Os produtos de dados derivados contêm a atribuição exigida por suas fontes.

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
