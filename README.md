# No-Stick distro catalogue

The list of distributions that [No-Stick](https://github.com/wallisoft/no-stick) offers in its
"Download a distro" window. No-Stick reads [distros.json](distros.json) from this repository each time
that window opens, so a change here reaches every user without a new release of the app.

This is a list of download links only. How a distro is made to boot lives in No-Stick's
[recipes](https://github.com/wallisoft/no-stick/tree/main/recipes), which are code, reviewed and shipped
with the app.

## Adding or updating a distro

Open a pull request that edits `distros.json`. Each entry has exactly these fields:

| Field | Meaning |
|---|---|
| `name` | What the user sees, with the version |
| `group` | The heading it appears under. Groups show in the order they first appear in the file |
| `size` | Download size, as text, e.g. `"2.9G"` |
| `live` | `true` if No-Stick can boot it live |
| `install` | `true` if No-Stick can install it to a virtual disk |
| `status` | A few honest words: what has actually been tried |
| `url` | A direct `https://` link to the `.iso`, on the distro's own site or an official mirror |

Rules:

- **Official links only.** The distro's own download server or a mirror it lists. Never a repackaged ISO.
- **Be honest in `group` and `status`.** "Tested on real hardware" means someone booted it on a physical
  machine, not in a virtual machine. If you haven't, put it under "Same recipe - not yet tested".
- **No commas** in `name`, `group`, `status` or `size`; the app's list uses them to separate rows.
- **Only list what No-Stick can boot.** A distro needs a recipe for its family first. Fedora's immutable
  variants (Silverblue, Bazzite, Bluefin, Aurora) and Vanilla OS are not here because no recipe exists yet;
  a recipe for them would be very welcome.

Every pull request is checked automatically: the file must be well-formed and every link must answer with
a real ISO. The same check runs every Monday, because links die whenever a distro publishes a point
release. Run it yourself with `python3 check.py`.

## Licence

MIT, the same as No-Stick.
