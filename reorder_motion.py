import re

with open('/Users/harry.simpson/RR WD2/motion.html', 'r') as f:
    html = f.read()

# Replace Nav Bar
nav_replacement = """<!-- BRANDBAR -->
    <nav class="site-nav" style="padding: 24px 0; border-bottom: 1px solid var(--border);">
        <div class="container nav-inner" style="display: flex; justify-content: space-between; align-items: center;">
            <a href="index.html" class="nav-brand"
                style="font-weight: 950; font-size: 20px; letter-spacing: -0.05em; text-transform: uppercase; text-decoration: none; color: #000;">RARE
                RENDER</a>
            <a href="#trial" style="background: #000; color: #fff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.2s;">Start $79 Trial</a>
        </div>
    </nav>"""
html = re.sub(r'<!-- BRANDBAR -->.*?</nav>', nav_replacement, html, flags=re.DOTALL)

# Replace Hero CTA
hero_cta_replacement = """<div class="hero-cta-wrap">
                        <a href="#trial" class="btn-trial">Start $79 Trial</a>
                        <p class="note-sub" style="margin-top: 16px; font-weight: 600; color: #555;">* Priority 48-hour delivery included</p>
                    </div>"""
html = re.sub(r'<div class="hero-cta-wrap">.*?</div>', hero_cta_replacement, html, count=1, flags=re.DOTALL)

# Extract blocks
def extract_block(marker, html_text):
    pattern = r'(\s*<!-- ' + marker + r' -->.*?</section>)'
    match = re.search(pattern, html_text, flags=re.DOTALL)
    return match.group(1) if match else ""

blocks = {
    'HERO': extract_block('HERO', html),
    'AUTHENTICITY': extract_block('AUTHENTICITY SECTION', html),
    'VISUALS': extract_block('VISUALS / PORTFOLIO', html),
    'COMPARISON': extract_block('COMPARISON / FRAMING', html),
    'VERSATILITY': extract_block('PROPERTY TYPES', html),
    'PRICING': extract_block('PRICING', html),
    'PREP': extract_block('PREPARATION & SUBMISSION', html),
    'PATHWAY': extract_block('ORDER PATHWAY', html),
    'WHY': extract_block('WHY AGENTS USE IT', html),
    'FAQ': extract_block('FAQ', html),
}

# Construct main content in the new funnel order
main_content = "".join([
    blocks['HERO'],
    blocks['VISUALS'],
    blocks['AUTHENTICITY'],
    blocks['COMPARISON'],
    blocks['WHY'],
    blocks['PATHWAY'],
    blocks['PRICING'],
    blocks['PREP'],
    blocks['VERSATILITY'],
    blocks['FAQ']
])

# Ensure pricing has id="trial"
main_content = main_content.replace('id="pricing"', 'id="trial"')

# Replace everything inside <main>
html = re.sub(r'<main>.*?</main>', f'<main>\n{main_content}\n    </main>', html, flags=re.DOTALL)

with open('/Users/harry.simpson/RR WD2/motion.html', 'w') as f:
    f.write(html)

print("Funnel Reordering Complete!")
