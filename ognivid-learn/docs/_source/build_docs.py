"""Build the OGNIVID LEARN documentation (English + Bahasa Indonesia).

Usage:  python3 -I ognivid-learn/docs/_source/build_docs.py
Writes: ognivid-learn/docs/OGNIVID-LEARN-Documentation.html,
        ognivid-learn/docs/id/OGNIVID-LEARN-Dokumentasi.html and ognivid-learn/docs/index.html

Every text is a pair T(en, id) so both languages always have the same structure.
Public portfolio version: no credentials, bank details, coupon codes, phone numbers or internal IDs.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = {"en": ROOT / "docs" / "OGNIVID-LEARN-Documentation.html",
       "id": ROOT / "docs" / "id" / "OGNIVID-LEARN-Dokumentasi.html"}
LINK = {"en": "OGNIVID-LEARN-Documentation.html", "id": "id/OGNIVID-LEARN-Dokumentasi.html"}
SITE = "https://learn.ognivid.com/"
PORTFOLIO = "https://diimasogan.github.io/#projects"
LANG = "en"


class T(tuple):
    def __new__(cls, en, id_=None):
        return super().__new__(cls, (en, en if id_ is None else id_))

    def __str__(self):
        return self[0] if LANG == "en" else self[1]


def s(x):
    return str(x) if isinstance(x, T) else x


# ---------------------------------------------------------------- building blocks
def icon(path):
    return f'<svg class="ico" viewBox="0 0 24 24">{path}</svg>'


ICONS = {
    "server": '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11L21 7H6.2"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="m9.5 9 1.8 1.8L15 7.2"/><path d="M8.5 14.2 7 22l5-3 5 3-1.5-7.8"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c.8-3.5 3.6-5.5 7-5.5s6.2 2 7 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "code": '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 4l-4 16"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.2 0 1.8-.9 1.4-2-.5-1.3.4-2.5 1.8-2.5H18a3 3 0 0 0 3-3A8.6 8.6 0 0 0 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10.5" cy="7.5" r="1"/><circle cx="15" cy="8" r="1"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}


def card(ic, title, text, amber=False):
    return (f'<div class="card{" amber" if amber else ""}"><div class="ihead">{icon(ICONS[ic])}<h3>{s(title)}</h3></div>'
            f'<p>{s(text)}</p></div>')


def grid(cards, cols=3):
    return f'<div class="grid g{cols}">{"".join(cards)}</div>'


def table(head, rows):
    h = "".join(f"<th>{s(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{s(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section(sid, title, body):
    return f'<section id="{sid}"><h2>{s(title)}</h2>{body}</section>'


def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{n}</b><span>{s(t)}</span></div>' for n, t in items) + "</div>"


def ul(items):
    return '<ul class="clean">' + "".join(f"<li>{s(i)}</li>" for i in items) + "</ul>"


def steps(items):
    return "".join(f'<div class="starter"><div class="snum">{i}</div><div><p class="q">{s(t)}</p><p>{s(d)}</p></div></div>'
                   for i, (t, d) in enumerate(items, 1))


# ---------------------------------------------------------------- diagram
def architecture_svg():
    L = lambda en, id_: s(T(en, id_))
    return f"""<figure><svg viewBox="0 0 980 430" role="img" aria-label="{L('Platform architecture','Arsitektur platform')}">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" class="mk"/></marker></defs>
<g class="lane"><rect x="10" y="20" width="220" height="390" rx="14"/><text x="120" y="46" class="lt">{L('Users','Pengguna')}</text></g>
<g class="lane"><rect x="250" y="20" width="490" height="390" rx="14"/><text x="495" y="46" class="lt">{L('Web hosting · Apache + PHP 8.4','Web hosting · Apache + PHP 8.4')}</text></g>
<g class="lane"><rect x="760" y="20" width="210" height="390" rx="14"/><text x="865" y="46" class="lt">{L('Connected services','Layanan terhubung')}</text></g>
<g class="bx"><rect x="28" y="70" width="184" height="56" rx="10"/><text x="120" y="94">{L('Students','Siswa')}</text><text x="120" y="113" class="sm">{L('browse, buy, learn','lihat, beli, belajar')}</text></g>
<g class="bx"><rect x="28" y="146" width="184" height="56" rx="10"/><text x="120" y="170">{L('Instructors','Instruktur')}</text><text x="120" y="189" class="sm">{L('create courses, withdraw','buat kursus, tarik dana')}</text></g>
<g class="bx"><rect x="28" y="222" width="184" height="56" rx="10"/><text x="120" y="246">Admin</text><text x="120" y="265" class="sm">{L('orders, grading, setup','pesanan, penilaian, setup')}</text></g>
<g class="bx amb"><rect x="28" y="330" width="184" height="56" rx="10"/><text x="120" y="354">{L('Python scripts','Script Python')}</text><text x="120" y="373" class="sm">{L('pages &amp; content as code','halaman &amp; konten sebagai kode')}</text></g>
<g class="bx"><rect x="270" y="70" width="450" height="44" rx="10"/><text x="495" y="97">{L('Server-side page cache + CDN · HTTPS','Cache halaman di server + CDN · HTTPS')}</text></g>
<g class="bx hl"><rect x="270" y="132" width="450" height="56" rx="10"/><text x="495" y="156">WordPress 7.1 (self-hosted, WordPress.org)</text><text x="495" y="175" class="sm">{L('Indonesian locale · UTC+7 · Hello Elementor theme','Bahasa Indonesia · UTC+7 · tema Hello Elementor')}</text></g>
<g class="bx"><rect x="270" y="206" width="140" height="62" rx="10"/><text x="340" y="231">Elementor Pro</text><text x="340" y="250" class="sm">{L('pages · theme builder','halaman · theme builder')}</text></g>
<g class="bx"><rect x="425" y="206" width="140" height="62" rx="10"/><text x="495" y="231">Tutor LMS Pro</text><text x="495" y="250" class="sm">{L('courses · quizzes · certs','kursus · kuis · sertifikat')}</text></g>
<g class="bx"><rect x="580" y="206" width="140" height="62" rx="10"/><text x="650" y="231">WooCommerce</text><text x="650" y="250" class="sm">{L('cart · checkout · orders','keranjang · checkout · pesanan')}</text></g>
<g class="bx amb"><rect x="270" y="286" width="450" height="50" rx="10"/><text x="495" y="308">{L('2 custom plugins (PHP)','2 plugin custom (PHP)')}</text><text x="495" y="325" class="sm">{L('Tutor fixes &amp; business rules · Indonesian translation (~1,440 strings)','Perbaikan Tutor &amp; aturan bisnis · terjemahan Indonesia (~1.440 teks)')}</text></g>
<g class="bx"><rect x="270" y="352" width="450" height="44" rx="10"/><text x="495" y="379">{L('MySQL / MariaDB database · REST API','Database MySQL / MariaDB · REST API')}</text></g>
<g class="bx hl"><rect x="778" y="70" width="174" height="56" rx="10"/><text x="865" y="94">SMTP · SSL 465</text><text x="865" y="113" class="sm">{L('own-domain mailbox','mailbox domain sendiri')}</text></g>
<g class="bx"><rect x="778" y="146" width="174" height="56" rx="10"/><text x="865" y="170">WhatsApp</text><text x="865" y="189" class="sm">{L('payment confirmation','konfirmasi pembayaran')}</text></g>
<g class="bx"><rect x="778" y="222" width="174" height="56" rx="10"/><text x="865" y="246">Telegram</text><text x="865" y="265" class="sm">{L('student community','komunitas siswa')}</text></g>
<g class="bx"><rect x="778" y="298" width="174" height="56" rx="10"/><text x="865" y="322">Google Meet</text><text x="865" y="341" class="sm">{L('live bootcamps','bootcamp live')}</text></g>
<g class="ln"><path d="M212 98h58" marker-end="url(#ar)"/><path d="M212 174h30v-78h28" marker-end="url(#ar)"/><path d="M212 250h30v-150h28" marker-end="url(#ar)"/>
<path d="M495 114v18M495 188v18M495 268v18M495 336v16" marker-end="url(#ar)"/><path d="M212 358h40v16h18" marker-end="url(#ar)"/>
<path d="M720 160h20v-62h38" marker-end="url(#ar)"/><path d="M720 237h20v-63h38" marker-end="url(#ar)"/><path d="M720 237h20v13h38" marker-end="url(#ar)"/><path d="M720 237h20v89h38" marker-end="url(#ar)"/></g>
</svg><figcaption>{L('One self-hosted WordPress install, separate from ognivid.com, runs the LMS, the store and the custom plugins. Pages and content are maintained from Python scripts through the WordPress REST API.','Satu instalasi WordPress self-hosted, terpisah dari ognivid.com, menjalankan LMS, toko, dan plugin custom. Halaman dan konten dikelola dari script Python lewat WordPress REST API.')}</figcaption></figure>"""


# ---------------------------------------------------------------- content
def content():
    return [
        section("summary", T("Executive summary", "Ringkasan eksekutif"),
            f'<p class="lead">{s(T("OGNIVID LEARN is an online learning platform I installed, configured and run on self-hosted WordPress: courses with quizzes and assignments, a Rupiah store with checkout, verifiable certificates, live bootcamps and an instructor programme, all in Indonesian.", "OGNIVID LEARN adalah platform belajar online yang saya pasang, konfigurasi, dan jalankan di WordPress self-hosted: kursus dengan kuis dan tugas, toko dalam Rupiah dengan checkout, sertifikat yang bisa diverifikasi, bootcamp live, dan program instruktur, semuanya dalam Bahasa Indonesia."))}</p>'
            f'<p>{s(T("It is a working, public site, not a demo, and it shows the full self-hosted WordPress job: installation and configuration, LMS and e-commerce setup, custom plugins, transactional e-mail, design, and day-to-day operation.", "Ini situs publik yang benar-benar berjalan, bukan demo, dan menunjukkan pekerjaan WordPress self-hosted secara utuh: instalasi dan konfigurasi, setup LMS dan e-commerce, plugin custom, e-mail transaksional, desain, serta operasional harian."))}</p>'
            + stats([("2", T("courses live", "kursus aktif")), ("58", T("lessons written", "pelajaran berisi materi")),
                     ("3", T("certificate templates", "template sertifikat")), ("~1,440", T("strings translated to Indonesian", "teks diterjemahkan ke Indonesia")) if LANG == "en" else ("~1.440", T("strings translated to Indonesian", "teks diterjemahkan ke Indonesia"))])
            + f'<p style="margin-top:18px"><a class="btn" href="{SITE}">{s(T("Visit learn.ognivid.com →", "Kunjungi learn.ognivid.com →"))}</a></p>'),

        section("features", T("What I set up", "Yang saya bangun"),
            grid([card("server", T("Self-hosted WordPress", "WordPress self-hosted"), T("A separate WordPress install from ognivid.com, set to Indonesian and UTC+7, with HTTPS, server-side page cache and CDN.", "Instalasi WordPress terpisah dari ognivid.com, berbahasa Indonesia dan zona waktu UTC+7, dengan HTTPS, cache halaman di server, dan CDN.")),
                  card("book", T("Learning management", "Learning management"), T("Tutor LMS Pro with courses, chapters, quizzes, project assignments and strict completion rules.", "Tutor LMS Pro dengan kursus, bab, kuis, tugas proyek, dan aturan penyelesaian yang ketat.")),
                  card("cart", T("Store & checkout", "Toko & checkout"), T("WooCommerce in Rupiah: cart, short checkout that creates the account automatically, bank transfer with WhatsApp confirmation, and automatic enrolment when an order is completed.", "WooCommerce dalam Rupiah: keranjang, checkout ringkas yang otomatis membuat akun, transfer bank dengan konfirmasi WhatsApp, dan pendaftaran kursus otomatis saat pesanan selesai.")),
                  card("award", T("Verifiable certificates", "Sertifikat terverifikasi"), T("Three branded templates (Completion, Participation, Appreciation). Each certificate has a unique number that anyone can verify on the site.", "Tiga template bermerek (Completion, Participation, Appreciation). Setiap sertifikat punya nomor unik yang bisa diverifikasi siapa pun di situs.")),
                  card("calendar", T("Events & bootcamps", "Event & bootcamp"), T("Live online bootcamps with their own landing page, time-based Early Bird pricing, add-on products, project submission and manual grading.", "Bootcamp online live dengan landing page sendiri, harga Early Bird berbasis waktu, produk add-on, pengumpulan proyek, dan penilaian manual.")),
                  card("users", T("Instructor programme", "Program instruktur"), T("Invite-only instructor registration, admin approval, course review before publishing, and withdrawals by bank transfer.", "Pendaftaran instruktur lewat undangan, persetujuan admin, review kursus sebelum terbit, dan penarikan dana via transfer bank."))])),

        section("architecture", T("Architecture & stack", "Arsitektur & stack"), architecture_svg()
            + table([T("Layer", "Lapisan"), T("What runs there", "Yang berjalan"), T("Notes", "Catatan")], [
                [T("Hosting", "Hosting"), "Apache, PHP 8.4", T("Web hosting with server-side page cache and CDN; cache purged after every update", "Web hosting dengan cache halaman di server dan CDN; cache dibersihkan setiap kali ada update")],
                ["CMS", "WordPress 7.1 (WordPress.org)", T("Self-hosted install, Indonesian locale, UTC+7", "Instalasi self-hosted, Bahasa Indonesia, UTC+7")],
                [T("Design", "Desain"), "Hello Elementor · Elementor + Elementor Pro 4.4", T("Global header and footer from Theme Builder; dark theme with one global stylesheet", "Header dan footer global dari Theme Builder; tema gelap dengan satu stylesheet global")],
                ["LMS", "Tutor LMS + Tutor Pro 4.2", T("Certificate, Assignments and Enrollment add-ons", "Add-on Certificate, Assignments, dan Enrollment")],
                ["E-commerce", "WooCommerce 11.3", T("Rupiah, bank transfer, coupons, add-on products", "Rupiah, transfer bank, kupon, produk add-on")],
                ["E-mail", "WP Mail SMTP", T("Own-domain mailbox over SSL (port 465); separate sender, admin and student addresses", "Mailbox domain sendiri lewat SSL (port 465); alamat pengirim, admin, dan siswa dipisah")],
                [T("Custom code", "Kode custom"), T("2 PHP plugins · Python tooling", "2 plugin PHP · tooling Python"), T("See the next sections", "Lihat bagian berikutnya")]])),

        section("plugins", T("Custom plugins", "Plugin custom"),
            f'<p>{s(T("Where a plugin setting was not enough, I wrote the behaviour as code instead of editing plugin files, so updates stay safe.", "Jika pengaturan plugin tidak cukup, saya menulis perilakunya sebagai kode, bukan mengubah file plugin, sehingga update tetap aman."))}</p>'
            + f'<h3 style="margin-top:18px">{s(T("1 · Tutor fixes & business rules (v1.10)", "1 · Perbaikan Tutor & aturan bisnis (v1.10)"))}</h3>'
            + table([T("Area", "Area"), T("What it does", "Fungsinya")], [
                [T("Bug fix", "Perbaikan bug"), T("Fixes an HTTP 500 error on the Forgot Password page in Tutor 4.2.1", "Memperbaiki error HTTP 500 di halaman Lupa Password pada Tutor 4.2.1")],
                [T("Certificates", "Sertifikat"), T("Applies the OGNIVID certificate template to every new course automatically", "Otomatis memasang template sertifikat OGNIVID ke setiap kursus baru")],
                [T("Checkout", "Checkout"), T("Short checkout plus a payment confirmation button that opens WhatsApp with the order details filled in", "Checkout ringkas plus tombol konfirmasi pembayaran yang membuka WhatsApp dengan detail pesanan terisi otomatis")],
                [T("Pricing", "Harga"), T("Early Bird price that switches automatically on a date, add-on rules, and one-click bundle links to the cart", "Harga Early Bird yang otomatis berganti pada tanggal tertentu, aturan add-on, dan link paket satu klik ke keranjang")],
                [T("After purchase", "Setelah pembelian"), T("Join-Telegram and contact-admin buttons on the thank-you page, order page and order e-mails", "Tombol gabung Telegram dan hubungi admin di halaman terima kasih, halaman pesanan, dan e-mail pesanan")],
                [T("Instructors", "Instruktur"), T("Invite-link registration that also works for logged-in students; Indonesian payout form with a fix for empty IBAN/SWIFT fields", "Pendaftaran lewat link undangan yang juga berfungsi untuk siswa yang sudah login; form penarikan dana berbahasa Indonesia dengan perbaikan kolom IBAN/SWIFT kosong")],
                [T("Catalogue", "Katalog"), T("Hides internal courses (speaker appreciation) from the public catalogue", "Menyembunyikan kursus internal (apresiasi pembicara) dari katalog publik")],
                [T("Data hygiene", "Kebersihan data"), T("Deleting a student also removes their enrolments, quiz history and assignment submissions", "Menghapus akun siswa ikut menghapus pendaftaran, riwayat kuis, dan kiriman tugasnya")]])
            + f'<h3 style="margin-top:22px">{s(T("2 · Indonesian translation for Tutor LMS (v1.0.6)", "2 · Terjemahan Indonesia untuk Tutor LMS (v1.0.6)"))}</h3>'
            + f'<p>{s(T("Tutor LMS has no official Indonesian translation. This plugin translates about 1,440 strings from Tutor and Tutor Pro, in both PHP and JavaScript, and is built from a JSON source with a small build script.", "Tutor LMS belum punya terjemahan resmi Bahasa Indonesia. Plugin ini menerjemahkan sekitar 1.440 teks dari Tutor dan Tutor Pro, baik PHP maupun JavaScript, dan dibangun dari sumber JSON dengan script build kecil."))}</p>'),

        section("design", T("Design & user experience", "Desain & pengalaman pengguna"),
            grid([card("palette", T("One visual system", "Satu sistem visual"), T("Dark theme with a lime accent and the Figtree font across Elementor pages, WooCommerce and the Tutor dashboard. Tutor's older light pages get a generated dark stylesheet.", "Tema gelap dengan aksen hijau limau dan font Figtree di semua halaman Elementor, WooCommerce, dan dashboard Tutor. Halaman Tutor lama yang masih terang diberi stylesheet gelap hasil generate.")),
                  card("globe", T("Guided landing pages", "Landing page panduan"), T("Step-by-step guides with real screenshots: how to check out (6 steps) and how to access a class (7 steps), each with an FAQ.", "Panduan langkah demi langkah dengan screenshot asli: cara checkout (6 langkah) dan cara akses kelas (7 langkah), masing-masing dengan FAQ.")),
                  card("calendar", T("Bootcamp landing", "Landing bootcamp"), T("Schedule, syllabus, rundown, pricing tiers, project brief, sample certificate, speaker and FAQ on one page.", "Jadwal, materi, rundown, paket harga, brief proyek, contoh sertifikat, pembicara, dan FAQ dalam satu halaman.")),
                  card("award", T("Certificate design", "Desain sertifikat"), T("Certificates rendered from HTML and positioned precisely, including a workaround for a 5px offset in Tutor's certificate builder.", "Sertifikat dirender dari HTML dan diposisikan presisi, termasuk solusi untuk pergeseran 5px di certificate builder Tutor.")),
                  card("layers", T("Marketing assets", "Aset promosi"), T("Course thumbnails and posters built in HTML, rendered with headless Chrome and exported as PNG and editable Canva files.", "Thumbnail kursus dan poster dibuat dengan HTML, dirender dengan Chrome headless, lalu diekspor sebagai PNG dan file Canva yang bisa diedit.")),
                  card("check", T("Clear learning flow", "Alur belajar jelas"), T("Strict completion: every lesson finished and every quiz or assignment passed before the certificate is issued automatically.", "Penyelesaian ketat: semua pelajaran selesai dan semua kuis atau tugas lulus, baru sertifikat terbit otomatis."))])),

        section("automation", T("Built and maintained as code", "Dibangun dan dikelola sebagai kode"),
            f'<p>{s(T("Most of the site is generated from a private Git repository, so every change is repeatable and reviewable.", "Sebagian besar situs dibuat dari repositori Git private, sehingga setiap perubahan bisa diulang dan ditinjau."))}</p>'
            + steps([(T("Generate", "Generate"), T("Python generators build the Elementor data for the home page and each landing page, plus the global CSS.", "Generator Python membuat data Elementor untuk beranda dan setiap landing page, plus CSS global.")),
                     (T("Back up", "Backup"), T("Before any change, the current settings and page data are exported to JSON.", "Sebelum ada perubahan, pengaturan dan data halaman yang sedang aktif diekspor ke JSON.")),
                     (T("Push", "Kirim"), T("Changes are sent through the WordPress REST API with a short-lived login session; course lessons and quizzes are pushed the same way.", "Perubahan dikirim lewat WordPress REST API dengan sesi login sementara; pelajaran dan kuis kursus dikirim dengan cara yang sama.")),
                     (T("Verify", "Verifikasi"), T("Elementor and hosting caches are cleared and the live page is compared with the generated payload.", "Cache Elementor dan hosting dibersihkan, lalu halaman live dibandingkan dengan payload yang dibuat."))])),

        section("security", T("Security & operations", "Keamanan & operasional"),
            grid([card("shield", T("No secrets in the repo", "Tidak ada rahasia di repo"), T("Passwords stay in a local file with restricted permissions; login cookies and REST nonces are deleted after each session.", "Password disimpan di file lokal dengan izin terbatas; cookie login dan nonce REST dihapus setelah setiap sesi.")),
                  card("mail", T("Reliable e-mail", "E-mail andal"), T("All mail goes through authenticated SMTP over SSL instead of PHP mail, so order and certificate e-mails reach the inbox.", "Semua e-mail lewat SMTP terautentikasi dengan SSL, bukan PHP mail, sehingga e-mail pesanan dan sertifikat sampai ke inbox.")),
                  card("bolt", T("Safe updates", "Update aman"), T("Customisations live in plugins and generators, not in edited core or plugin files, and must be re-checked after Tutor updates.", "Kustomisasi ada di plugin dan generator, bukan di file core atau plugin yang diubah, dan dicek ulang setiap kali Tutor di-update.")),
                  card("check", T("Order workflow", "Alur pesanan"), T("Orders stay on hold until payment is confirmed; marking them completed enrols the student and sends the e-mail automatically.", "Pesanan ditahan sampai pembayaran dikonfirmasi; saat ditandai selesai, siswa otomatis terdaftar dan menerima e-mail.")),
                  card("users", T("Role separation", "Pemisahan peran"), T("Separate flows and dashboards for students, instructors and admin, with admin approval for instructors and their courses.", "Alur dan dashboard terpisah untuk siswa, instruktur, dan admin, dengan persetujuan admin untuk instruktur dan kursusnya.")),
                  card("code", T("Documented", "Terdokumentasi"), T("An internal handbook covers every component, daily operations and how to re-run each script.", "Buku panduan internal mencakup setiap komponen, operasional harian, dan cara menjalankan ulang setiap script."))])),

        section("skills", T("What this project demonstrates", "Yang ditunjukkan project ini"),
            ul([T("Installing and configuring self-hosted WordPress for a real business, including locale, time zone, HTTPS, caching and CDN.", "Memasang dan mengonfigurasi WordPress self-hosted untuk bisnis nyata, termasuk bahasa, zona waktu, HTTPS, cache, dan CDN."),
                T("Integrating an LMS, an e-commerce store and transactional e-mail into one working flow, from checkout to certificate.", "Mengintegrasikan LMS, toko e-commerce, dan e-mail transaksional menjadi satu alur yang berjalan, dari checkout sampai sertifikat."),
                T("Writing custom WordPress plugins in PHP for bug fixes, business rules and translation.", "Menulis plugin WordPress custom dengan PHP untuk perbaikan bug, aturan bisnis, dan terjemahan."),
                T("Managing WordPress and Elementor through the REST API with scripts, backups and repeatable deployments.", "Mengelola WordPress dan Elementor lewat REST API dengan script, backup, dan deployment yang bisa diulang."),
                T("Designing a consistent, Indonesian-language user experience across theme, LMS and store.", "Merancang pengalaman pengguna berbahasa Indonesia yang konsisten di tema, LMS, dan toko.")])
            + f'<p class="note" style="margin-top:18px">{s(T("Need something similar? I also set up WordPress, Nextcloud, Immich and other self-hosted platforms for businesses. See the portfolio for contact options.", "Butuh yang serupa? Saya juga memasang WordPress, Nextcloud, Immich, dan platform self-hosted lain untuk bisnis. Lihat portofolio untuk opsi kontak."))} <a href="{PORTFOLIO}">diimasogan.github.io</a></p>'),
    ]


# ---------------------------------------------------------------- page template
CSS = """
:root{--bg:#F6F7F4;--surface:#FFFFFF;--surface2:#EEF1EA;--ink:#17191A;--muted:#5B616A;--line:#DDE2D7;
 --navy:#111111;--acc:#3A8F00;--acc-ink:#2F7600;--acc-tint:#E9F6DC;--amber:#0E9F9F;--amber-tint:#DFF5F5;--hero:#111111;--hero-ink:#C8CCC4;--eyebrow:#82FF1F;
 --ico-ink:#FFFFFF;--btn-ink:#FFFFFF;--shadow:0 1px 2px rgba(17,17,17,.06),0 6px 20px rgba(17,17,17,.06)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0F0F10;--surface:#17171A;--surface2:#1D1D21;--ink:#E8E8EA;--muted:#A3A3AB;
 --line:#2A2A2F;--navy:#F2F2F3;--acc:#82FF1F;--acc-ink:#9BFF4F;--acc-tint:#1F2E12;--amber:#18D4D4;--amber-tint:#10292A;--hero:#0A0A0B;--ico-ink:#111111;--btn-ink:#111111;--shadow:none}}
:root[data-theme="dark"]{--bg:#0F0F10;--surface:#17171A;--surface2:#1D1D21;--ink:#E8E8EA;--muted:#A3A3AB;--line:#2A2A2F;--navy:#F2F2F3;
 --acc:#82FF1F;--acc-ink:#9BFF4F;--acc-tint:#1F2E12;--amber:#18D4D4;--amber-tint:#10292A;--hero:#0A0A0B;--ico-ink:#111111;--btn-ink:#111111;--shadow:none}
th{background:#111111!important}
.ico{stroke:var(--ico-ink)!important}
a.btn{color:var(--btn-ink)!important}
.snum{color:var(--btn-ink)!important}
header.hero{background:radial-gradient(520px 260px at 85% 0%,rgba(130,255,31,.22),transparent 70%),var(--hero)!important}
"""
CSS_COMMON = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Segoe UI",Calibri,Arial,sans-serif}
a{color:var(--acc-ink)}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em;background:var(--surface2);padding:1px 5px;border-radius:5px}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
header.hero{background:var(--hero);color:#fff;padding:56px 0 44px}
.hero .eyebrow{color:var(--eyebrow);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:13px}
.hero h1{font:700 clamp(32px,5vw,52px)/1.1 Cambria,Georgia,serif;margin:10px 0 12px}
.hero p{color:var(--hero-ink);max-width:760px;margin:0;font-size:18px}
.hero .meta{margin-top:18px;color:var(--hero-ink);opacity:.8;font-size:14px}
nav.toc{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.toc .wrap{display:flex;gap:6px;overflow-x:auto;padding-top:10px;padding-bottom:10px;align-items:center}
nav.toc a{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:14px;padding:6px 10px;border-radius:999px}
nav.toc a:hover{background:var(--surface2);color:var(--ink)}
nav.toc .spacer{flex:1}
.tgl{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer;white-space:nowrap;text-decoration:none}
a.tgl{color:var(--ink)!important}
section{padding:44px 0 8px;scroll-margin-top:56px}
h2{font:700 30px/1.2 Cambria,Georgia,serif;color:var(--navy);margin:0 0 14px}
h3{font-size:18px;margin:0 0 6px;color:var(--ink)}
.lead{font-size:18px;color:var(--muted);max-width:820px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}
.stat{background:var(--acc-tint);border-radius:14px;padding:18px;text-align:center}
.stat b{display:block;font:700 34px/1.1 Cambria,Georgia,serif;color:var(--acc-ink)}
.stat span{color:var(--muted);font-size:14px}
.grid{display:grid;gap:14px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow)}
.card p{margin:0;color:var(--muted)}
.ihead{display:flex;gap:12px;align-items:center;margin-bottom:8px}
.ico{width:40px;height:40px;flex:none;padding:9px;border-radius:50%;background:var(--acc);stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.amber .ico{background:var(--amber)}
figure{margin:18px 0;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:10px;overflow:auto}
figure svg{display:block;width:100%;height:auto;min-width:720px;font-family:"Segoe UI",Calibri,Arial,sans-serif}
figcaption{color:var(--muted);font-size:14px;text-align:center;padding:6px}
svg .lane rect{fill:var(--surface2);stroke:var(--line)}svg .lt{fill:var(--muted);font-size:13px;font-weight:700;text-anchor:middle;letter-spacing:.04em;text-transform:uppercase}
svg .bx rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}svg .bx text{fill:var(--ink);font-size:14px;font-weight:600;text-anchor:middle}
svg .bx text.sm{fill:var(--muted);font-size:11.5px;font-weight:400}
svg .bx.hl rect{stroke:var(--acc);stroke-width:2;fill:var(--acc-tint)}svg .bx.amb rect{stroke:var(--amber);stroke-width:2;fill:var(--amber-tint)}
svg .ln path{fill:none;stroke:var(--acc);stroke-width:2}svg .mk{fill:var(--acc)}
ul.clean,ol.clean{padding-left:22px;margin:10px 0}ul.clean li,ol.clean li{margin:6px 0}
.note{background:var(--amber-tint);border-radius:12px;padding:14px 16px;color:var(--ink)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:15px}
th{color:#fff;text-align:left;padding:10px 14px;font-weight:600}
td{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:var(--surface2)}
.q{font-weight:700;color:var(--navy);margin:0 0 6px!important;font-size:17px}
.starter{display:flex;gap:16px;align-items:flex-start;margin:14px 0}.starter p{margin:0 0 6px;color:var(--muted)}
.snum{flex:none;width:40px;height:40px;border-radius:50%;background:var(--acc);color:#fff;font:700 18px/40px Cambria,Georgia,serif;text-align:center}
a.btn{display:inline-block;background:var(--acc);text-decoration:none;font-weight:600;padding:10px 18px;border-radius:10px}
footer{padding:40px 0 60px;color:var(--muted);font-size:14px;border-top:1px solid var(--line);margin-top:40px}
body.present nav.toc{display:none}
body.present section,body.present header.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center}
body.present section{border-top:1px solid var(--line)}
@media (max-width:820px){.stats{grid-template-columns:repeat(2,1fr)}.g2,.g3{grid-template-columns:1fr}h2{font-size:26px}}
@media print{nav.toc,.tgl{display:none}section{break-inside:avoid}body{background:#fff}}
"""
JS = """<script>
(function(){var r=document.documentElement,k='doc-theme';
function set(t){if(t)r.setAttribute('data-theme',t);else r.removeAttribute('data-theme');try{localStorage.setItem(k,t)}catch(e){}}
try{var t=localStorage.getItem(k);if(t)r.setAttribute('data-theme',t)}catch(e){}
document.getElementById('theme').onclick=function(){var c=r.getAttribute('data-theme');set(c==='dark'?'light':c==='light'?'':'dark')};
document.getElementById('present').onclick=function(){document.body.classList.toggle('present')};
document.addEventListener('keydown',function(e){if(e.key==='f'&&document.body.classList.contains('present')){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}});
})();
</script>"""

TOC = [("summary", T("Summary", "Ringkasan")), ("features", T("What I set up", "Yang dibangun")),
       ("architecture", T("Architecture", "Arsitektur")), ("plugins", T("Custom plugins", "Plugin custom")),
       ("design", T("Design & UX", "Desain & UX")), ("automation", T("As code", "Sebagai kode")),
       ("security", T("Security & ops", "Keamanan & operasional")), ("skills", T("Skills shown", "Keahlian"))]


def page():
    other = "id" if LANG == "en" else "en"
    other_href = ("../" + LINK["en"]) if LANG == "id" else LINK["id"]
    toc = "".join(f'<a href="#{i}">{s(t)}</a>' for i, t in TOC)
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OGNIVID LEARN · {s(T("Self-hosted WordPress LMS", "LMS WordPress self-hosted"))}</title>
<meta name="description" content="{s(T("Documentation of OGNIVID LEARN, an online learning platform on self-hosted WordPress with Tutor LMS Pro, WooCommerce, Elementor Pro and custom plugins.", "Dokumentasi OGNIVID LEARN, platform belajar online di WordPress self-hosted dengan Tutor LMS Pro, WooCommerce, Elementor Pro, dan plugin custom."))}">
<style>{CSS_COMMON}{CSS}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">{s(T("Project Documentation", "Dokumentasi Project"))}</div>
  <h1>OGNIVID LEARN</h1>
  <p>{s(T("An online learning platform on self-hosted WordPress: LMS, store, certificates and bootcamps, set up and run end to end", "Platform belajar online di WordPress self-hosted: LMS, toko, sertifikat, dan bootcamp, dipasang dan dijalankan dari awal sampai akhir"))}</p>
  <div class="meta">{s(T("Version 1.0 · November 2026 · Live site: ", "Versi 1.0 · November 2026 · Situs live: "))}<a href="{SITE}" style="color:#82FF1F">learn.ognivid.com</a></div>
</div></header>
<nav class="toc" aria-label="Contents"><div class="wrap">{toc}<span class="spacer"></span>
  <a class="tgl" href="{other_href}" hreflang="{other}">{"Bahasa Indonesia" if LANG == "en" else "English"}</a>
  <button class="tgl" id="present" title="One section per screen (F = full screen)">{s(T("Presentation mode", "Mode presentasi"))}</button>
  <button class="tgl" id="theme">{s(T("Theme", "Tema"))}</button>
</div></nav>
<main class="wrap">
{"".join(content())}
</main>
<footer><div class="wrap">OGNIVID LEARN · <a href="{SITE}">learn.ognivid.com</a> · <a href="{PORTFOLIO}">{s(T("Portfolio", "Portofolio"))}</a></div></footer>
{JS}
</body>
</html>
"""


INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=OGNIVID-LEARN-Documentation.html">
<title>OGNIVID LEARN documentation</title></head><body><a href="OGNIVID-LEARN-Documentation.html">English</a> · <a href="id/OGNIVID-LEARN-Dokumentasi.html">Bahasa Indonesia</a></body></html>
"""

if __name__ == "__main__":
    for LANG in ("en", "id"):
        OUT[LANG].parent.mkdir(parents=True, exist_ok=True)
        OUT[LANG].write_text(page(), encoding="utf-8")
        print("wrote", OUT[LANG].relative_to(ROOT))
    (ROOT / "docs" / "index.html").write_text(INDEX, encoding="utf-8")
    print("wrote docs/index.html")
