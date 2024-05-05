
function selectFile() {
    document.getElementById('fileInput').click();
    document.getElementById('fileInput').addEventListener('change', function() {
        var selectedFile = this.files[0];
        console.log('Selected file:', selectedFile.name);
        FileText = document.getElementById('FileText')
        const last = selectedFile.name.split('.').slice(-1);
        FileText.innerHTML = `Selected a :<h1>${last}</h1> File`
        console.log(selectedFile.name.split('.'))
        document.getElementById('PlusImage').style.display = "none"
        document.getElementById('ButtonsContinaer').style.display = 'flex'
    });
}

async function handleGenerationOftheCode() {
    const fileInput = document.getElementById('fileInput');
    const selectedFile = fileInput.files[0];

    // Check if a file has been selected
    if (!selectedFile) {
        console.error("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/add-file', {
            method: "POST",
            body: formData // Use FormData object to send file data
        });
        const data = await response.json();
        if (response.status === 200) {
            console.log("File uploaded successfully");
            afterCodeGeneration(data.file_id,data.file_name) // Log any response data from the server
        } else {
            console.error("Error uploading file:", data.error);
        }
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}


async function afterCodeGeneration(id,fileName){
    alert(`The Code for the File ${fileName} is ${id} and u can share the Link http://localhost:5000/file/${id}`);
    window.location.reload();
}


async function handleFileDownload() {
    const code = document.getElementById('basic-url').value;
    try {
        const response = await fetch(`/file/${code}`);
        const data = await response.json();
        if (response.status == 200) {
            console.log("The File name is:", data.fileName);
            const confirmDownload = confirm(`Do you want to download "${data.fileName}"?`);
            if (confirmDownload) {
                try {
                    const downloadResponse = await fetch(`/download/Uploads/${data.fileName}`);
                    const blob = await downloadResponse.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = data.fileName;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    window.location.reload();
                } catch (error) {
                    console.log("Error downloading file:", error);
                }
            } else {
                console.log("Download canceled by user");
            }
        } else {
            alert("Error in the Code Duck YourSelf");
        }
    } catch (error) {
        console.log("Error fetching file data:", error);
    }
}

