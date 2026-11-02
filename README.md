# Sito di Patrizia Vaccaro – patriziavaccaro.net

Sito statico pubblicato con GitHub Pages dal ramo `main`.

## Come si modifica

1. Prima di tutto: `git pull` (altre conversazioni possono aver modificato il sito).
2. Si modificano **solo** i file in `_sorgenti/`:
   - `pagina.html` – testi e stile della pagina principale
   - `articoli.py` – articoli (il primo dell'elenco compare per primo)
   - `foto.jpg`, `fonts/`
3. Si rigenera il sito: `python3 _sorgenti/build.py`
4. Si controlla e si pubblica: `git add -A && git commit && git push`

Tutti gli altri file vengono rigenerati da `build.py`: non vanno modificati a mano.
