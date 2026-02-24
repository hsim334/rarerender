import re

with open('/Users/harry.simpson/RR WD2/motion.html', 'r') as f:
    html = f.read()

# 1. Update Navigation
nav_regex = re.compile(r'<!-- BRANDBAR -->.*?</nav>', re.DOTALL)
new_nav = """<!-- BRANDBAR -->
    <nav class="site-nav" style="padding: 24px 0; border-bottom: 1px solid var(--border);">
        <div class="container nav-inner" style="display: flex; justify-content: space-between; align-items: center;">
            <a href="index.html" class="nav-brand"
                style="font-weight: 950; font-size: 20px; letter-spacing: -0.05em; text-transform: uppercase; text-decoration: none; color: #000;">RARE
                RENDER</a>
            <a href="#trial" style="font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #fff; background: #000; padding: 12px 24px; border-radius: 6px; text-decoration: none; transition: opacity 0.2s;">START $79 TRIAL</a>
        </div>
    </nav>"""
html = nav_regex.sub(new_nav, html)

# 2. Update Hero CTA
hero_cta_regex = re.compile(r'<div class="hero-cta-wrap">.*?</div>', re.DOTALL)
new_hero_cta = """<div class="hero-cta-wrap">
                        <a href="#trial" class="btn-trial">Claim Trial Listing — $79</a>
                        <p class="note-sub" style="margin-top: 16px; font-weight: 600; color: #ff3333;">* Includes priority 48-hour delivery</p>
                    </div>"""
html = hero_cta_regex.sub(new_hero_cta, html, count=1)

# 3. Swap Authenticity and Visuals
auth_regex = re.compile(r'(<!-- AUTHENTICITY SECTION -->.*?</section>)\s*(<!-- VISUALS / PORTFOLIO -->.*?</section>)', re.DOTALL)
html = auth_regex.sub(r'\2\n\n        \1', html)

# 4. Reorder bottom funnel: Before -> Pricing, Prep, Pathway, Why, FAQ. After -> Why, Pathway, Prep, Pricing, FAQ
why_regex = re.compile(r'(<!-- WHY AGENTS USE IT -->.*?</section>)', re.DOTALL)
why_block = why_regex.search(html).group(1)
html = html.replace(why_block, '')

pathway_regex = re.compile(r'(<!-- ORDER PATHWAY -->.*?</section>)', re.DOTALL)
pathway_block = pathway_regex.search(html).group(1)
html = html.replace(pathway_block, '')

prep_regex = re.compile(r'(<!-- PREPARATION & SUBMISSION -->.*?</section>)', re.DOTALL)
prep_block = prep_regex.search(html).group(1)
html = html.replace(prep_block, '')

# Insert Why, Pathway, Prep before Pricing
pricing_regex = re.compile(r'(<!-- PRICING -->)', re.DOTALL)
html = html.replace('<!-- PRICING -->', f"{why_block}\n\n        {pathway_block}\n\n        {prep_block}\n\n        <!-- PRICING -->")

# Update Pricing id to "trial"
html = html.replace('<section class="container reveal" id="pricing">', '<section class="container reveal" id="trial">')


with open('/Users/harry.simpson/RR WD2/motion.html', 'w') as f:
    f.write(html)
