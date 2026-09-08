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

# シューマン・サーフェース

イベントラインと、正直で遅延のあるクロス相関パネルを備えた、3D時間-周波数サーフェースとしてのシューマン共鳴。実際のELFステーションの1か月分のデータをレンダリングし、人が日々の雷のパターン、モードリボン、そして地磁気嵐が何を引き起こし、何を引き起こさないかを確認できるようにした。

ステータス：v1.0.0。2013年10月と6月、シエラネバダELFステーション（グラナダ大学）から。ステーションが独自に公開したスペクトルとモードフィッティングを、スロットごとに再現。残りの10か月間の生データは、同じパイプラインで処理されている。ビューワーは、4つのモードを備えた単一の独立したHTMLファイルであり、[ランディングページ](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/)で公開されている。

## 表示内容

- **サーフェース**: 時間（1か月、30分間隔の列）×周波数（6〜25 Hz、0.125 Hz間隔の行）×dB単位の磁気振幅（基準値：1 pT/√Hz）。NSおよびEWセンサーを、積み重ね可能な2つのシートとして表示。
- **モードリボン**: サーフェース上に表示される、モード1〜3のフィッティングされた中心周波数。
- **イベントライン**: サーフェースの前面に表示。Kp地磁気指数（3時間間隔、GFZ）、ステーションでの現地時間（タイムスタンプから計算）、M6以上の地震（USGS）。
- **相関パネル**: 任意のサーフェース系列（モード振幅、モード周波数、バンドパワー）と任意のイベント系列との間のピアソンのrと遅延（±24時間）。95%のヌルバンドがあり、その有効サンプルサイズは、両方の系列における自己相関に対して補正されている（バートレット）。バンド内の曲線はヌル結果であり、1つとして表示される。

## バンドが6〜25 Hzである理由

ステーションのコイルは、約33 Hzで共振するRLCセンサーであり、その作成者は6〜25 Hzでのみ校正している。25 Hzを超えると、生スペクトルはキャビティではなく、センサーの共振によって支配されるため、モード4以降はこの装置では分解できない。それらには、より広帯域のステーションが必要である。

## 検証（2013年10月、センサーあたり4464スロット）

| ステーションが公開したnpzと比較 | NS | EW |
|---|---|---|
| 振幅スペクトル比（当方のもの/ステーションのもの）、6〜25 Hz（中央値、p5、p95） | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| スロットごとの飽和度、相関 | 1.000 | 1.000 |
| モード1の中心周波数、中央値の差 | +0.004 Hz | +0.008 Hz |
| モード2の中心周波数、中央値の差 | +0.000 Hz | +0.002 Hz |
| モード3の中心周波数、中央値の差 | -0.000 Hz | +0.001 Hz |
| モードピーク振幅比、中央値 | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

残差周波数散布は、2つのレーベンバーグ-マルカート実装（ステーションのlmfit、ここのSciPy）が、少数のスロットで異なる局所的な最小値に収束することによるもの。ビューワーは、文書化されたモードごとのウィンドウから外れるフィッティングをマスクする。

検証器はゲートである。30秒以内に95%以上のスロットが一致し、スペクトル比の5パーセンタイルと95パーセンタイルが1 ± 0.005の範囲にあり、すべてのモードの中央値の周波数差が0.02 Hz未満であり、飽和系列の相関が0.99を超えている場合にのみ、ゼロ以外の値を返す。

## 雷のライン：モデル、測定値ではない

2013年の測定されたグローバルな雷の系列は、公開されているものがない（WWLLNはサブスクリプション制、Blitzortungアーカイブには参加者のログインが必要、NASAのLIS/OTD気候データはEarthdataの背後に存在する）。したがって、ビューワーは、モデルラインとして**キツネの煙突スケジュール**を搭載している。これは、Whipple 1929、カーネギー曲線（Harrison 2013）、およびLIS/OTDの昼間気候データ（Blakeslee et al. 2014）に基づいて、UTC時間で東南アジア、アフリカ、およびアメリカの3つのガウス関数である。表示される場所はすべて、モデルとしてラベル付けされている。測定された対応するデータも組み込まれている。それは、1か月間の各モードの振幅のUTC時間ごとの平均である。詳細は`docs/data-contract.md`を参照。

## データとライセンス

| ソース | 内容 | ライセンス | 使用方法 |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | 2013年3月から12月、および2017年1月から2月の256 Hzの生時系列データ | CC BY 4.0 | 入力。派生した製品は、帰属表示付きで公開できる。 |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | ステーションで処理された10分ごとのスペクトル+ローレンツフィッティング | CC BY-NC-ND 3.0 | 検証器のみ。再配布は行われない。 |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148; コード [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | キャリブレーション式と処理チェーン | 論文はCC BY-NC-ND、コードはリポジトリのライセンスに従う | 方法は`scripts/process_month.py`で再現 |
| GFZポツダム Kp指数、Matzka et al. 2021 | 3時間ごとのKp | CC BY 4.0 | イベントライン |
| USGS FDSNイベントサービス | 地震 | パブリックドメイン | イベントライン |

`data/`に含まれるものは何もコミットされていない。Zenodoアーカイブは1つの26.5 GBのzipファイルであり、フェッチスクリプトはHTTP範囲リクエストを使用してその中央ディレクトリを読み取り、要求された月のみをストリーミングする。

## パイプライン

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

固定された方法（ステーションのチェーンをミラーリングしているため、検証できる）。10秒のハニング窓、50%のオーバーラップ、8192（31.25 mHz）へのゼロパディング、飽和した窓の破棄、RLCキャリブレーション `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f`（L = 298 kH、C = 77.75 pF、R = 320 kΩ）、人工バンドの直線フィルター、6.35〜23.75 Hzの振幅ドメインでフィッティングされた3つのローレンツ関数と線形項。

## 標準への準拠

スタジオの6つのワークフロー標準に対して、0〜3のスコアを付けて評価。

| 標準 | スコア | 証拠 |
|---|---|---|
| PIN_PER_STEP | 2 | すべての数値選択（ウィンドウ、オーバーラップ、FFTサイズ、キャリブレーション定数、適合バンド、シード）は、`process_month.py`の先頭にある名前付き定数であり、npz `method`フィールドに書き込まれます。まだ、NumPyのバージョン間でバイト単位で再現することはできません。ライブラリのバージョンに関する情報もありません。 |
| アンドン権限 | 2 | `verify_against_granada.py`は、ステーションが公開している適合データと矛盾する場合の停止ポイントです。フェッチスクリプトは、書き込む前に、すべてのzipエントリの展開後のサイズを確認します。 |
| 名前付き補正器 | 2 | パイプライン内に不可逆的な外部呼び出しはありません。唯一の公開パスは、ソースコードのgitプッシュです。`data/`は無視されます。不良の`viewer/index.html`に対する補正器：npzから再ビルドします。 |
| 秘密鍵による分解 | 2 | フェッチ、処理、検証、ビルドは、それぞれ1つのジョブを持つ4つのスクリプトです。ビューアテンプレートは、ステーションに関する情報を一切持たず、ステーションに依存しないJSONブロックを使用します。 |
| 不確実性に基づいた人間によるゲート | 1 | 相関パネルには、不確実性のゲートであるヌルバンドが表示されます。パイプライン自体には、人間によるチェックポイントはありません。修正：検証器に、指定された許容範囲に対して合格/不合格を送信させます（担当：次のセッション）。 |
| 外部検証器 | 3 | 検証器は、ステーションが独自に作成した出力です（異なるコード、異なる作成者、lmfitとSciPy）。上記の表の数値。 |

## 信頼性とデータ

パイプラインは、チェックアウトからローカルで実行されます。`data/`と`viewer/`の下でのみ、読み書きを行います。
ネットワークアクセスは、スクリプトにフェッチを要求した場合にのみ発生します：Zenodo（生のアーカイブ）、Digibug（ステーションの検証器ファイル）、GFZ（Kp）、USGS（地震）。データセットのアップロードには、これらのスクリプトの外で、独自のHugging Faceアカウントにログインする必要があります。資格情報は読み込まれたり保存されたりせず、テレメトリも送信されず、ビューアはThree.jsと2つのフォントをパブリックCDNからロードする静的なページであり、それ以外には何もありません。
要件：NumPy、SciPy、PyArrowを搭載したPython 3.11以降、任意のOS。オプションのランディングページには、Nodeが必要です。

## ライセンス

コードはMITライセンスです。派生データ製品には、そのソースによって必要な帰属表示が含まれます。

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
