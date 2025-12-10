# Resume Upload API - Test Guide

## ✅ API Endpoint

**POST** `http://localhost:8000/api/candidates/upload/`

---

## 📤 How to Upload a Resume

### Using cURL:
```bash
curl -X POST http://localhost:8000/api/candidates/upload/ \
  -F "resume_file=@/path/to/resume.pdf"
```

### Using JavaScript (Fetch):
```javascript
const formData = new FormData();
formData.append('resume_file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/candidates/upload/', {
  method: 'POST',
  body: formData,
});

const data = await response.json();
console.log(data);
```

### Using React Component:
```javascript
function ResumeUpload() {
  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('resume_file', e.target.files[0]);
    
    const response = await fetch('http://localhost:8000/api/candidates/upload/', {
      method: 'POST',
      body: formData,
    });
    
    const data = await response.json();
    console.log('Upload success:', data);
  };
  
  return (
    <input 
      type="file" 
      accept=".pdf,.docx" 
      onChange={handleUpload} 
    />
  );
}
```

---

## ✅ Success Response (201 Created)

```json
{
  "id": 1,
  "resume_file": "http://localhost:8000/media/resumes/john_doe_resume.pdf",
  "created_at": "2025-12-10T17:23:45.123456Z",
  "message": "Resume uploaded successfully"
}
```

---

## ❌ Error Response (400 Bad Request)

```json
{
  "resume_file": [
    "This field is required."
  ]
}
```

---

## 📁 File Storage

Uploaded files are saved to:
```
server-resume-parser/media/resumes/
```

---

## 🧪 Test from Terminal

```bash
cd /Users/ayush/lrn/server-resume-parser
source venv/bin/activate
python manage.py runserver
```

Then in another terminal:
```bash
curl -X POST http://localhost:8000/api/candidates/upload/ \
  -F "resume_file=@/path/to/your/resume.pdf"
```
