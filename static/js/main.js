// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {

  // --- DOM Element Selectors ---
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const dropzoneText = document.getElementById('dropzoneText');
  const uploadBtn = document.getElementById('uploadBtn');
  const btnText = document.getElementById('btnText');
  const loader = document.getElementById('loader');
  const reportsList = document.getElementById('reportsList');
  const reportView = document.getElementById('reportView');
  const closeReportBtn = document.getElementById('closeReportBtn');

  let selectedFile = null;

  // --- UI State Functions ---
  const showLoader = (isLoading) => {
    loader.style.display = isLoading ? 'block' : 'none';
    btnText.textContent = isLoading ? 'Reviewing...' : 'Upload & Review';
    uploadBtn.disabled = isLoading;
    fileInput.disabled = isLoading;
  };

  const showToast = (message, isError = false) => {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${isError ? 'error' : ''}`;
    setTimeout(() => {
      toast.className = toast.className.replace('show', '');
    }, 3000);
  };

  // --- API Call Functions ---
  const fetchReports = async () => {
    try {
      const res = await fetch('/reports?limit=50');
      if (!res.ok) throw new Error('Failed to fetch reports');
      const data = await res.json();
      
      reportsList.innerHTML = '';
      if (!data.length) {
        reportsList.innerHTML = '<p class="muted">No reports yet.</p>';
        return;
      }

      data.forEach(r => {
        const div = document.createElement('div');
        div.className = 'report-item';
        div.innerHTML = `<strong>${r.filename}</strong><div class='muted' style='font-size:12px'>${new Date(r.uploaded_at).toLocaleString()}</div>`;
        div.onclick = () => showReport(r.uuid);
        reportsList.appendChild(div);
      });
    } catch (error) {
      console.error(error);
      showToast(error.message, true);
    }
  };

  const showReport = async (uuid) => {
    try {
      const res = await fetch(`/report/${uuid}`);
      if (!res.ok) throw new Error('Failed to load report');
      const data = await res.json();
      
      document.getElementById('reportTitle').innerText = data.filename;
      document.getElementById('reportMeta').innerText = `Model: ${data.llm_model || 'N/A'} | Language: ${data.language}`;
      
      const reviewMd = data.review_text || '(No review available)';
      document.getElementById('reviewMarkdown').innerHTML = marked.parse(reviewMd);
      
      const codeEl = document.getElementById('codeText');
      codeEl.textContent = data.code_content || '';
      hljs.highlightElement(codeEl);
      
      reportView.style.display = 'block';
      window.scrollTo({ top: reportView.offsetTop - 20, behavior: 'smooth' });
    } catch (error) {
      console.error(error);
      showToast(error.message, true);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      showToast('Please select a file first.', true);
      return;
    }

    showLoader(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch('/review-file', { method: 'POST', body: formData });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Review failed');
      }
      const result = await res.json();
      showToast('Review complete!');
      await fetchReports();
      showReport(result.uuid);
    } catch (error) {
      console.error(error);
      showToast(error.message, true);
    } finally {
      showLoader(false);
    }
  };

  // --- Event Listeners ---
  dropzone.addEventListener('click', () => fileInput.click());
  closeReportBtn.addEventListener('click', () => reportView.style.display = 'none');
  uploadBtn.addEventListener('click', uploadFile);

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, e => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'));
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'));
  });

  dropzone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      handleFileSelect({ target: fileInput });
    }
  });
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      selectedFile = file;
      dropzoneText.textContent = selectedFile.name;
      uploadBtn.disabled = false;
      btnText.textContent = 'Upload & Review';
    } else {
      selectedFile = null;
      dropzoneText.textContent = 'Drop a file or click to choose';
      uploadBtn.disabled = true;
      btnText.textContent = 'Select a File';
    }
  };
  
  fileInput.addEventListener('change', handleFileSelect);

  // --- Initial Load ---
  fetchReports();
});