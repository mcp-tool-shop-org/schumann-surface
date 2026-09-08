import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'Schumann Surface',
  description: 'Schumann resonance as a 3D time-frequency surface with event lanes and honest lagged cross-correlation, built from the Sierra Nevada ELF station\'s open raw archive.',
  logoBadge: 'SS',
  brandName: 'schumann-surface',
  repoUrl: 'https://github.com/mcp-tool-shop-org/schumann-surface',
  footerText: 'MIT Licensed — built by <a href="https://mcp-tool-shop.github.io/" style="color:var(--color-muted);text-decoration:underline">MCP Tool Shop</a>. Data CC BY 4.0, Salinas et al., University of Granada.',

  hero: {
    badge: 'Open data · open code',
    headline: 'See the Earth ring.',
    headlineAccent: 'Schumann resonance, honestly.',
    description: 'One month of a real ELF station rendered as a 3D surface, a day-stacked volume, a cavity globe and a trajectory, with Kp, night and earthquake lanes and a correlation panel that shows the null band.',
    primaryCta: { href: 'viewer/', label: 'Open the viewer' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      { label: 'Fetch + process + verify one month', code: 'python scripts/pipeline_month.py 1310' },
      { label: 'Build the viewer', code: 'python scripts/build_viewer.py 1310 --main' },
      { label: 'Read the dataset', code: "pd.read_parquet('modes/SN_201310.parquet')" },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'What it shows',
      subtitle: 'Four selectable modes, all kept. Every lane labelled measured or model.',
      features: [
        { title: 'Surface', desc: 'Time × frequency (6–25 Hz) × amplitude in dB re 1 pT/√Hz, NS and EW as stackable sheets, with fitted mode ribbons.' },
        { title: 'Day stack', desc: 'The month folded into hour-of-day × day × frequency, so the daily lightning rhythm becomes a shape you can see.' },
        { title: 'Cavity globe', desc: 'Measured mode amplitudes drive standing-wave patterns on an ionosphere shell; bearing fans from NS/EW polarisation; chimneys on their UTC schedule.' },
        { title: 'Correlation with the null shown', desc: 'Pearson r against lag, with a 95 % band corrected for autocorrelation. A curve inside the band is a null result and is displayed as one.' },
        { title: 'Reproduces the station', desc: 'The chain mirrors the University of Granada processing and matches its published spectra at ratio 1.0000, slot by slot, two months and counting.' },
        { title: 'Public dataset', desc: 'Parquet tables of spectra, mode fits, polarisation and lanes on Hugging Face, CC BY 4.0, with a knowledge base inside.' },
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Usage',
      cards: [
        { title: 'One month, end to end', code: 'pip install numpy scipy pyarrow\npython scripts/pipeline_month.py 1310   # fetch, process, verify, export' },
        { title: 'The daily rhythm from the dataset', code: "import pandas as pd\nmodes = pd.read_parquet('modes/SN_201310.parquet')\nm1 = modes[(modes['mode']==1) & (modes.sensor=='NS') & ~modes.masked]\nm1.groupby(m1.t_utc.dt.hour)['peak'].mean()" },
      ],
    },
  ],
};
