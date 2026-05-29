# markitdown-api

API serverless per convertire file e URL in Markdown, basata su [MarkItDown](https://github.com/microsoft/markitdown) di Microsoft. Deploy su Vercel in 2 minuti.

---

## 🚀 Deploy su Vercel

### 1. Prerequisiti
- Account [Vercel](https://vercel.com) (gratuito)
- [Vercel CLI](https://vercel.com/docs/cli) installata: `npm i -g vercel`
- oppure collegare direttamente la repo da GitHub

### 2. Deploy da terminale

```bash
# Clona o copia questa cartella, poi:
cd markitdown-api
vercel
```

Segui le istruzioni interattive. Al primo deploy Vercel chiederà:
- **Set up and deploy?** → Y
- **Which scope?** → scegli il tuo account
- **Link to existing project?** → N
- **Project name** → markitdown-api (o come vuoi)
- **Directory** → `.` (corrente)
- **Override settings?** → N

### 3. Deploy da GitHub (alternativa)
1. Crea una repo GitHub con questi file
2. Vai su [vercel.com/new](https://vercel.com/new)
3. Importa la repo → Deploy automatico ✅

---

## 📡 Endpoints

### `GET /`
Health check. Ritorna lo stato dell'API e la lista degli endpoint.

### `POST /api/convert/url`
Converti un URL (pagina web, YouTube, ecc.) in Markdown.

**Request:**
```json
{
  "url": "https://esempio.com/articolo"
}
```

**Response:**
```json
{
  "success": true,
  "source": "https://esempio.com/articolo",
  "markdown": "# Titolo articolo\n\nContenuto..."
}
```

**Esempio con curl:**
```bash
curl -X POST https://tua-api.vercel.app/api/convert/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Rome"}'
```

### `POST /api/convert/file`
Converti un file (PDF, DOCX, XLSX, PPTX, ecc.) in Markdown.

**Request:** `multipart/form-data` con campo `file`

**Response:**
```json
{
  "success": true,
  "filename": "documento.pdf",
  "markdown": "# Titolo\n\nContenuto estratto..."
}
```

**Esempio con curl:**
```bash
curl -X POST https://tua-api.vercel.app/api/convert/file \
  -F "file=@documento.pdf"
```

**Esempio con n8n:**
- Node: HTTP Request
- Method: POST
- URL: `https://tua-api.vercel.app/api/convert/url`
- Body: JSON `{"url": "{{ $json.url }}"}`

---

## 📦 Formati supportati

| Tipo | Formati |
|------|---------|
| Documenti | PDF, DOCX, PPTX, XLSX, XLS |
| Web | HTML, URL, YouTube |
| Testo | CSV, JSON, XML, TXT |
| Media | JPG, PNG (OCR), MP3, WAV (trascrizione) |
| Archivi | ZIP (itera il contenuto) |
| Ebook | EPUB |

---

## ⚠️ Limiti Vercel Free Tier

| Limite | Valore |
|--------|--------|
| Timeout per richiesta | 10 secondi |
| Dimensione payload | 4.5 MB |
| Invocazioni/mese | 100,000 |
| Memoria | 1024 MB |

Per file grandi o conversioni lente (audio, OCR), considera il piano Pro (60s timeout).

---

## 🔧 Uso in n8n (integrazione PulseIT)

Node **HTTP Request** con:
- Method: `POST`
- URL: `https://tua-api.vercel.app/api/convert/url`
- Body Type: `JSON`
- Body: `{ "url": "{{ $json.article_url }}" }`

L'output `markdown` è pronto da passare a Claude Haiku per la generazione articolo.
