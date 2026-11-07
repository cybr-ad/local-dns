# Script to generate src/web_ui.h and dashboard.html with the ultimate Pitch-Black Cyber Dashboard

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WT32-ETH01 Shield | Pitch-Black Network Monitor & Ad Blocker</title>
  <style>
    :root {
      --bg: #000000;
      --card-bg: #06080d;
      --card-header: #0b0f17;
      --card-border: #141c2c;
      --card-border-glow: #1e293b;
      --accent-green: #00ff9d;
      --accent-green-dim: rgba(0, 255, 157, 0.15);
      --accent-cyan: #00e5ff;
      --accent-cyan-dim: rgba(0, 229, 255, 0.15);
      --accent-red: #ff0055;
      --accent-red-dim: rgba(255, 0, 85, 0.15);
      --accent-purple: #b388ff;
      --accent-purple-dim: rgba(179, 136, 255, 0.15);
      --accent-yellow: #ffd600;
      --text: #f1f5f9;
      --text-muted: #64748b;
      --text-dim: #94a3b8;
      --font-mono: 'Consolas', 'Fira Code', 'Roboto Mono', Monaco, monospace;
      --radius: 10px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* TOP CYBER BAR */
    .topbar {
      background: #020305;
      border-bottom: 1px solid var(--card-border);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .shield-badge {
      background: linear-gradient(135deg, #00ff9d 0%, #00b0ff 100%);
      color: #000;
      padding: 6px 12px;
      border-radius: 6px;
      font-weight: 900;
      font-size: 0.95rem;
      letter-spacing: 1px;
      box-shadow: 0 0 16px rgba(0, 255, 157, 0.35);
    }
    .brand-title {
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      background: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--accent-green);
      animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 157, 0.7); }
      70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(0, 255, 157, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 157, 0); }
    }
    .brand-sub {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    /* REALTIME TRAFFIC METERS */
    .traffic-pill {
      display: flex;
      align-items: center;
      gap: 16px;
      background: #070a12;
      border: 1px solid #1a253a;
      border-radius: 999px;
      padding: 6px 16px;
      font-family: var(--font-mono);
      font-size: 0.8rem;
    }
    .traffic-val {
      font-weight: 700;
    }
    .traffic-down { color: var(--accent-green); }
    .traffic-up { color: var(--accent-cyan); }
    .traffic-total { color: var(--text-dim); border-left: 1px solid #1a253a; padding-left: 12px; }

    /* NAVIGATION TABS */
    .navbar {
      background: #020305;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      padding: 0 24px;
      gap: 4px;
      overflow-x: auto;
    }
    .nav-tab {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 12px 16px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .nav-tab:hover {
      color: var(--text);
    }
    .nav-tab.active {
      color: var(--accent-green);
      border-bottom-color: var(--accent-green);
    }
    .nav-tab.term-btn.active {
      color: var(--accent-cyan);
      border-bottom-color: var(--accent-cyan);
    }

    /* MAIN CONTAINER */
    .main-layout {
      display: flex;
      flex: 1;
      position: relative;
      overflow: hidden;
    }
    .main-content {
      flex: 1;
      padding: 24px;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
      transition: margin-right 0.3s ease;
    }
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
    }

    /* STATS SUMMARY TILES */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat-tile {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 18px;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s;
    }
    .stat-tile:hover {
      border-color: var(--card-border-glow);
    }
    .stat-tile::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--accent-green);
    }
    .stat-tile.red::before { background: var(--accent-red); }
    .stat-tile.cyan::before { background: var(--accent-cyan); }
    .stat-tile.purple::before { background: var(--accent-purple); }
    .stat-tile.yellow::before { background: var(--accent-yellow); }

    .tile-title {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 6px;
      font-weight: 700;
    }
    .tile-num {
      font-size: 2rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.5px;
    }
    .tile-sub {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 4px;
    }

    /* CARD CONTAINERS */
    .panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      margin-bottom: 24px;
      overflow: hidden;
    }
    .panel-head {
      background: var(--card-header);
      padding: 14px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .panel-title {
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-body {
      padding: 20px;
    }

    /* CONTROLS & FILTER ROW */
    .filter-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
      align-items: center;
    }
    .cyber-input {
      background: #04060a;
      border: 1px solid var(--card-border);
      border-radius: 6px;
      color: var(--text);
      padding: 8px 14px;
      font-size: 0.85rem;
      outline: none;
      transition: all 0.2s;
    }
    .cyber-input:focus {
      border-color: var(--accent-green);
      box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
    }
    .cyber-btn {
      background: #0c121e;
      border: 1px solid var(--card-border);
      color: var(--text-dim);
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .cyber-btn:hover {
      background: #141e30;
      color: var(--text);
      border-color: #243552;
    }
    .cyber-btn.active {
      background: var(--accent-green);
      color: #000;
      border-color: var(--accent-green);
      box-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
    }
    .cyber-btn-red {
      background: var(--accent-red-dim);
      color: var(--accent-red);
      border-color: var(--accent-red);
    }
    .cyber-btn-red:hover {
      background: var(--accent-red);
      color: #fff;
    }

    /* ACTIVE FILTER PILL */
    .active-filter-badge {
      display: none;
      background: rgba(0, 229, 255, 0.15);
      border: 1px solid var(--accent-cyan);
      color: var(--accent-cyan);
      padding: 4px 10px;
      border-radius: 999px;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      align-items: center;
      gap: 6px;
    }
    .active-filter-badge.visible {
      display: inline-flex;
    }
    .clear-filter-btn {
      cursor: pointer;
      font-weight: 900;
    }

    /* DATA TABLES */
    .table-container {
      overflow-x: auto;
      border: 1px solid var(--card-border);
      border-radius: 6px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
      text-align: left;
    }
    th {
      background: #04060a;
      padding: 12px 14px;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--card-border);
    }
    td {
      padding: 12px 14px;
      border-bottom: 1px solid #0c121e;
    }
    tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    /* CLICKABLE IP PILL */
    .ip-link {
      font-family: var(--font-mono);
      color: var(--accent-cyan);
      font-weight: 700;
      cursor: pointer;
      background: rgba(0, 229, 255, 0.1);
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid rgba(0, 229, 255, 0.25);
      transition: all 0.2s;
      display: inline-block;
    }
    .ip-link:hover {
      background: var(--accent-cyan);
      color: #000;
      box-shadow: 0 0 12px rgba(0, 229, 255, 0.4);
    }
    .mac-text {
      font-family: var(--font-mono);
      color: var(--text-muted);
      font-size: 0.78rem;
    }

    /* STATUS TAGS */
    .tag {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: 0.5px;
    }
    .tag-blocked {
      background: var(--accent-red-dim);
      color: var(--accent-red);
      border: 1px solid rgba(255, 0, 85, 0.4);
    }
    .tag-allowed {
      background: var(--accent-green-dim);
      color: var(--accent-green);
      border: 1px solid rgba(0, 255, 157, 0.4);
    }
    .tag-cached {
      background: var(--accent-cyan-dim);
      color: var(--accent-cyan);
      border: 1px solid rgba(0, 229, 255, 0.4);
    }

    /* MINI PROGRESS BARS */
    .bar-bg {
      background: #101624;
      border-radius: 999px;
      height: 6px;
      width: 80px;
      display: inline-block;
      vertical-align: middle;
      overflow: hidden;
      margin-right: 8px;
    }
    .bar-fill {
      height: 100%;
      background: var(--accent-red);
      border-radius: 999px;
    }

    /* =========================================================================
       TERMINAL MODE (PITCH-BLACK HACKER CRT TERMINAL)
       ========================================================================= */
    .terminal-box {
      background: #000000;
      border: 1px solid #142032;
      border-radius: var(--radius);
      box-shadow: 0 0 30px rgba(0, 0, 0, 0.9), inset 0 0 20px rgba(0, 229, 255, 0.03);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 620px;
    }
    .terminal-header {
      background: #05080e;
      border-bottom: 1px solid #142032;
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .terminal-title {
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: var(--accent-green);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .term-dots {
      display: flex;
      gap: 6px;
    }
    .term-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .td-red { background: #ff5f56; }
    .td-yellow { background: #ffbd2e; }
    .td-green { background: #27c93f; }

    .terminal-body {
      flex: 1;
      padding: 14px 16px;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      line-height: 1.5;
      color: #94a3b8;
      background: radial-gradient(circle at 50% 50%, #03060a 0%, #000000 100%);
    }
    .term-line {
      display: flex;
      gap: 12px;
      padding: 3px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.02);
      align-items: baseline;
    }
    .term-line:hover {
      background: rgba(0, 229, 255, 0.04);
    }
    .term-time { color: #475569; min-width: 65px; }
    .term-verdict { font-weight: 800; min-width: 75px; }
    .term-verdict.blocked { color: var(--accent-red); }
    .term-verdict.allowed { color: var(--accent-green); }
    .term-verdict.cached { color: var(--accent-cyan); }
    .term-ip { color: var(--accent-cyan); min-width: 110px; cursor: pointer; }
    .term-ip:hover { text-decoration: underline; }
    .term-mac { color: #475569; min-width: 135px; font-size: 0.74rem; }
    .term-domain { color: #f8fafc; flex: 1; word-break: break-all; }
    .term-info { color: #64748b; font-size: 0.74rem; }
    .cursor-blink {
      display: inline-block;
      width: 8px;
      height: 14px;
      background: var(--accent-green);
      vertical-align: middle;
      animation: blink 1s step-end infinite;
      margin-left: 4px;
    }
    @keyframes blink { 50% { opacity: 0; } }

    /* =========================================================================
       RIGHT-SIDE DRAWER / SPLIT INSPECTOR
       ========================================================================= */
    .side-inspector {
      width: 420px;
      background: #04060a;
      border-left: 1px solid var(--card-border);
      position: fixed;
      top: 0;
      right: -440px;
      height: 100vh;
      z-index: 200;
      box-shadow: -10px 0 30px rgba(0, 0, 0, 0.8);
      transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
    }
    .side-inspector.open {
      right: 0;
    }
    .inspector-head {
      background: var(--card-header);
      padding: 16px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .inspector-title {
      font-size: 1rem;
      font-weight: 800;
      color: var(--accent-cyan);
    }
    .close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.4rem;
      cursor: pointer;
      line-height: 1;
      padding: 4px;
    }
    .close-btn:hover { color: #fff; }

    .inspector-body {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
    }
    .inspector-info-card {
      background: #080c14;
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 14px;
      margin-bottom: 18px;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      font-size: 0.82rem;
      border-bottom: 1px solid #0f1624;
    }
    .info-row:last-child { border-bottom: none; }
    .info-label { color: var(--text-muted); }
    .info-val { font-family: var(--font-mono); font-weight: 700; color: var(--text); }

    /* FOOTER */
    footer {
      text-align: center;
      padding: 20px;
      color: var(--text-muted);
      font-size: 0.75rem;
      border-top: 1px solid var(--card-border);
      background: #010204;
      font-family: var(--font-mono);
    }
  </style>
</head>
<body>

  <!-- TOP HEADER -->
  <header class="topbar">
    <div class="brand">
      <div class="shield-badge">SHIELD</div>
      <div>
        <div class="brand-title">
          <span>WT32-ETH01 Network Core</span>
          <div class="pulse-dot"></div>
        </div>
        <div class="brand-sub">Hardware DNS Sinkhole &bull; IP: 107.7.97.95</div>
      </div>
    </div>

    <!-- LIVE WAN/LAN SPEED METER -->
    <div class="traffic-pill">
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:var(--accent-green);font-size:0.75rem;animation:pulse 1.2s infinite;">●</span>
        <span style="color:var(--text-muted);">RX:</span>
        <span class="traffic-val traffic-down" id="hdr-speed-rx">0 B/s</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;">
        <span style="color:var(--text-muted);">TX:</span>
        <span class="traffic-val traffic-up" id="hdr-speed-tx">0 B/s</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;border-left:1px solid #1a253a;padding-left:10px;">
        <span style="color:var(--text-muted);">PKTS:</span>
        <span class="traffic-val" style="color:var(--accent-yellow);" id="hdr-pkts">0</span> <span style="font-size:0.7rem;color:var(--text-muted);">p/s</span>
      </div>
      <div style="display:flex;align-items:center;gap:6px;border-left:1px solid #1a253a;padding-left:10px;">
        <span style="color:var(--text-muted);">PING:</span>
        <span class="traffic-val" style="color:var(--accent-purple);" id="hdr-ping">--</span>
      </div>
      <div class="traffic-total">
        <span style="color:var(--text-muted);">TOTAL:</span>
        <span id="hdr-total-mb" style="font-weight:700;color:var(--text);">0 B</span>
      </div>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <nav class="navbar">
    <button class="nav-tab active" onclick="showTab('dashboard')">📊 Dashboard</button>
    <button class="nav-tab" onclick="showTab('devices')">📱 Network Devices</button>
    <button class="nav-tab term-btn" onclick="showTab('terminal')">📟 Terminal Mode</button>
    <button class="nav-tab" onclick="showTab('queries')">⚡ Live Query Table</button>
    <button class="nav-tab" onclick="showTab('topdomains')">🏆 Top Domains</button>
    <button class="nav-tab" onclick="showTab('upstream')">⚙️ Upstream DNS & WAN</button>
    <button class="nav-tab" onclick="showTab('rules')">🛡️ Rule Manager & Catalog</button>
    <button class="nav-tab" onclick="showTab('guide')">🌐 Router Setup</button>
    
  </nav>

  <div class="main-layout">
    <main class="main-content">

      <!-- =========================================================================
           TAB 1: DASHBOARD OVERVIEW
           ========================================================================= -->
      <section id="pane-dashboard" class="tab-pane active">
        <!-- STATS TILES -->
        <div class="stats-row">
          <div class="stat-tile">
            <div class="tile-title">Total DNS Queries</div>
            <div class="tile-num" id="dash-total">0</div>
            <div class="tile-sub">All network queries handled</div>
          </div>
          <div class="stat-tile red">
            <div class="tile-title">Blocked Ads & Trackers</div>
            <div class="tile-num" id="dash-blocked" style="color:var(--accent-red);">0</div>
            <div class="tile-sub" id="dash-blockrate">0.0% sinkholed to 0.0.0.0</div>
          </div>
          <div class="stat-tile cyan">
            <div class="tile-title">RAM Cache Hits</div>
            <div class="tile-num" id="dash-cached" style="color:var(--accent-cyan);">0</div>
            <div class="tile-sub">Answered in &lt; 1 ms</div>
          </div>
          <div class="stat-tile purple">
            <div class="tile-title">Active Devices</div>
            <div class="tile-num" id="dash-clients" style="color:var(--accent-purple);">0</div>
            <div class="tile-sub">Clients tracked on LAN</div>
          </div>
          <div class="stat-tile yellow">
            <div class="tile-title">Blocklist Rules</div>
            <div class="tile-num" id="dash-rules" style="color:var(--accent-yellow);">413</div>
            <div class="tile-sub" id="dash-rules-sub">413 Built-in + 0 Custom</div>
          </div>
        </div>

        <!-- QUICK SYSTEM STATUS -->
        <div class="panel">
          <div class="panel-head">
            <div class="panel-title">📡 Network Infrastructure Telemetry</div>
            <button class="cyber-btn" onclick="fetchData()">🔄 Poll Now</button>
          </div>
          <div class="panel-body">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:18px; font-size:0.86rem;">
              <div><strong style="color:var(--text-muted);">ESP32 Static IP:</strong> <code style="color:var(--accent-green);">107.7.97.95</code></div>
              <div><strong style="color:var(--text-muted);">Router Gateway:</strong> <code>107.7.97.77</code></div>
              <div><strong style="color:var(--text-muted);">Primary WAN DNS:</strong> <code id="dash-dns1">1.1.1.1</code></div>
              <div><strong style="color:var(--text-muted);">Secondary WAN DNS:</strong> <code id="dash-dns2">8.8.8.8</code></div>
              <div><strong style="color:var(--text-muted);">System Uptime:</strong> <span id="dash-uptime">0s</span></div>
              <div><strong style="color:var(--text-muted);">Free RAM Heap:</strong> <span id="dash-heap">0 KB</span></div>
            </div>
          </div>
        </div>
      
        <!-- LIVE REAL-TIME NETWORK & SINKHOLE ACTIVITY GRAPH -->
        <div class="panel" style="margin-top:20px;">
          <div class="panel-head" style="display:flex; justify-content:space-between; align-items:center;">
            <div class="panel-title" style="display:flex; align-items:center; gap:8px;">
              <span>📈 Live Real-Time DNS Traffic & Latency Stream</span>
              <span style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">(Rolling 45-Second Window)</span>
            </div>
            <div style="display:flex; align-items:center; gap:16px; font-family:var(--font-mono); font-size:0.78rem;">
              <span style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:10px; height:10px; background:var(--accent-green); border-radius:2px; box-shadow:0 0 6px var(--accent-green);"></span>
                <span>Allowed Queries: <strong id="graph-val-allowed" style="color:var(--accent-green);">0/s</strong></span>
              </span>
              <span style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:10px; height:10px; background:var(--accent-red); border-radius:2px; box-shadow:0 0 6px var(--accent-red);"></span>
                <span>Blocked Ads: <strong id="graph-val-blocked" style="color:var(--accent-red);">0/s</strong></span>
              </span>
              <span style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:10px; height:10px; background:var(--accent-cyan); border-radius:2px; box-shadow:0 0 6px var(--accent-cyan);"></span>
                <span>Upstream Ping: <strong id="graph-val-ping" style="color:var(--accent-cyan);">11 ms</strong></span>
              </span>
            </div>
          </div>
          <div class="panel-body" style="padding:15px; position:relative;">
            <canvas id="trafficCanvas" height="150" style="width:100%; height:150px; display:block; background:#04060a; border-radius:6px; border:1px solid #101726;"></canvas>
            <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:6px; padding:0 4px;">
              <span>45s ago</span>
              <span>30s ago</span>
              <span>15s ago</span>
              <span style="color:var(--accent-green);">● Live Now</span>
            </div>
          </div>
        </div>

        <!-- ESP32 HARDWARE HEALTH & RESOURCE MONITOR -->
        <div class="panel" style="margin-top:20px;">
          <div class="panel-head">
            <div class="panel-title">⚡ ESP32 Hardware Health & Silicon Telemetry</div>
            <div style="font-size:0.75rem; color:var(--accent-green); font-family:var(--font-mono);">● ALL CORES HEALTHY</div>
          </div>
          <div class="panel-body">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:20px;">
              
              <!-- RAM / HEAP CARD -->
              <div style="background:#070a12; border:1px solid #162032; border-radius:8px; padding:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
                  <strong style="color:var(--text-dim); font-size:0.85rem;">Free RAM Heap:</strong>
                  <span id="esp-heap-txt" style="font-family:var(--font-mono); font-weight:700; color:var(--accent-green);">-- KB</span>
                </div>
                <div style="background:#101726; border-radius:999px; height:8px; overflow:hidden; margin-bottom:10px;">
                  <div id="esp-heap-bar" style="width:70%; height:100%; background:linear-gradient(90deg, #00ff9d, #00e5ff); border-radius:999px; transition:width 0.4s;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">
                  <span>Min Free: <strong id="esp-min-heap" style="color:var(--text-dim);">-- KB</strong></span>
                  <span>Total: 320 KB</span>
                </div>
              </div>

              <!-- CPU & CLOCK CARD -->
              <div style="background:#070a12; border:1px solid #162032; border-radius:8px; padding:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
                  <strong style="color:var(--text-dim); font-size:0.85rem;">CPU Core Clock:</strong>
                  <span id="esp-cpu-txt" style="font-family:var(--font-mono); font-weight:700; color:var(--accent-cyan);">240 MHz</span>
                </div>
                <div style="font-size:0.82rem; color:var(--text-dim); margin-bottom:6px;">
                  Xtensa® 32-bit LX6 Dual-Core
                </div>
                <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">
                  Core 0: Network / Core 1: DNS & Web
                </div>
              </div>

              <!-- CHIP TEMPERATURE CARD -->
              <div style="background:#070a12; border:1px solid #162032; border-radius:8px; padding:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
                  <strong style="color:var(--text-dim); font-size:0.85rem;">Internal Silicon Temp:</strong>
                  <span id="esp-temp-txt" style="font-family:var(--font-mono); font-weight:700; color:var(--accent-yellow);">-- °C</span>
                </div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                  <span id="esp-temp-badge" class="tag tag-allowed" style="font-size:0.72rem;">Optimal Thermal</span>
                  <span id="esp-temp-f" style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">(-- °F)</span>
                </div>
                <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">
                  Built-in TSENS Diode
                </div>
              </div>

              <!-- FLASH STORAGE CARD -->
              <div style="background:#070a12; border:1px solid #162032; border-radius:8px; padding:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
                  <strong style="color:var(--text-dim); font-size:0.85rem;">Flash Partition (App):</strong>
                  <span id="esp-flash-txt" style="font-family:var(--font-mono); font-weight:700; color:var(--accent-purple);">780 KB / 3.14 MB</span>
                </div>
                <div style="background:#101726; border-radius:999px; height:8px; overflow:hidden; margin-bottom:10px;">
                  <div id="esp-flash-bar" style="width:25%; height:100%; background:linear-gradient(90deg, #b388ff, #7c4dff); border-radius:999px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">
                  <span>huge_app partition</span>
                  <span>75% Free for OTA</span>
                </div>
              </div>

            </div>
          </div>
        </div>

      
        

        
      </section>

      <!-- =========================================================================
           TAB 2: NETWORK DEVICES LIST (WITH MAC & TRAFFIC FILTERING)
           ========================================================================= -->
      <section id="pane-devices" class="tab-pane">
        <div class="panel">
          <div class="panel-head">
            <div class="panel-title">
              <span>📱 Connected Local Devices & Bandwidth</span>
              <span class="active-filter-badge" id="dev-filter-badge">
                Filtering: <span id="dev-filter-ip"></span>
                <span class="clear-filter-btn" onclick="clearFilter()">&times;</span>
              </span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted);">
              Click any IP to inspect live traffic & query stream
            </div>
          </div>
          <div class="panel-body">
            <!-- SORT & FILTER CONTROLS -->
            <div class="filter-bar">
              <span style="font-size:0.8rem; color:var(--text-muted); font-weight:700;">SORT BY:</span>
              <button class="cyber-btn active" id="btn-sort-traffic" onclick="sortDevices('traffic')">⚡ Most Traffic</button>
              <button class="cyber-btn" id="btn-sort-queries" onclick="sortDevices('queries')">📊 Most Queries</button>
              <button class="cyber-btn" id="btn-sort-blocked" onclick="sortDevices('blocked')">🚫 Most Blocked</button>
              <button class="cyber-btn" id="btn-sort-recent" onclick="sortDevices('recent')">⏱️ Most Recent</button>
              <button class="cyber-btn" onclick="scanLan()" style="background:var(--accent-cyan-dim);color:var(--accent-cyan);border-color:var(--accent-cyan);">⚡ Scan LAN Devices</button>
              <input type="text" class="cyber-input" id="dev-search" placeholder="Search IP or MAC..." onkeyup="renderDevicesTable()">
            </div>

            <!-- DEVICES TABLE -->
            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Device IP</th>
                    <th>Hardware MAC Address</th>
                    <th>DNS Traffic</th>
                    <th>Total Queries</th>
                    <th>Blocked Ads</th>
                    <th>Block Rate</th>
                    <th>Last Active</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="devices-tbody">
                  <tr><td colspan="8" style="text-align:center; color:var(--text-muted); padding:30px;">Loading network devices...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- =========================================================================
           TAB 3: TERMINAL MODE (PURE PITCH-BLACK RETRO CRT TERMINAL)
           ========================================================================= -->
      <section id="pane-terminal" class="tab-pane">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-title">
              <div class="term-dots">
                <div class="term-dot td-red"></div>
                <div class="term-dot td-yellow"></div>
                <div class="term-dot td-green"></div>
              </div>
              <span>WT32-ETH01 :: LIVE STREAM TERMINAL</span>
              <span class="active-filter-badge" id="term-filter-badge">
                Target: <span id="term-filter-ip"></span>
                <span class="clear-filter-btn" onclick="clearFilter()">&times;</span>
              </span>
            </div>

            <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
              <label style="font-size:0.75rem; color:var(--text-muted); display:flex; align-items:center; gap:4px; font-family:var(--font-mono);">
                <input type="checkbox" id="term-autoscroll" checked> Auto-Scroll
              </label>
              <button class="cyber-btn" onclick="togglePause()"><span id="btn-pause-text">⏸️ Pause</span></button>
              <button class="cyber-btn" onclick="clearTerminal()">🧹 Clear</button>
              <input type="text" class="cyber-input" id="term-search" placeholder="Filter domain/IP..." style="width:160px;" onkeyup="renderTerminal()">
            </div>
          </div>

          <div class="terminal-body" id="term-content">
            <div class="term-line" style="color:var(--accent-green);">
              <span>[SYSTEM INITIALIZED] Listening on UDP Port 53 &bull; Sinkhole Ready.</span>
            </div>
          </div>
        </div>
      </section>

      <!-- =========================================================================
           TAB 4: LIVE QUERY TABLE
           ========================================================================= -->
      <section id="pane-queries" class="tab-pane">
        <div class="panel">
          <div class="panel-head">
            <div class="panel-title">
              <span>⚡ Live DNS Query Stream</span>
              <span class="active-filter-badge" id="query-filter-badge">
                Target: <span id="query-filter-ip"></span>
                <span class="clear-filter-btn" onclick="clearFilter()">&times;</span>
              </span>
            </div>
            <div style="display:flex; gap:8px;">
              <button class="cyber-btn active" id="flt-all" onclick="setQueryVerdictFilter('all')">All</button>
              <button class="cyber-btn" id="flt-blk" onclick="setQueryVerdictFilter('blocked')">Blocked</button>
              <button class="cyber-btn" id="flt-alw" onclick="setQueryVerdictFilter('allowed')">Allowed</button>
              <button class="cyber-btn" id="flt-cch" onclick="setQueryVerdictFilter('cached')">Cached</button>
            </div>
          </div>
          <div class="panel-body">
            <div class="filter-bar">
              <input type="text" class="cyber-input" id="query-search" placeholder="Search domain, IP or MAC..." style="flex:1;" onkeyup="renderQueriesTable()">
            </div>

            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Client IP</th>
                    <th>MAC Address</th>
                    <th>Requested Domain</th>
                    <th>Type</th>
                    <th>Verdict</th>
                    <th>Latency</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="queries-tbody">
                  <tr><td colspan="8" style="text-align:center; color:var(--text-muted); padding:30px;">Waiting for queries...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- =========================================================================
           TAB 5: TOP DOMAINS
           ========================================================================= -->
      <section id="pane-topdomains" class="tab-pane">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(400px, 1fr)); gap:20px;">
          <!-- TOP ALLOWED -->
          <div class="panel">
            <div class="panel-head">
              <div class="panel-title" style="color:var(--accent-green);">🏆 Top 15 Allowed Domains</div>
            </div>
            <div class="panel-body">
              <div id="top-allowed-list">Loading...</div>
            </div>
          </div>

          <!-- TOP BLOCKED -->
          <div class="panel">
            <div class="panel-head">
              <div class="panel-title" style="color:var(--accent-red);">🚫 Top 15 Blocked Ad Networks</div>
            </div>
            <div class="panel-body">
              <div id="top-blocked-list">Loading...</div>
            </div>
          </div>
        </div>
      </section>

      <!-- =========================================================================
           TAB 6: UPSTREAM DNS & WAN FAILOVER
           ========================================================================= -->
      <section id="pane-upstream" class="tab-pane">
        <div class="panel">
          <div class="panel-head">
            <div class="panel-title">🌐 Dual Upstream DNS & WAN Benchmark</div>
            <button class="cyber-btn" onclick="runBenchmark()">⚡ Benchmark Latency</button>
          </div>
          <div class="panel-body">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:24px;">
              <div class="stat-tile cyan">
                <div class="tile-title">Primary Upstream DNS</div>
                <div class="tile-num" id="up-dns1" style="font-size:1.5rem;">1.1.1.1</div>
                <div class="tile-sub">Cloudflare Secure DNS &bull; Latency: <span id="lat-dns1" style="font-weight:700;">--</span></div>
              </div>
              <div class="stat-tile purple">
                <div class="tile-title">Secondary DNS (Failover)</div>
                <div class="tile-num" id="up-dns2" style="font-size:1.5rem;">8.8.8.8</div>
                <div class="tile-sub">Google Public DNS &bull; Latency: <span id="lat-dns2" style="font-weight:700;">--</span></div>
              </div>
            </div>

                        <!-- QUICK PRESET BUTTONS -->
            <div style="margin-bottom:18px;">
              <span style="font-size:0.8rem; color:var(--text-muted); font-weight:700; display:block; margin-bottom:8px;">RECOMMENDED UPSTREAM DNS PRESETS:</span>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <button class="cyber-btn active" onclick="setDnsPreset('94.140.14.14', '94.140.15.15')" style="font-size:0.75rem;">🛡️ AdGuard DNS (Recommended)</button>
                <button class="cyber-btn" onclick="setDnsPreset('1.1.1.1', '1.0.0.1')" style="font-size:0.75rem;">⚡ Cloudflare</button>
                <button class="cyber-btn" onclick="setDnsPreset('9.9.9.9', '149.112.112.112')" style="font-size:0.75rem;">🔒 Quad9</button>
                <button class="cyber-btn" onclick="setDnsPreset('8.8.8.8', '8.8.4.4')" style="font-size:0.75rem;">🔍 Google</button>
              </div>
            </div>
            <div style="max-width:440px;">
              <div style="margin-bottom:14px;">
                <label style="display:block; font-size:0.8rem; color:var(--text-muted); margin-bottom:4px; font-weight:700;">Primary DNS IP</label>
                <input type="text" class="cyber-input" id="cfg-dns1" value="1.1.1.1" style="width:100%;">
              </div>
              <div style="margin-bottom:14px;">
                <label style="display:block; font-size:0.8rem; color:var(--text-muted); margin-bottom:4px; font-weight:700;">Secondary DNS IP</label>
                <input type="text" class="cyber-input" id="cfg-dns2" value="8.8.8.8" style="width:100%;">
              </div>
              <button class="cyber-btn active" onclick="saveDnsConfig()">💾 Save DNS Settings</button>
            </div>
          </div>
        </div>
      </section>

            <!-- =========================================================================
           TAB 7: COMPLETE RULE MANAGER & BLOCKLIST CATALOG
           ========================================================================= -->
      <section id="pane-rules" class="tab-pane">
        
        <!-- MASTER ENGINE TOGGLE & SOURCE CARD -->
        <div class="panel" style="margin-bottom:20px;">
          <div class="panel-head" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px;">
            <div>
              <div class="panel-title" style="display:flex; align-items:center; gap:10px;">
                <span>🛡️ DNS Sinkhole Engine & Rule Controller</span>
                <span id="master-status-badge" class="tag tag-allowed">ENABLED (ACTIVE)</span>
              </div>
              <div style="font-size:0.8rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">
                Active Shield: <strong id="rules-active-count" style="color:var(--accent-green);">413 Built-in Rules</strong> &bull; 
                Custom Blacklist: <strong id="rules-custom-count" style="color:var(--accent-red);">0</strong> &bull; 
                Whitelisted Bypasses: <strong id="rules-white-count" style="color:var(--accent-cyan);">0</strong>
              </div>
            </div>
            <div style="display:flex; gap:10px;">
              <button id="btn-toggle-engine" class="cyber-btn active" onclick="toggleEngine()" style="font-weight:700; padding:8px 18px; border-radius:6px;">⏸️ Pause Ad Shield</button>
            </div>
          </div>
          <div class="panel-body">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; font-size:0.82rem; color:var(--text-dim);">
              <div style="background:#070a12; border:1px solid #141c2c; border-radius:6px; padding:12px;">
                <strong style="color:var(--accent-green); display:block; margin-bottom:4px;">Official Sources:</strong>
                Steven Black Unified Hosts, AdGuard DNS Base, Peter Lowe's List, Windows Telemetry Blocklist.
              </div>
              <div style="background:#070a12; border:1px solid #141c2c; border-radius:6px; padding:12px;">
                <strong style="color:var(--accent-cyan); display:block; margin-bottom:4px;">Storage Location:</strong>
                Pre-compiled ROM Flash (PROGMEM) with O(log N) binary search lookup (&lt;1 microsecond).
              </div>
              <div style="background:#070a12; border:1px solid #141c2c; border-radius:6px; padding:12px;">
                <strong style="color:var(--accent-purple); display:block; margin-bottom:4px;">Sinkhole Action:</strong>
                Matching queries immediately return <code>0.0.0.0</code> (NXDOMAIN for ads, clean for real sites).
              </div>
            </div>
          </div>
        </div>

        <!-- BUILT-IN RULE CATALOG BROWSER & LIVE FILTER -->
        <div class="panel" style="margin-bottom:20px;">
          <div class="panel-head" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div class="panel-title">
              <span>📚 Comprehensive Rule Catalog & Live Inspector</span>
              <span id="rules-match-count" style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono); font-weight:normal;">(Showing 413 rules)</span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted);">
              Browse, search, or 1-click whitelist any domain in the blocklist
            </div>
          </div>
          <div class="panel-body">
            <!-- CATEGORY FILTER BUTTONS -->
            <div class="filter-bar" style="margin-bottom:12px; display:flex; flex-wrap:wrap; gap:6px;">
              <span style="font-size:0.8rem; color:var(--text-muted); font-weight:700; align-self:center; margin-right:4px;">DEVICE FILTER:</span>
              <button class="cyber-btn active" id="btn-cat-all" onclick="filterRuleCategory('all')">All Rules (413)</button>
              <button class="cyber-btn" id="btn-cat-mobile" onclick="filterRuleCategory('mobile')">📱 Android & iPhone</button>
              <button class="cyber-btn" id="btn-cat-winlinux" onclick="filterRuleCategory('winlinux')">🖥️ Windows & Linux</button>
              <button class="cyber-btn" id="btn-cat-tuya" onclick="filterRuleCategory('tuya')">🏠 Tuya Smart Home</button>
              <button class="cyber-btn" id="btn-cat-ads" onclick="filterRuleCategory('ads')">📢 Ad Networks</button>
              <button class="cyber-btn" id="btn-cat-track" onclick="filterRuleCategory('track')">👁️ Trackers & Analytics</button>
              <button class="cyber-btn" id="btn-cat-social" onclick="filterRuleCategory('social')">💬 Social Pixels</button>
            </div>

            <!-- SEARCH BAR -->
            <div style="display:flex; gap:10px; margin-bottom:14px;">
              <input type="text" class="cyber-input" id="rule-search" placeholder="Type to search rules (e.g. doubleclick, samsung, microsoft, telemetry, google)..." onkeyup="renderRulesTable()" style="flex:1;">
              <button class="cyber-btn" onclick="document.getElementById('rule-search').value=''; renderRulesTable();">Clear</button>
            </div>

            <!-- RULE BROWSER TABLE -->
            <div class="table-container" style="max-height:380px; overflow-y:auto;">
              <table>
                <thead>
                  <tr>
                    <th>Blocked Domain Pattern</th>
                    <th>Threat Category</th>
                    <th>Source Database</th>
                    <th>Current Status</th>
                    <th>Quick Action</th>
                  </tr>
                </thead>
                <tbody id="rules-tbody">
                  <tr><td colspan="5" style="text-align:center; padding:20px; color:var(--text-muted);">Loading rule catalog...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- CUSTOM RULES: WHITELIST & BLACKLIST SIDE-BY-SIDE -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(380px, 1fr)); gap:20px;">
          
          <!-- CUSTOM WHITELIST (NEVER BLOCK) -->
          <div class="panel">
            <div class="panel-head" style="display:flex; justify-content:space-between; align-items:center;">
              <div class="panel-title" style="color:var(--accent-green);">✅ Custom Whitelist (Bypass Filter)</div>
              <button class="cyber-btn" onclick="clearList('white')" style="font-size:0.7rem; padding:2px 8px; color:var(--accent-red);" title="Clear all custom whitelist rules">&times; Clear All</button>
            </div>
            <div class="panel-body">
              <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:12px;">
                Whitelisted domains will <strong>never be blocked</strong>, even if they appear in the built-in threat blocklist.
              </p>
              
              <!-- Quick Single Add -->
              <div style="display:flex; gap:8px; margin-bottom:10px;">
                <input type="text" class="cyber-input" id="add-wl-domain" placeholder="e.g. tracking.mywork.com or example.com" onkeydown="if(event.key==='Enter') addRule('white')" style="flex:1;">
                <button class="cyber-btn active" onclick="addRule('white')">+ Whitelist</button>
              </div>

              <!-- Upload File & Bulk Paste Actions -->
              <div style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap;">
                <input type="file" id="wl-file-input" accept=".txt,.hosts,.conf,text/plain" style="display:none;" onchange="handleFileUpload(event, 'white')">
                <button class="cyber-btn" onclick="document.getElementById('wl-file-input').click()" style="font-size:0.75rem; padding:4px 10px;">📁 Upload .txt File</button>
                <button class="cyber-btn" onclick="toggleBulkModal('white')" style="font-size:0.75rem; padding:4px 10px;">📋 Bulk Paste Text</button>
              </div>

              <!-- Bulk Input & File Upload Container -->
              <div id="bulk-box-white" style="display:none; background:#070a12; border:1px solid #1c263c; border-radius:6px; padding:10px; margin-bottom:12px;">
                <div id="file-info-white" style="display:none; font-size:0.75rem; color:var(--accent-green); font-family:var(--font-mono); margin-bottom:6px;"></div>
                <textarea id="bulk-input-white" class="cyber-input" placeholder="Paste domains or hosts file lines to whitelist (one per line)..." style="width:100%; height:90px; font-family:var(--font-mono); font-size:0.75rem; box-sizing:border-box; margin-bottom:8px;"></textarea>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <button class="cyber-btn active" onclick="importBulkRules('white')" id="btn-import-white">🚀 Import & Whitelist All</button>
                  <span id="bulk-status-white" style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);"></span>
                </div>
              </div>

              <!-- Whitelist Rules List -->
              <div id="wl-container" style="max-height:220px; overflow-y:auto;">Loading whitelist...</div>
            </div>
          </div>

          <!-- CUSTOM BLACKLIST (ALWAYS SINKHOLE) -->
          <div class="panel">
            <div class="panel-head" style="display:flex; justify-content:space-between; align-items:center;">
              <div class="panel-title" style="color:var(--accent-red);">🚫 Custom Blacklist (Extra Block Rules)</div>
              <button class="cyber-btn" onclick="clearList('block')" style="font-size:0.7rem; padding:2px 8px; color:var(--accent-red);" title="Clear all custom blacklist rules">&times; Clear All</button>
            </div>
            <div class="panel-body">
              <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:12px;">
                Add custom domains, ads, or tracking servers to sinkhole across your entire local network.
              </p>
              
              <!-- Quick Single Add -->
              <div style="display:flex; gap:8px; margin-bottom:10px;">
                <input type="text" class="cyber-input" id="add-bl-domain" placeholder="e.g. annoying-adserver.com" onkeydown="if(event.key==='Enter') addRule('block')" style="flex:1;">
                <button class="cyber-btn cyber-btn-red" onclick="addRule('block')">+ Block</button>
              </div>

              <!-- Upload File & Bulk Paste Actions -->
              <div style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap;">
                <input type="file" id="bl-file-input" accept=".txt,.hosts,.conf,text/plain" style="display:none;" onchange="handleFileUpload(event, 'block')">
                <button class="cyber-btn" onclick="document.getElementById('bl-file-input').click()" style="font-size:0.75rem; padding:4px 10px;">📁 Upload .txt File</button>
                <button class="cyber-btn" onclick="toggleBulkModal('block')" style="font-size:0.75rem; padding:4px 10px;">📋 Bulk Paste Text</button>
              </div>

              <!-- Bulk Input & File Upload Container -->
              <div id="bulk-box-block" style="display:none; background:#070a12; border:1px solid #1c263c; border-radius:6px; padding:10px; margin-bottom:12px;">
                <div id="file-info-block" style="display:none; font-size:0.75rem; color:var(--accent-green); font-family:var(--font-mono); margin-bottom:6px;"></div>
                <textarea id="bulk-input-block" class="cyber-input" placeholder="Paste domains or hosts file lines here (e.g. 0.0.0.0 ad.server.com or ||badsite.com^)..." style="width:100%; height:90px; font-family:var(--font-mono); font-size:0.75rem; box-sizing:border-box; margin-bottom:8px;"></textarea>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <button class="cyber-btn cyber-btn-red" onclick="importBulkRules('block')" id="btn-import-block">🚀 Import & Block All</button>
                  <span id="bulk-status-block" style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);"></span>
                </div>
              </div>

              <!-- Blacklist Rules List -->
              <div id="bl-container" style="max-height:220px; overflow-y:auto;">Loading blacklist...</div>
            </div>
          </div>
              <div id="bl-container" style="max-height:220px; overflow-y:auto;">Loading blacklist...</div>
            </div>
          </div>

        </div>
      </section>

    
      <!-- TAB 8: ROUTER SETUP GUIDE -->
      <section id="pane-guide" class="tab-pane">
        <div class="cyber-card">
          <div class="card-header">
            <h3>🌐 Network-Wide Ad Protection: TP-Link Archer AX50 Setup Guide</h3>
          </div>
          <div class="card-body" style="font-size:0.9rem; line-height:1.7;">
            <p style="color:var(--text-dim); margin-bottom:18px;">
              To protect <strong>every smartphone, laptop, smart TV, and gaming console</strong> across your entire Wi-Fi network and monitor all network traffic, configure your router to use the WT32-ETH01 as its primary DNS resolver:
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:18px; margin-bottom:20px;">
              <div style="background:#070a12; border:1px solid #1a253a; border-radius:8px; padding:18px;">
                <div style="font-weight:700; color:var(--accent-green); margin-bottom:8px; font-size:1rem;">Step 1: Open Router Admin</div>
                <div style="color:var(--text-dim); font-size:0.85rem;">
                  Open <a href="http://107.7.97.77" target="_blank" style="color:var(--accent-cyan); text-decoration:underline;">http://107.7.97.77</a> (Archer AX50 Web Management) in your browser and log in.
                </div>
              </div>

              <div style="background:#070a12; border:1px solid #1a253a; border-radius:8px; padding:18px;">
                <div style="font-weight:700; color:var(--accent-cyan); margin-bottom:8px; font-size:1rem;">Step 2: Navigate to DHCP Settings</div>
                <div style="color:var(--text-dim); font-size:0.85rem;">
                  Go to <strong>Advanced</strong> &rarr; <strong>Network</strong> &rarr; <strong>DHCP Server</strong>.
                </div>
              </div>

              <div style="background:#070a12; border:1px solid #1a253a; border-radius:8px; padding:18px;">
                <div style="font-weight:700; color:var(--accent-yellow); margin-bottom:8px; font-size:1rem;">Step 3: Set Primary DNS</div>
                <div style="color:var(--text-dim); font-size:0.85rem;">
                  Set <strong>Primary DNS</strong>: <code style="color:#00ff9d; font-weight:700; background:#0e1726; padding:2px 8px; border-radius:4px;">107.7.97.95</code><br>
                  Leave <em>Secondary DNS</em> blank or set to <code>0.0.0.0</code>.
                </div>
              </div>

              <div style="background:#070a12; border:1px solid #1a253a; border-radius:8px; padding:18px;">
                <div style="font-weight:700; color:var(--accent-purple); margin-bottom:8px; font-size:1rem;">Step 4: Save & Apply</div>
                <div style="color:var(--text-dim); font-size:0.85rem;">
                  Click <strong>Save</strong>. Connected devices will instantly receive the new DNS and all ads and malicious telemetry across your whole network will be blocked!
                </div>
              </div>
            </div>

            <div style="display:flex; justify-content:flex-end;">
              <button class="cyber-btn primary" onclick="showTab('devices')">View Connected Devices &rarr;</button>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- =========================================================================
         RIGHT-SIDE DRAWER / SPLIT INSPECTOR FOR CLICKED IP
         ========================================================================= -->
    <aside class="side-inspector" id="side-inspector">
      <div class="inspector-head">
        <div class="inspector-title" id="insp-header-ip">107.7.97.82</div>
        <button class="close-btn" onclick="closeInspector()">&times;</button>
      </div>

      <div class="inspector-body">
        <div class="inspector-info-card">
          <div class="info-row">
            <span class="info-label">Hardware MAC:</span>
            <span class="info-val" id="insp-mac">--</span>
          </div>
          <div class="info-row">
            <span class="info-label">Total Queries:</span>
            <span class="info-val" id="insp-total">0</span>
          </div>
          <div class="info-row">
            <span class="info-label">Blocked Ads:</span>
            <span class="info-val" id="insp-blocked" style="color:var(--accent-red);">0</span>
          </div>
          <div class="info-row">
            <span class="info-label">Block Percentage:</span>
            <span class="info-val" id="insp-rate">0.0%</span>
          </div>
          <div class="info-row">
            <span class="info-label">Total Traffic:</span>
            <span class="info-val" id="insp-bytes">0 KB</span>
          </div>
          <div class="info-row">
            <span class="info-label">Last Active:</span>
            <span class="info-val" id="insp-seen">Just now</span>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <strong style="font-size:0.85rem;">Live Activity for this Device</strong>
          <button class="cyber-btn" onclick="showTab('terminal')" style="font-size:0.74rem;">📟 Open in Terminal</button>
        </div>

        <div id="insp-queries-stream" style="font-family:var(--font-mono); font-size:0.76rem;">
          <!-- Filtered queries for this device -->
        </div>
      </div>
    </aside>
  </div>

  <footer>
    WT32-ETH01 HARDWARE AD SHIELD &bull; DUAL-CORE ESP32 240MHZ &bull; LAN8720A 100MBPS FULL DUPLEX &bull; SINKHOLE 0.0.0.0
  </footer>

  <script>
    // Global state
    let state = {
      filterIp: null,
      deviceSort: 'traffic',
      queryVerdictFilter: 'all',
      isPaused: false,
      clients: [],
      logs: [],
      stats: {},
      topDomains: { allowed: [], blocked: [] }
    };

    // Format helpers
    function formatBytes(bytes) {
      if (!bytes || bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return (bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
    }

    function formatSpeed(bytesPerSec) {
      if (!bytesPerSec || bytesPerSec === 0) return '0 B/s';
      if (bytesPerSec < 1024) return bytesPerSec + ' B/s';
      const kb = bytesPerSec / 1024;
      if (kb < 1000) return kb.toFixed(1) + ' KB/s';
      return (kb / 1024).toFixed(2) + ' MB/s';
    }

    function timeAgo(sec) {
      if (sec === undefined || sec === null) return '--';
      if (sec < 5) return 'Just now';
      if (sec < 60) return sec + 's ago';
      const m = Math.floor(sec / 60);
      if (m < 60) return m + 'm ago';
      return Math.floor(m / 60) + 'h ago';
    }

    // Tab Navigation
    function showTab(paneId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      
      const targetPane = document.getElementById('pane-' + paneId);
      if (targetPane) targetPane.classList.add('active');

      const tabs = document.querySelectorAll('.nav-tab');
      tabs.forEach(tab => {
        if (tab.getAttribute('onclick') && tab.getAttribute('onclick').includes(paneId)) {
          tab.classList.add('active');
        }
      });
    }

    // Filter by IP (Clicking any IP)
    function inspectIp(ip) {
      state.filterIp = ip;
      
      // Update badges
      document.querySelectorAll('.active-filter-badge').forEach(b => b.classList.add('visible'));
      ['dev-filter-ip', 'term-filter-ip', 'query-filter-ip'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = ip;
      });

      // Update inspector drawer data
      const client = state.clients.find(c => c.ip === ip);
      document.getElementById('insp-header-ip').innerText = ip;
      document.getElementById('insp-mac').innerText = client ? (client.mac || '--') : '--';
      document.getElementById('insp-total').innerText = client ? client.total : '0';
      document.getElementById('insp-blocked').innerText = client ? client.blocked : '0';
      document.getElementById('insp-rate').innerText = client ? (client.rate + '%') : '0.0%';
      document.getElementById('insp-bytes').innerText = client ? formatBytes(client.bytes) : '0 B';
      document.getElementById('insp-seen').innerText = client ? timeAgo(client.seen) : '--';

      // Render inspector filtered queries
      renderInspectorQueries(ip);

      // Slide out inspector
      document.getElementById('side-inspector').classList.add('open');

      // Also update tables
      renderQueriesTable();
      renderTerminal();
      renderDevicesTable();
    }

    function closeInspector() {
      document.getElementById('side-inspector').classList.remove('open');
    }

    function clearFilter() {
      state.filterIp = null;
      document.querySelectorAll('.active-filter-badge').forEach(b => b.classList.remove('visible'));
      closeInspector();
      renderQueriesTable();
      renderTerminal();
      renderDevicesTable();
    }

    // Sort devices
    function sortDevices(method) {
      state.deviceSort = method;
      document.querySelectorAll('#btn-sort-traffic, #btn-sort-queries, #btn-sort-blocked, #btn-sort-recent')
        .forEach(b => b.classList.remove('active'));
      
      const activeBtn = document.getElementById('btn-sort-' + method);
      if (activeBtn) activeBtn.classList.add('active');
      renderDevicesTable();
    }

    function renderDevicesTable() {
      const tbody = document.getElementById('devices-tbody');
      if (!tbody) return;

      let list = [...state.clients];
      const q = (document.getElementById('dev-search')?.value || '').toLowerCase();
      if (q) {
        list = list.filter(c => (c.ip && c.ip.toLowerCase().includes(q)) || (c.mac && c.mac.toLowerCase().includes(q)));
      }

      // Sort
      if (state.deviceSort === 'traffic') {
        list.sort((a, b) => (b.bytes || 0) - (a.bytes || 0));
      } else if (state.deviceSort === 'queries') {
        list.sort((a, b) => (b.total || 0) - (a.total || 0));
      } else if (state.deviceSort === 'blocked') {
        list.sort((a, b) => (b.blocked || 0) - (a.blocked || 0));
      } else if (state.deviceSort === 'recent') {
        list.sort((a, b) => (a.seen || 0) - (b.seen || 0));
      }

      if (list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:var(--text-muted); padding:24px;">No matching devices found</td></tr>';
        return;
      }

      tbody.innerHTML = list.map(c => `
        <tr style="${state.filterIp === c.ip ? 'background:rgba(0,229,255,0.06);' : ''}">
          <td><span class="ip-link" onclick="inspectIp('${c.ip}')">${c.ip}</span></td>
          <td><span class="mac-text">${c.mac || '--'}</span></td>
          <td style="font-family:var(--font-mono); font-weight:700; color:var(--accent-green);">${formatBytes(c.bytes)}</td>
          <td style="font-family:var(--font-mono);">${c.total}</td>
          <td style="font-family:var(--font-mono); color:var(--accent-red); font-weight:700;">${c.blocked}</td>
          <td>
            <div class="bar-bg"><div class="bar-fill" style="width:${Math.min(100, c.rate)}%;"></div></div>
            <span style="font-family:var(--font-mono); font-size:0.75rem;">${c.rate}%</span>
          </td>
          <td style="font-size:0.78rem; color:var(--text-muted);">${timeAgo(c.seen)}</td>
          <td>
            <button class="cyber-btn" onclick="inspectIp('${c.ip}')" style="padding:4px 8px; font-size:0.72rem;">Inspect &rarr;</button>
          </td>
        </tr>
      `).join('');
    }

    // Terminal Mode Render
    function renderTerminal() {
      const container = document.getElementById('term-content');
      if (!container) return;

      let logs = [...state.logs];
      if (state.filterIp) {
        logs = logs.filter(l => l.ip === state.filterIp);
      }
      const q = (document.getElementById('term-search')?.value || '').toLowerCase();
      if (q) {
        logs = logs.filter(l => l.domain.toLowerCase().includes(q) || l.ip.includes(q) || (l.mac && l.mac.toLowerCase().includes(q)));
      }

      if (logs.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); padding:10px;">No terminal entries match current filter.</div>';
        return;
      }

      container.innerHTML = logs.map(l => {
        let vClass = 'allowed';
        let vText = '[ALLOW]';
        let detail = `(${l.ms}ms &bull; WAN)`;
        if (l.verdict === 1) {
          vClass = 'blocked';
          vText = '[BLOCK]';
          detail = `(0ms &bull; SINKHOLE 0.0.0.0)`;
        } else if (l.verdict === 2) {
          vClass = 'cached';
          vText = '[CACHE]';
          detail = `(0ms &bull; MEMORY)`;
        }
        return `
          <div class="term-line">
            <span class="term-time">${timeAgo(l.ago)}</span>
            <span class="term-verdict ${vClass}">${vText}</span>
            <span class="term-ip" onclick="inspectIp('${l.ip}')">${l.ip}</span>
            <span class="term-mac">${l.mac || '--'}</span>
            <span class="term-domain">${l.domain}</span>
            <span class="term-info">${detail}</span>
          </div>
        `;
      }).join('') + '<div style="margin-top:6px; color:var(--accent-green);"><span class="cursor-blink"></span></div>';

      if (document.getElementById('term-autoscroll')?.checked) {
        container.scrollTop = container.scrollHeight;
      }
    }

    function clearTerminal() {
      document.getElementById('term-content').innerHTML = '<div style="color:var(--text-muted); padding:10px;">Terminal cleared. Waiting for queries...</div>';
    }

    function togglePause() {
      state.isPaused = !state.isPaused;
      document.getElementById('btn-pause-text').innerText = state.isPaused ? '▶️ Resume' : '⏸️ Pause';
    }

    // Live Query Table Render
    function setQueryVerdictFilter(f) {
      state.queryVerdictFilter = f;
      document.querySelectorAll('#flt-all, #flt-blk, #flt-alw, #flt-cch').forEach(b => b.classList.remove('active'));
      const btnMap = { 'all': 'flt-all', 'blocked': 'flt-blk', 'allowed': 'flt-alw', 'cached': 'flt-cch' };
      if (btnMap[f]) document.getElementById(btnMap[f]).classList.add('active');
      renderQueriesTable();
    }

    function renderQueriesTable() {
      const tbody = document.getElementById('queries-tbody');
      if (!tbody) return;

      let list = [...state.logs];
      if (state.filterIp) {
        list = list.filter(l => l.ip === state.filterIp);
      }
      if (state.queryVerdictFilter === 'blocked') {
        list = list.filter(l => l.verdict === 1);
      } else if (state.queryVerdictFilter === 'allowed') {
        list = list.filter(l => l.verdict === 0);
      } else if (state.queryVerdictFilter === 'cached') {
        list = list.filter(l => l.verdict === 2);
      }

      const q = (document.getElementById('query-search')?.value || '').toLowerCase();
      if (q) {
        list = list.filter(l => l.domain.toLowerCase().includes(q) || l.ip.includes(q) || (l.mac && l.mac.toLowerCase().includes(q)));
      }

      if (list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:var(--text-muted); padding:24px;">No queries match filter</td></tr>';
        return;
      }

      tbody.innerHTML = list.map(l => {
        let tag = '<span class="tag tag-allowed">ALLOWED</span>';
        if (l.verdict === 1) tag = '<span class="tag tag-blocked">BLOCKED</span>';
        else if (l.verdict === 2) tag = '<span class="tag tag-cached">CACHED</span>';

        return `
          <tr style="${state.filterIp === l.ip ? 'background:rgba(0,229,255,0.06);' : ''}">
            <td style="color:var(--text-muted); font-size:0.75rem;">${timeAgo(l.ago)}</td>
            <td><span class="ip-link" onclick="inspectIp('${l.ip}')">${l.ip}</span></td>
            <td><span class="mac-text">${l.mac || '--'}</span></td>
            <td style="font-family:var(--font-mono); font-weight:600; color:#fff;">${l.domain}</td>
            <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted);">${l.type === 28 ? 'AAAA' : 'A'}</td>
            <td>${tag}</td>
            <td style="font-family:var(--font-mono); font-size:0.75rem;">${l.ms}ms</td>
            <td>
              <button class="cyber-btn" onclick="inspectIp('${l.ip}')" style="padding:3px 7px; font-size:0.7rem;">Filter</button>
            </td>
          </tr>
        `;
      }).join('');
    }

    // Inspector Stream Render
    function renderInspectorQueries(ip) {
      const container = document.getElementById('insp-queries-stream');
      if (!container) return;

      const filtered = state.logs.filter(l => l.ip === ip);
      if (filtered.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); padding:10px 0;">No recent queries from this device.</div>';
        return;
      }

      container.innerHTML = filtered.map(l => {
        let color = 'var(--accent-green)';
        let lbl = 'ALLOW';
        if (l.verdict === 1) { color = 'var(--accent-red)'; lbl = 'BLOCK'; }
        else if (l.verdict === 2) { color = 'var(--accent-cyan)'; lbl = 'CACHE'; }

        return `
          <div style="padding:7px 0; border-bottom:1px solid #101624; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <span style="color:${color}; font-weight:800; margin-right:6px;">[${lbl}]</span>
              <span style="color:#fff;">${l.domain}</span>
            </div>
            <span style="color:var(--text-muted); font-size:0.7rem;">${timeAgo(l.ago)}</span>
          </div>
        `;
      }).join('');
    }

    // Top Domains Render
    function renderTopDomains() {
      const alwBox = document.getElementById('top-allowed-list');
      const blkBox = document.getElementById('top-blocked-list');

      if (alwBox && state.topDomains.allowed) {
        alwBox.innerHTML = state.topDomains.allowed.map((d, i) => `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #0f1624; font-size:0.84rem;">
            <span><strong style="color:var(--text-muted); margin-right:8px;">#${i+1}</strong> <code style="color:#fff;">${d.domain}</code></span>
            <span class="tag tag-allowed">${d.count} hits</span>
          </div>
        `).join('') || '<div style="color:var(--text-muted);">No domains recorded yet.</div>';
      }

      if (blkBox && state.topDomains.blocked) {
        blkBox.innerHTML = state.topDomains.blocked.map((d, i) => `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #0f1624; font-size:0.84rem;">
            <span><strong style="color:var(--text-muted); margin-right:8px;">#${i+1}</strong> <code style="color:var(--accent-red);">${d.domain}</code></span>
            <span class="tag tag-blocked">${d.count} blocks</span>
          </div>
        `).join('') || '<div style="color:var(--text-muted);">No ads blocked yet.</div>';
      }
    }

    // API Base URL (Supports opening dashboard.html directly from local file)
    const API_BASE = (window.location.protocol === 'file:') ? 'http://107.7.97.95' : '';

    // Detect local file:// protocol (Chrome blocks local files from making HTTP calls to LAN IPs)
    if (window.location.protocol === 'file:') {
      window.addEventListener('DOMContentLoaded', () => {
        const banner = document.createElement('div');
        banner.style.cssText = "background:linear-gradient(90deg, #ff1744, #7c4dff); color:#fff; padding:12px 20px; text-align:center; font-weight:700; font-size:0.9rem; position:sticky; top:0; z-index:99999; box-shadow:0 4px 20px rgba(0,0,0,0.6); display:flex; justify-content:center; align-items:center; gap:12px; flex-wrap:wrap;";
        banner.innerHTML = '<span>⚠️ Chrome blocks local files (file://) from reading LAN data.</span> <a href="http://107.7.97.95/" style="background:#00ff9d; color:#04060a; padding:6px 16px; border-radius:6px; text-decoration:none; font-weight:800; box-shadow:0 0 10px #00ff9d;">👉 Switch to Tab 2 (http://107.7.97.95/)</a>';
        document.body.prepend(banner);
      });
    }

    
    // Real-Time Graph History Buffer (30 points = 45 seconds at 1.5s intervals)
    const MAX_GRAPH_POINTS = 30;
    const graphHistory = {
      allowed: new Array(MAX_GRAPH_POINTS).fill(0),
      blocked: new Array(MAX_GRAPH_POINTS).fill(0),
      ping: new Array(MAX_GRAPH_POINTS).fill(12)
    };

    let prevTotal = 0;
    let prevBlocked = 0;

    function updateChart(stats) {
      const curTotal = stats.total || 0;
      const curBlocked = stats.blocked || 0;
      const curPing = stats.pingMs || 11;

      let deltaAllowed = 0;
      let deltaBlocked = 0;

      if (prevTotal > 0 && curTotal >= prevTotal) {
        const deltaTotal = curTotal - prevTotal;
        deltaBlocked = Math.max(0, curBlocked - prevBlocked);
        deltaAllowed = Math.max(0, deltaTotal - deltaBlocked);
      }

      prevTotal = curTotal;
      prevBlocked = curBlocked;

      // Push to history
      graphHistory.allowed.shift();
      graphHistory.allowed.push(deltaAllowed);

      graphHistory.blocked.shift();
      graphHistory.blocked.push(deltaBlocked);

      graphHistory.ping.shift();
      graphHistory.ping.push(curPing);

      // Update text indicators
      const elAlw = document.getElementById('graph-val-allowed');
      const elBlk = document.getElementById('graph-val-blocked');
      const elPng = document.getElementById('graph-val-ping');
      if (elAlw) elAlw.innerText = deltaAllowed + '/s';
      if (elBlk) elBlk.innerText = deltaBlocked + '/s';
      if (elPng) elPng.innerText = curPing + ' ms';

      renderCanvasGraph();
    }

    function renderCanvasGraph() {
      const canvas = document.getElementById('trafficCanvas');
      if (!canvas) return;

      // Handle high-DPI crisp rendering
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const width = rect.width;
      const height = rect.height;

      if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
        canvas.width = width * dpr;
        canvas.height = height * dpr;
      }

      const ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Clear Canvas
      ctx.fillStyle = '#04060a';
      ctx.fillRect(0, 0, width, height);

      // Draw Grid Lines
      ctx.strokeStyle = '#0d1522';
      ctx.lineWidth = 1;
      for (let y = 30; y < height; y += 30) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Max value for scaling
      const maxVal = Math.max(5, ...graphHistory.allowed, ...graphHistory.blocked);
      const stepX = width / (MAX_GRAPH_POINTS - 1);

      // Draw Series Helper
      function drawSeries(data, strokeColor, fillColor) {
        ctx.beginPath();
        for (let i = 0; i < data.length; i++) {
          const x = i * stepX;
          const y = height - 12 - ((data[i] / maxVal) * (height - 30));
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }

        if (fillColor) {
          ctx.lineTo(width, height);
          ctx.lineTo(0, height);
          ctx.closePath();
          ctx.fillStyle = fillColor;
          ctx.fill();
        }

        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 2;
        ctx.shadowColor = strokeColor;
        ctx.shadowBlur = 8;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // 1. Draw Allowed (Green with subtle glow gradient)
      const gradGreen = ctx.createLinearGradient(0, 0, 0, height);
      gradGreen.addColorStop(0, 'rgba(0, 255, 157, 0.18)');
      gradGreen.addColorStop(1, 'rgba(0, 255, 157, 0.0)');
      drawSeries(graphHistory.allowed, '#00ff9d', gradGreen);

      // 2. Draw Blocked (Neon Pink/Red)
      const gradRed = ctx.createLinearGradient(0, 0, 0, height);
      gradRed.addColorStop(0, 'rgba(255, 0, 85, 0.25)');
      gradRed.addColorStop(1, 'rgba(255, 0, 85, 0.0)');
      drawSeries(graphHistory.blocked, '#ff0055', gradRed);
    }

    // Poll API Data
    async function fetchData() {
      if (state.isPaused) return;

      try {
        let tData;
        try {
          tData = await fetch(API_BASE + '/api/telemetry').then(r => r.json());
        } catch (err) {
          const [statsRes, logsRes, clientsRes, topRes] = await Promise.all([
            fetch(API_BASE + '/api/stats').then(r => r.json()),
            fetch(API_BASE + '/api/logs').then(r => r.json()),
            fetch(API_BASE + '/api/clients').then(r => r.json()),
            fetch(API_BASE + '/api/top_domains').then(r => r.json())
          ]);
          tData = { stats: statsRes, logs: logsRes, clients: clientsRes, topDomains: topRes };
        }

        const statsRes = tData.stats;
        state.stats = statsRes;
        if (statsRes.blocking !== undefined) {
          isBlockingEnabled = statsRes.blocking;
          updateEngineUI();
        }
        state.logs = tData.logs;
        state.clients = tData.clients;
        state.topDomains = tData.topDomains;

        // Update Header Meters
        document.getElementById('hdr-speed-rx').innerText = formatSpeed(statsRes.speedRx);
        document.getElementById('hdr-speed-tx').innerText = formatSpeed(statsRes.speedTx);
        if (document.getElementById('hdr-pkts')) {
          document.getElementById('hdr-pkts').innerText = statsRes.packetsPerSec || 0;
        }
        if (document.getElementById('hdr-ping')) {
          document.getElementById('hdr-ping').innerText = (statsRes.pingMs || 11) + ' ms';
        }
        document.getElementById('hdr-total-mb').innerText = formatBytes(statsRes.rxBytes + statsRes.txBytes);

        // Update Dashboard Tiles
        document.getElementById('dash-total').innerText = statsRes.total;
        document.getElementById('dash-blocked').innerText = statsRes.blocked;
        document.getElementById('dash-blockrate').innerText = statsRes.blockRate + '% sinkholed';
        document.getElementById('dash-cached').innerText = statsRes.cached;
        document.getElementById('dash-clients').innerText = statsRes.clientCount || clientsRes.length;

        // Dynamic Exact Blocklist Rules Counter
        const builtinRules = (statsRes.builtinCount !== undefined) ? statsRes.builtinCount : (typeof BUILTIN_RULES !== 'undefined' ? BUILTIN_RULES.length : 469);
        const customRules = (statsRes.blacklistCount !== undefined) ? statsRes.blacklistCount : (typeof customBlacklist !== 'undefined' ? customBlacklist.length : 0);
        const totalExactRules = builtinRules + customRules;
        const elDashRules = document.getElementById('dash-rules');
        const elDashRulesSub = document.getElementById('dash-rules-sub');
        if (elDashRules) elDashRules.innerText = totalExactRules;
        if (elDashRulesSub) elDashRulesSub.innerText = `${builtinRules} Built-in + ${customRules} Custom`;
        document.getElementById('dash-dns1').innerText = statsRes.upstreamDns;
        document.getElementById('dash-dns2').innerText = statsRes.upstreamDns2 || '--';
        document.getElementById('dash-uptime').innerText = statsRes.uptime + 's';
        document.getElementById('dash-heap').innerText = Math.round(statsRes.heap / 1024) + ' KB';

        // Update Upstream IPs
        document.getElementById('up-dns1').innerText = statsRes.upstreamDns;
        document.getElementById('up-dns2').innerText = statsRes.upstreamDns2 || '--';

        // Update Chart
        updateChart(statsRes);

        // Update ESP32 Hardware Health Telemetry
        if (statsRes.heap) {
          const freeKb = Math.round(statsRes.heap / 1024);
          const totalKb = Math.round((statsRes.totalHeap || 327680) / 1024);
          const minKb = Math.round((statsRes.minHeap || statsRes.heap) / 1024);
          const heapPct = Math.min(100, Math.round((freeKb / totalKb) * 100));

          const elHeapTxt = document.getElementById('esp-heap-txt');
          const elHeapBar = document.getElementById('esp-heap-bar');
          const elMinHeap = document.getElementById('esp-min-heap');
          if (elHeapTxt) elHeapTxt.innerText = freeKb + ' KB Free (' + heapPct + '%)';
          if (elHeapBar) elHeapBar.style.width = heapPct + '%';
          if (elMinHeap) elMinHeap.innerText = minKb + ' KB';
        }

        if (statsRes.tempC !== undefined) {
          const tc = statsRes.tempC;
          const tf = (tc * 1.8 + 32).toFixed(1);
          const elTemp = document.getElementById('esp-temp-txt');
          const elTempF = document.getElementById('esp-temp-f');
          const elTempBadge = document.getElementById('esp-temp-badge');
          if (elTemp) elTemp.innerText = tc.toFixed(1) + ' °C';
          if (elTempF) elTempF.innerText = '(' + tf + ' °F)';
          if (elTempBadge) {
            if (tc < 65) {
              elTempBadge.innerText = 'Optimal Thermal';
              elTempBadge.className = 'tag tag-allowed';
            } else if (tc < 80) {
              elTempBadge.innerText = 'Warm / Moderate';
              elTempBadge.className = 'tag tag-cached';
            } else {
              elTempBadge.innerText = 'High Heat';
              elTempBadge.className = 'tag tag-blocked';
            }
          }
        }

        if (statsRes.cpuFreq) {
          const elCpu = document.getElementById('esp-cpu-txt');
          if (elCpu) elCpu.innerText = statsRes.cpuFreq + ' MHz';
        }

        if (statsRes.sketchSize && statsRes.freeSketch) {
          const usedKb = Math.round(statsRes.sketchSize / 1024);
          const totalPartKb = Math.round((statsRes.sketchSize + statsRes.freeSketch) / 1024);
          const partPct = Math.min(100, Math.round((usedKb / totalPartKb) * 100));

          const elFlashTxt = document.getElementById('esp-flash-txt');
          const elFlashBar = document.getElementById('esp-flash-bar');
          if (elFlashTxt) elFlashTxt.innerText = (usedKb / 1024).toFixed(2) + ' MB / ' + (totalPartKb / 1024).toFixed(2) + ' MB (' + partPct + '%)';
          if (elFlashBar) elFlashBar.style.width = partPct + '%';
        }

        

        // Re-render components
        renderDevicesTable();
        renderTerminal();
        renderQueriesTable();
        renderTopDomains();

        if (state.filterIp) {
          renderInspectorQueries(state.filterIp);
        }
      } catch (e) {
        console.warn('Polling error:', e);
      }
    }

    // Upstream Benchmark
    async function scanLan() {
      try {
        await fetch(API_BASE + '/api/scan_lan', { method: 'POST' });
        alert('Active LAN ARP sweep initiated! Discovering connected network hosts...');
        setTimeout(fetchData, 1200);
      } catch (e) {
        alert('Scan request sent.');
      }
    }

    async function runBenchmark() {
      document.getElementById('lat-dns1').innerText = 'Testing...';
      document.getElementById('lat-dns2').innerText = 'Testing...';
      try {
        const res = await fetch(API_BASE + '/api/benchmark').then(r => r.json());
        document.getElementById('lat-dns1').innerText = res.lat1 + ' ms';
        document.getElementById('lat-dns2').innerText = res.lat2 + ' ms';
      } catch (e) {
        document.getElementById('lat-dns1').innerText = 'Error';
        document.getElementById('lat-dns2').innerText = 'Error';
      }
    }

    // Save DNS Config
    function setDnsPreset(dns1, dns2) {
      document.getElementById('cfg-dns1').value = dns1;
      document.getElementById('cfg-dns2').value = dns2;
      saveDnsConfig();
    }

    async function saveDnsConfig() {
      const d1 = document.getElementById('cfg-dns1').value.trim();
      const d2 = document.getElementById('cfg-dns2').value.trim();
      const body = new URLSearchParams();
      body.append('dns1', d1);
      body.append('dns2', d2);
      body.append('blocking', 'true');

      await fetch(API_BASE + '/api/save_settings', { method: 'POST', body });
      alert('DNS Upstream settings updated successfully!');
      fetchData();
    }

    
    // Built-in Blocklist Catalog (Embedded into Web UI PROGMEM)
    const BUILTIN_RULES = [
    {d:"1e100.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"2mdn.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"a-0001.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0002.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0003.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0004.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0005.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0006.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0007.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0008.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a-0009.a-msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"a.applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"a1.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"a2.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"a3.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"aax-us-east.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"aax.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"activity-stream-icons.services.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"activity.windows.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"ad-delivery.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ad.leadbolt.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"ad.toutiao.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"ad6media.fr",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adblade.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adbuffs.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adbutler.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adcolony.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"adform.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adhigh.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adition.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adjust.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"admanmedia.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"admin.appnext.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"admob.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"adnxs-simple.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adnxs.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adriver.ru",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adroll.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ads-partners.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ads-twitter.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.api.vungle.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"ads.facebook.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.google.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ads.linkedin.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"ads.pinterest.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.reddit.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.tiktok.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"ads.twitter.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"adsafeprotected.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adserver.yahoo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adservice.google.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adservices.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"adsmol.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adspecs.yahoo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adspirit.de",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adstargets.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adsterra.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adtechus.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adtrafficquality.google",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"advertising.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"advertising.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"advertising.yahoo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"adzerk.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"airtake.iot.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"alb.reddit.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"amplitude.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"an.facebook.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"analytics.google.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"analytics.tiktok.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"analytics.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"analytics.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"analytics.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"analytics.twitter.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"android.bugsnag.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"api-adservices.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"api.branch.io",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"api.ogury.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"api2.branch.io",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"app-analytics.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"app-measurement.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"app.adjust.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"app.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"appattest.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"appnext.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"appsflyer.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"arc.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"asimov-win.settings.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"assoc-amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"atdmt.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"auction.unityads.unity3d.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"bag.itunes.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"bdv.bidvertiser.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"betrad.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"bidswitch.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"bidvertiser.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"bingads.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"bluekai.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"branch.io",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"braze.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"browser.pipe.aria.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"business-api.tiktok.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"c.ad6media.fr",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"c.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"c.pollfish.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"casalemedia.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"cdn-lb.vungle.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"cdns.unityads.unity3d.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"chartboost.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"chitika.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"clarity.ms",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"clevertap.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"click.google-analytics.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"clickadu.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"clicksor.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"clicky.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"compatexchange.cloudapp.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"config.inmobi.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"config.unityads.unity3d.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"configuration.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"consent.ogury.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"contile.services.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"control.kochava.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"corpext.msitadfs.glbdns2.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"counter.yadro.ru",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"crash-reports.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"crash.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"crashlytics.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"crazyegg.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"criteo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"criteo.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"cs1.wpc.v0cdn.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ct.pinterest.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"d.applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"da.chartboost.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"daisy.ubuntu.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"data.flurry.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"data.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"data.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"data.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"data.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"datadoghq.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"delivery.trafficjunky.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"demdex.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"detectportal.firefox.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"device-metrics-us-2.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"device-metrics-us.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"df.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"diagnostics.support.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"directory.services.live.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"displaycatalog.mp.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"doubleclick.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"edge.activity.windows.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"engine.adzerk.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"engine.fyber.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"ero-advertising.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"events.api.vungle.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"events.appsflyer.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"events.redditmedia.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"everesttech.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"exdynsrv.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"exoclick.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"fe2.update.microsoft.com.akadns.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"fe3.delivery.mp.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"feedback.search.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"feedback.windows.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"firebaseinstallations.googleapis.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"firefox.settings.services.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"flashtalking.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"flighting.cp.wd.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"fls-eu.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"fls-na.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"flurry.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"fullstory.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"fundingchoicesmessages.google.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"fyber.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"g.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"gemini.yahoo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"global.appnext.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"google-analytics.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"googleadservices.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"googlesyndication.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"graph-video.facebook.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"gumgum.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"gw.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"gw.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"gw.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"h1.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"h2.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"h2.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"h2.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"heap.io",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"histats.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"hotjar.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"httpbin.org",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"i1.services.social.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"iad.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"iadsdk.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"incoming.telemetry.mozilla.org",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"indexexchange.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"info.startappservice.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"infolinks.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"init.itunes.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"init.supersonicads.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"inmobi.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"innovid.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"inspectlet.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"ironsource.mobi",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ironsrc.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"juicyads.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"kochava.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"kontera.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"krxd.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"leadbolt.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"leanplum.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"live.chartboost.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"liveintent.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"liveramp.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"localytics.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"location.services.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"log.pinterest.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"log.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"log.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"log.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"logrocket.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"luckyorange.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mads.amazon.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mathtag.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"matomo.org",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"mc.yandex.ru",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"media.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mediav.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"metrics.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"metrics.canonical.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"metrics.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"metrika.yandex.ru",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mgid.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mintegral.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"mixpanel.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"mmismm.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"moat.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"moatads.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mobvista.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"moengage.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"mookie1.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"mouseflow.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"ms.applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"msedge.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"msftconnecttest.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"nativo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"net.rayjump.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"newrelic.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"news-events.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"nexac.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"oca.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"oca.telemetry.microsoft.com.nsatc.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"ogury.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"omtrdc.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"onesignal.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"openx.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"optimizely.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"outbrain.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"outcome.ironsrc.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"pagead2.googlesyndication.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"pangle.io",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"pangolin-sdk-toutiao.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"partner.googleadservices.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"pdn.applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"pgl.rayjump.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"pipe.aria.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"piwik.pro",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"pixel.facebook.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"pixel.wp.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"pollfish.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"popads.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"popcash.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"popcon.debian.org",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"pre.footprintpredict.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"preview.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"propellerads.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"propellerclick.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"pubmatic.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"push.services.mozilla.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"px.ads.linkedin.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"quantcount.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"quantserve.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"qwapi.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"rad.live.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"rad.msn.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"rcm-eu.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"rcm-na.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"redir.metaservices.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"reports.crashlytics.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"reports.wes.df.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"resources.infolinks.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"revcontent.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"rlcdn.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"rpc.tapjoy.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"rt.applovin.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"rubiconproject.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"rubiconproject.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"s.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"sc-analytics.appspot.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"scorecardresearch.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"scorecardresearch.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"searchads.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"securemetrics.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"segment.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"segment.io",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"services.wes.df.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"serving-sys.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"settings-win.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"settings.crashlytics.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"settings.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"sharethrough.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"simpli.fi",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"singular.net",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"sls.update.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"smaato.net",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"smart-ad-server.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"smartadserver.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"smartlook.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"smoot.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"snapads.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"soma.smaato.net",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"sovrn.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"spotxchange.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"sqm.df.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"sqm.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"ssl.google-analytics.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"ssw.live.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"startappservice.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"statcounter.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"stats.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"stats.wp.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"statsfe1.ws.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"statsfe2.ws.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"stickyads.tv",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"stocks-sparkline.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"supersonicads.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"support-sp.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"syndication.exdynsrv.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"syndication.popcash.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"t.appsflyer.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"taboola.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"tapjoy.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"teads.tv",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"telecommand.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry-coverage.mozilla.org",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry.appex.bing.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry.inmobi.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry.mozilla.org",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry.sdk.snapcraft.io",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"telemetry.urs.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"tr.facebook.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"tr.snapchat.com",c:"social",s:"Social Media Tracker Filter"},
    {d:"track.ironsrc.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"track.supersonicads.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"tracking.tuya.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"tracking.tuyaeu.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"tracking.tuyaus.com",c:"tuya",s:"Tuya IoT Telemetry Blocklist"},
    {d:"trafficjunky.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"trafficjunky.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"tremorhub.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"trends.revcontent.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"tribalfusion.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"triplelift.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"turn.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"undertone.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"unityads.unity.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"unityads.unity3d.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"unrulymedia.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"v10.events.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"v10.vortex-win.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"v10c.events.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"v20.events.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"version.bing.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"vibrantmedia.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"view.adjust.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"view.atdmt.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"vortex-win.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"vortex.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"vscode-sync.trafficmanager.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"vscodeweb.azurewebsites.net",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"vungle.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"vwo.com",c:"track",s:"Web Analytics & Session Recorders"},
    {d:"watson.live.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"watson.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"watson.ppe.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"watson.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"wd.adcolony.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"web.vortex.data.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"webview.unityads.unity3d.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"wes.df.telemetry.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"win10.ipv6.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"win1710.ipv6.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"win8.ipv6.microsoft.com",c:"winlinux",s:"Windows & Linux Telemetry Feed"},
    {d:"ws-na.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"ws.tapjoyads.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"www.msftconnecttest.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"xp.apple.com",c:"mobile",s:"Android & iOS App Blocker"},
    {d:"yads.zedo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"yehiante.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"yieldlab.net",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"yieldmanager.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"yieldmo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"yieldoptimizer.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"z-eu.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"z-na.amazon-adsystem.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"zedo.com",c:"ads",s:"Steven Black / AdGuard DNS Base"},
    {d:"zemanta.com",c:"ads",s:"Steven Black / AdGuard DNS Base"}
  ];

    let selectedCategory = 'all';
    let customWhitelist = [];
    let customBlacklist = [];
    let isBlockingEnabled = true;

    function filterRuleCategory(cat) {
      selectedCategory = cat;
      document.querySelectorAll('#btn-cat-all, #btn-cat-mobile, #btn-cat-winlinux, #btn-cat-tuya, #btn-cat-ads, #btn-cat-track, #btn-cat-social')
        .forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btn-cat-' + cat);
      if (activeBtn) activeBtn.classList.add('active');
      renderRulesTable();
    }

    function renderRulesTable() {
      const tbody = document.getElementById('rules-tbody');
      if (!tbody) return;

      const searchInput = document.getElementById('rule-search');
      const term = searchInput ? searchInput.value.trim().toLowerCase() : '';

      // Filter catalog
      const filtered = BUILTIN_RULES.filter(item => {
        if (selectedCategory !== 'all' && item.c !== selectedCategory) return false;
        if (term && !item.d.includes(term)) return false;
        return true;
      });

      const counter = document.getElementById('rules-match-count');
      if (counter) {
        counter.innerText = `(Showing ${filtered.length} of ${BUILTIN_RULES.length} rules)`;
      }

      if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px; color:var(--text-muted);">No rules match your filter.</td></tr>';
        return;
      }

      // Display top 80 matches for fast scrolling
      const page = filtered.slice(0, 80);

      tbody.innerHTML = page.map(item => {
        const isWhitelisted = customWhitelist.includes(item.d);
        const isBlacklisted = customBlacklist.includes(item.d);

        let catLabel = 'Ad Network';
        let catColor = 'var(--accent-red)';
        if (item.c === 'mobile') { catLabel = '📱 Android & iPhone'; catColor = '#00e5ff'; }
        else if (item.c === 'winlinux') { catLabel = '🖥️ Windows & Linux'; catColor = '#00ff9d'; }
        else if (item.c === 'tuya') { catLabel = '🏠 Tuya Smart Home'; catColor = '#ff9100'; }
        else if (item.c === 'track') { catLabel = '👁️ Analytics & Tracker'; catColor = '#ffd600'; }
        else if (item.c === 'social') { catLabel = '💬 Social Tracker'; catColor = '#ff80ab'; }

        let statusBadge = '<span class="tag tag-blocked">Sinkhole Active</span>';
        let actionBtn = `<button class="cyber-btn" onclick="quickWhitelist('${item.d}')" style="font-size:0.72rem; padding:2px 8px;">✓ Whitelist</button>`;

        if (isWhitelisted) {
          statusBadge = '<span class="tag tag-allowed">Whitelisted (Bypassed)</span>';
          actionBtn = `<button class="cyber-btn" onclick="removeRule('white', '${item.d}')" style="font-size:0.72rem; padding:2px 8px; color:var(--accent-red);">&times; Un-whitelist</button>`;
        }

        return `
          <tr>
            <td><code style="color:${isWhitelisted ? 'var(--accent-green)' : '#fff'}; font-weight:700;">${item.d}</code></td>
            <td><span style="font-size:0.75rem; color:${catColor}; font-weight:600;">${catLabel}</span></td>
            <td><span style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">${item.s}</span></td>
            <td>${statusBadge}</td>
            <td>${actionBtn}</td>
          </tr>
        `;
      }).join('');
    }

    async function toggleEngine() {
      const newStatus = !isBlockingEnabled;
      const body = new URLSearchParams();
      body.append('enabled', newStatus ? '1' : '0');

      try {
        await fetch(API_BASE + '/api/toggle_blocking', { method: 'POST', body });
        isBlockingEnabled = newStatus;
        updateEngineUI();
      } catch (e) {
        alert('Toggle failed: ' + e);
      }
    }

    function updateEngineUI() {
      const badge = document.getElementById('master-status-badge');
      const btn = document.getElementById('btn-toggle-engine');
      if (badge && btn) {
        if (isBlockingEnabled) {
          badge.innerText = 'ENABLED (ACTIVE)';
          badge.className = 'tag tag-allowed';
          btn.innerText = '⏸️ Pause Ad Shield';
          btn.className = 'cyber-btn active';
        } else {
          badge.innerText = 'DISABLED (PAUSED)';
          badge.className = 'tag tag-blocked';
          btn.innerText = '▶️ Resume Ad Shield';
          btn.className = 'cyber-btn cyber-btn-red';
        }
      }
    }

    async function quickWhitelist(domain) {
      const body = new URLSearchParams();
      body.append('domain', domain);
      await fetch(API_BASE + '/api/add_white', { method: 'POST', body });
      await fetchRules();
    }

    // Rules management
    async function fetchRules() {
      try {
        const r = await fetch(API_BASE + '/api/lists').then(res => res.json());
        customWhitelist = r.whitelist || [];
        customBlacklist = r.blacklist || [];

        const wl = document.getElementById('wl-container');
        const bl = document.getElementById('bl-container');
        const elCustomCount = document.getElementById('rules-custom-count');
        const elWhiteCount = document.getElementById('rules-white-count');

        if (elCustomCount) elCustomCount.innerText = customBlacklist.length;
        if (elWhiteCount) elWhiteCount.innerText = customWhitelist.length;
        const elActiveCount = document.getElementById('rules-active-count');
        if (elActiveCount) elActiveCount.innerText = (typeof BUILTIN_RULES !== 'undefined' ? BUILTIN_RULES.length : 469) + ' Built-in Rules';

        if (wl) {
          wl.innerHTML = customWhitelist.map(d => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid #101624;">
              <code style="color:var(--accent-green); font-weight:700;">${d}</code>
              <button class="cyber-btn" onclick="removeRule('white', '${d}')" style="padding:2px 6px; font-size:0.7rem; color:var(--accent-red);">&times; Remove</button>
            </div>
          `).join('') || '<div style="color:var(--text-muted); font-size:0.8rem; padding:10px 0;">No whitelisted domains.</div>';
        }

        if (bl) {
          bl.innerHTML = customBlacklist.map(d => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid #101624;">
              <code style="color:var(--accent-red); font-weight:700;">${d}</code>
              <button class="cyber-btn" onclick="removeRule('block', '${d}')" style="padding:2px 6px; font-size:0.7rem; color:var(--accent-red);">&times; Remove</button>
            </div>
          `).join('') || '<div style="color:var(--text-muted); font-size:0.8rem; padding:10px 0;">No custom blacklisted domains.</div>';
        }

        renderRulesTable();
      } catch (e) {}
    }

    async function addRule(type) {
      const input = document.getElementById(type === 'white' ? 'add-wl-domain' : 'add-bl-domain');
      const domain = input.value.trim().toLowerCase();
      if (!domain) return;
      const endpoint = type === 'white' ? '/api/add_white' : '/api/add_block';
      const body = new URLSearchParams();
      body.append('domain', domain);
      await fetch(API_BASE + endpoint, { method: 'POST', body });
      input.value = '';
      await fetchRules();
    }

    async function removeRule(type, domain) {
      const endpoint = type === 'white' ? '/api/remove_white' : '/api/remove_block';
      const body = new URLSearchParams();
      body.append('domain', domain);
      await fetch(API_BASE + endpoint, { method: 'POST', body });
      await fetchRules();
    }

    function toggleBulkModal(type) {
      const box = document.getElementById('bulk-box-' + type);
      if (box) box.style.display = (box.style.display === 'none' || !box.style.display) ? 'block' : 'none';
    }

    function handleFileUpload(event, type) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        const text = e.target.result;
        const box = document.getElementById('bulk-box-' + type);
        const textarea = document.getElementById('bulk-input-' + type);
        const info = document.getElementById('file-info-' + type);
        
        if (box) box.style.display = 'block';
        if (textarea) textarea.value = text;
        
        const count = parseDomainText(text).length;
        if (info) {
          info.style.display = 'block';
          info.innerText = `📄 Loaded: ${file.name} (${(file.size / 1024).toFixed(1)} KB) - ${count} valid domains detected`;
        }
      };
      reader.readAsText(file);
    }

    function parseDomainText(rawText) {
      const rawLines = rawText.split('\n');
      const domains = [];
      const domainRegex = /^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$/i;

      for (let line of rawLines) {
        line = line.trim();
        if (!line || line.startsWith('#') || line.startsWith('!') || line.startsWith(';')) continue;
        if (line.includes('#')) line = line.split('#')[0].trim();
        if (line.startsWith('||')) {
          line = line.substring(2);
          if (line.includes('^')) line = line.split('^')[0];
        }
        const parts = line.split(/\s+/);
        let d = (parts.length >= 2 && ['0.0.0.0', '127.0.0.1'].includes(parts[0])) ? parts[1] : parts[0];
        d = d.trim().toLowerCase().replace(/\.$/, '');
        if (domainRegex.test(d) && !domains.includes(d)) {
          domains.push(d);
        }
      }
      return domains;
    }

    async function importBulkRules(type) {
      const textarea = document.getElementById('bulk-input-' + type);
      const status = document.getElementById('bulk-status-' + type);
      const btn = document.getElementById('btn-import-' + type);
      if (!textarea || !textarea.value.trim()) return;

      const domains = parseDomainText(textarea.value);
      if (domains.length === 0) {
        if (status) status.innerText = 'No valid domains found.';
        return;
      }

      if (btn) btn.disabled = true;
      if (status) status.innerText = `Importing ${domains.length} domains...`;

      try {
        const body = new URLSearchParams();
        body.append('type', type);
        body.append('domains', domains.join('\n'));
        const resp = await fetch(API_BASE + '/api/add_bulk', { method: 'POST', body });
        if (resp.ok) {
          const res = await resp.json();
          if (status) status.innerText = `Done! Imported ${res.added || domains.length} rules.`;
        } else {
          throw new Error('Batch API fallback');
        }
      } catch (e) {
        const endpoint = type === 'white' ? '/api/add_white' : '/api/add_block';
        for (let i = 0; i < domains.length; i++) {
          const body = new URLSearchParams();
          body.append('domain', domains[i]);
          await fetch(API_BASE + endpoint, { method: 'POST', body });
          if (status) status.innerText = `Importing ${i + 1}/${domains.length}...`;
        }
        if (status) status.innerText = `Done! Imported ${domains.length} rules.`;
      }

      textarea.value = '';
      if (btn) btn.disabled = false;
      await fetchRules();
    }

    async function clearList(type) {
      const name = type === 'white' ? 'Whitelist' : 'Blacklist';
      if (!confirm(`Are you sure you want to clear all custom ${name} rules?`)) return;
      try {
        const body = new URLSearchParams();
        body.append('type', type);
        await fetch(API_BASE + '/api/clear_list', { method: 'POST', body });
        await fetchRules();
      } catch (e) {
        alert('Clear failed: ' + e);
      }
    }

    // Auto Refresh Interval
    fetchData();
    fetchRules();
    renderRulesTable();
    setInterval(fetchData, 1500);
  </script>
</body>
</html>
"""

# Write src/web_ui.h
with open(r'c:\Users\MSI Laptop\Desktop\esp21-eth01-ad-blocker\src\web_ui.h', 'w', encoding='utf-8') as f:
    f.write('#ifndef WEB_UI_H\n#define WEB_UI_H\n\n#include <Arduino.h>\n#include <pgmspace.h>\n\nstatic const char INDEX_HTML[] PROGMEM = R"rawliteral(\n')
    f.write(html_content)
    f.write('\n)rawliteral";\n\n#endif // WEB_UI_H\n')

# Also write dashboard.html
with open(r'c:\Users\MSI Laptop\Desktop\esp21-eth01-ad-blocker\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS: Generated src/web_ui.h and dashboard.html!")

