"""Password lock for instructor-guide.html (a stopgap until real authentication and authorization).

The site is static and the repository is public, so a password check in JavaScript alone would hide nothing:
the guide would still be readable in the page source. Instead the build encrypts the whole guide
(AES-256-GCM, key from PBKDF2-SHA256) and publishes only a password prompt plus the ciphertext.
The browser decrypts it with the Web Crypto API once the right password is typed.

The password is never committed. It comes from, in order:
  * the CSCI391_GUIDE_PASSWORD environment variable, or
  * curriculum/private/guide_password.txt (gitignored; created with a random password on first build).
Change the password by editing that file (or setting the variable) and rebuilding.
"""
import base64
import html
import os
import secrets

HERE = os.path.dirname(os.path.abspath(__file__))
PRIVATE = os.path.join(HERE, "private")
PW_FILE = os.path.join(PRIVATE, "guide_password.txt")
ITERATIONS = 310_000


def password():
    pw = os.environ.get("CSCI391_GUIDE_PASSWORD", "").strip()
    if pw:
        return pw
    if os.path.exists(PW_FILE):
        pw = open(PW_FILE, encoding="utf8").read().strip()
        if pw:
            return pw
    os.makedirs(PRIVATE, exist_ok=True)
    pw = "-".join(secrets.token_hex(3) for _ in range(4))
    with open(PW_FILE, "w", encoding="utf8") as f:
        f.write(pw + "\n")
    print(f"Created a new instructor's guide password in {PW_FILE}")
    return pw


def encrypt(plaintext, pw):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(pw.encode("utf8"))
    ct = AESGCM(key).encrypt(iv, plaintext.encode("utf8"), None)
    b64 = lambda b: base64.b64encode(b).decode("ascii")  # noqa: E731
    return {"salt": b64(salt), "iv": b64(iv), "ct": b64(ct), "iter": ITERATIONS}


def locked_page(guide_html, title):
    """The published instructor-guide.html: a password prompt and the encrypted guide. Never the plaintext."""
    try:
        blob = encrypt(guide_html, password())
    except ImportError:
        blob = None  # no crypto library: publish the prompt with nothing behind it rather than the plaintext
    data = "null" if blob is None else '{"salt":"%(salt)s","iv":"%(iv)s","ct":"%(ct)s","iter":%(iter)d}' % blob
    return GATE.replace("__TITLE__", html.escape(title)).replace("__DATA__", data)


GATE = r"""<!DOCTYPE html>
<!-- GENERATED FILE: built by curriculum/build_site.py. The guide below is encrypted; see curriculum/guide_lock.py. -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE__</title>
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--maroon:#70002e;--maroon-d:#4f0020;--ink:#1f1a1c;--muted:#5b5559;--line:#e4dfe1;--soft:#f7f5f2}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px 16px;background:var(--soft);color:var(--ink);font-family:Inter,'Segoe UI',system-ui,Arial,sans-serif}
.card{width:100%;max-width:420px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px 28px;box-shadow:0 10px 30px rgba(0,0,0,.06)}
.brand{display:inline-block;background:var(--maroon);color:#fff;border-radius:6px;padding:5px 8px;font-size:13px;font-weight:800;letter-spacing:.04em}
h1{font-size:24px;margin:14px 0 6px}
p{margin:0 0 18px;color:var(--muted);font-size:15px;line-height:1.5}
label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}
input{width:100%;font:inherit;font-size:16px;padding:11px 12px;border:1.5px solid var(--line);border-radius:8px}
input:focus{outline:none;border-color:var(--maroon);box-shadow:0 0 0 3px rgba(112,0,46,.12)}
button{margin-top:14px;width:100%;font:inherit;font-weight:700;font-size:15px;color:#fff;background:var(--maroon);border:0;border-radius:8px;padding:12px;cursor:pointer}
button:hover{background:var(--maroon-d)}
button[disabled]{opacity:.6;cursor:progress}
.err{color:#b3261e;font-size:14px;margin:10px 0 0;min-height:1.2em}
.back{display:block;margin-top:18px;font-size:14px;color:var(--maroon)}
</style>
</head>
<body>
<form class="card" id="gate" autocomplete="off">
  <span class="brand">CSCI 391</span>
  <h1>Instructor's guide</h1>
  <p>This guide holds quiz questions and answer keys, so it's for instructors only. Enter the password to open it.</p>
  <label for="pw">Password</label>
  <input id="pw" type="password" autocomplete="current-password" required autofocus>
  <button type="submit" id="go">Open the guide</button>
  <p class="err" id="err" role="alert"></p>
  <a class="back" href="index.html">← Back to the course site</a>
</form>
<script>
(function () {
  var DATA = __DATA__, SKEY = 'csci391-guide-key';
  var form = document.getElementById('gate'), err = document.getElementById('err'), go = document.getElementById('go');
  function bytes(b64) { var s = atob(b64), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function show(text) { document.open(); document.write(text); document.close(); }
  function open(key) {
    return crypto.subtle.decrypt({ name: 'AES-GCM', iv: bytes(DATA.iv) }, key, bytes(DATA.ct))
      .then(function (buf) { return new TextDecoder().decode(buf); });
  }
  if (!DATA || !window.crypto || !crypto.subtle) {
    err.textContent = !DATA ? 'The guide was built without encryption support, so it is not available here.'
                            : 'This browser cannot open the guide (Web Crypto is unavailable).';
    go.disabled = true; return;
  }
  // Stay unlocked for this browser tab's session.
  try {
    var saved = sessionStorage.getItem(SKEY);
    if (saved) crypto.subtle.importKey('raw', bytes(saved), 'AES-GCM', true, ['decrypt']).then(open).then(show)
      .catch(function () { try { sessionStorage.removeItem(SKEY); } catch (e) {} });
  } catch (e) {}
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    err.textContent = ''; go.disabled = true; go.textContent = 'Checking…';
    var pw = new TextEncoder().encode(document.getElementById('pw').value), key;
    crypto.subtle.importKey('raw', pw, 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: bytes(DATA.salt), iterations: DATA.iter, hash: 'SHA-256' },
                                       base, { name: 'AES-GCM', length: 256 }, true, ['decrypt']);
      })
      .then(function (k) { key = k; return open(k); })
      .then(function (text) {
        crypto.subtle.exportKey('raw', key).then(function (raw) {
          try { sessionStorage.setItem(SKEY, btoa(String.fromCharCode.apply(null, new Uint8Array(raw)))); } catch (e) {}
        }).finally(function () { show(text); });
      })
      .catch(function () {
        err.textContent = 'That password is not right.'; go.disabled = false; go.textContent = 'Open the guide';
        document.getElementById('pw').select();
      });
  });
})();
</script>
</body>
</html>
"""
