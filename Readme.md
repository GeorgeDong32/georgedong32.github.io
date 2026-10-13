# George Dong — personal website

A dependency-free, English-language portfolio for AI coding agents, open-source contributions and integrated-circuit research interests. The site is plain HTML and CSS; it needs no Node packages, build process, JavaScript, database, analytics or third-party fonts.

## Preview

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. You can also open `index.html` directly. The Python server is only a local preview tool, not a deployment dependency.

## Structure

- `index.html`: the complete portfolio, including Work, About, Earlier Projects and Contact.
- `css/site.css`: all active styles, layout breakpoints, focus treatment and reduced-motion handling.
- `about.html`, `project.html`: legacy URLs, redirected to the corresponding homepage section with a meaningful no-script fallback.
- `img/avatar.webp`: the original illustrated avatar, used without modification.
- `img/projects/*.webp`: original project previews/artwork reused in Earlier Projects. These are historical materials, not newly generated screenshots.
- `tests/check_site.py`: standard-library structural, metadata, local-link, image-alt and compatibility checks.

The previous template's CSS, scripts and alternate-color assets are retained for history/compatibility, but none are loaded by the new pages. The unused FontAwesome webfonts and the unused Inter `font-family` entry were removed; text now uses the system font stack. They can be removed separately after checking for external deep links. GitHub Pages can serve the repository directly as before; this change does not modify deployment settings.

## Content maintenance

Edit the semantic sections in `index.html`. There is deliberately no second content store or generated copy to synchronize. Update the short fallback summaries in `about.html` and `project.html` when the corresponding sections change substantially.

Keep these distinctions clear:

- Cherry Studio is a community project. This portfolio describes George Dong's contributions, not ownership of the product.
- The Cherry Studio security example links to the specific merged PR. Don't broaden its claims to imply a complete security audit or elimination of every related attack surface.
- Pi-Extensions is a suite with four linked components. Describe each component's job rather than publishing arbitrary skill ratings.
- EDA / chip design is a research interest here. Add outcomes or papers only when there is a public, verified source.
- Earlier Projects intentionally preserves legacy work without claiming current support, availability or a working public demo where none is linked.
- Education wording deliberately omits the university and other location details; keep it that way. Education dates and volatile statistics are omitted. Recheck the public profile when updating education or roles.
- Contact lists both public email addresses (Outlook and Foxmail). No phone number or contact form is included.

### Sources checked for this refresh (2026-10-12)

- Profile: https://github.com/GeorgeDong32
- Profile source: https://github.com/GeorgeDong32/GeorgeDong32/blob/main/README.md
- Contribution: https://github.com/CherryHQ/cherry-studio/pull/18751 (author `GeorgeDong32`; GitHub API returned `merged: true`)
- Permission kernel: https://github.com/GeorgeDong32/pi-permission-modes
- Agent supervision: https://github.com/GeorgeDong32/pi-agent-panel
- Review: https://github.com/GeorgeDong32/pi-review
- Terminal interface: https://github.com/GeorgeDong32/pi-claude-code-tui
- Earlier project descriptions, URLs and artwork: the previous portfolio at commit `b73bb15692492e8e53414643befe6251ff61cbcd`.

The existing blog link is preserved: https://blog.georgedong.tech/. External links can change independently of this repository.

### Domain and indexing

The site is served from the same repository through both GitHub Pages and Cloudflare Pages, and the primary domain may change over time. Canonical URLs are therefore relative (`/`) instead of pinned to a hostname: each serving host resolves its own canonical URL, and no domain is hard-coded in routing. `og:url` is omitted for the same reason (relative Open Graph URLs are unreliable across consumers). `og:image` keeps one absolute URL on `github.io` because the Open Graph spec expects absolute image addresses; it is a resource link, not routing, and stays valid regardless of the serving domain. No DNS, hosting, redirect or deployment configuration is changed here.

The existing `robots.txt` is preserved. It broadly disallows crawling; review that policy deliberately if the site should become search-indexable. Metadata alone does not override it.

## Checks

```sh
python3 tests/check_site.py
git diff --check
```

The checks cover HTML nesting, unique IDs, one main heading per page, language and metadata, local resources, fragment targets, alt text and image dimensions, no runtime dependencies, and old-URL redirects/fallback links. They do not check the availability or content of external sites, nor replace browser/accessibility testing.

Browser review checklist:

1. Check widths 390, 768, 1180 and 1440 px. The hero text and avatar must stay separate, and the document must have no horizontal overflow.
2. Use keyboard-only navigation: the first Tab should reveal Skip to content, all links should have visible focus, and every section navigation target should remain below the header.
3. Open both legacy URLs and verify their destination sections; browser Back/Forward should work normally.
4. Test with JavaScript disabled (the full site still works), with reduced motion, and with text zoomed to 200%.
5. Confirm image loading, external project destinations, email links and the blog link.

There is no build command: HTML/CSS and local assets are the deployable output. No deployment or push is performed by the refresh itself.
