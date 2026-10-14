# Jasmine Wang — portfolio site

A Jekyll site hosted free on GitHub Pages, edited through Pages CMS (a form-based editor), served on your own domain.

## Where the content lives

| What | File | Edit in Pages CMS under |
|---|---|---|
| Name, headline, self-introduction, links, résumé PDF, photo | `_data/profile.yml` | About me |
| Projects | `_data/projects.yml` | Projects |
| Education | `_data/education.yml` | Education |
| Blog posts | `_posts/YYYY-MM-DD-title.md` | Blog posts |
| Uploaded PDFs and images | `assets/uploads/` | Media |

Every save in Pages CMS is a commit to GitHub, and GitHub Pages republishes the site automatically in about a minute.

## One-time setup (about 30 minutes)

### 1. Put the site on GitHub
1. Create a free account at github.com if you don't have one.
2. Create a new **public** repository, e.g. `portfolio`.
3. On the repository page choose **Add file → Upload files**, drag in everything from this folder (including the hidden `.pages.yml` — on a Mac press Cmd+Shift+. in Finder to see it), and commit.

### 2. Turn on GitHub Pages
1. Repository → **Settings → Pages**.
2. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
3. After a minute the site is live at `https://<your-username>.github.io/portfolio/`.
   (It will look right once the custom domain is connected in step 4. To use the github.io address on its own, set `baseurl: "/portfolio"` in `_config.yml`.)

### 3. Connect the editor
1. Go to https://app.pagescms.org and sign in with GitHub.
2. Pick the `portfolio` repository. You'll see About me, Projects, Education and Blog posts as forms.

### 4. Buy and connect your domain
1. Buy a domain at a registrar such as Cloudflare Registrar, Porkbun or Namecheap (a `.com` is typically about $10–15 a year). Ideas: `jasminewang.com`, `jasminewang.io`, `jasminewangpm.com`.
2. In the registrar's DNS settings add:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | `<your-username>.github.io` |

3. GitHub → repository **Settings → Pages → Custom domain**: enter `yourdomain.com` and save (this creates a `CNAME` file in the repo).
4. Once the DNS check passes (minutes to a few hours), tick **Enforce HTTPS**.
5. Set `url: "https://yourdomain.com"` in `_config.yml`.

## Publishing a blog post
1. Pages CMS → **Blog posts → Add an entry**.
2. Fill in title, date and a short summary, paste the article, and optionally add the Medium link and a PDF.
3. Save. It appears on the home page and at `/blog/` within a minute.

Readers get a **Download PDF** button on every post: it downloads your uploaded PDF if you added one, otherwise it opens the browser's save-as-PDF with a clean print layout.

## Importing your Medium article
Medium's settings include a **Download your information** option that emails you a zip with each story as HTML. Or just copy the text from the article page. Paste the story text into a new post (or the placeholder post in `_posts/`), and delete the placeholder when done.
