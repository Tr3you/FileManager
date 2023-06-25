document.getElementById("file-1").addEventListener("change", function (e){
    if(e.target.files[0]){
        const file = e.target.files[0];
        console.log(file)
        document.getElementById("file_name").innerText = `${file.name} | ${ file.size < 1000000 ? parseInt(file.size / 1000) + 'KB' : (file.size / 1000000).toFixed(2) + 'MB'}`
        document.getElementById("last_modified").value = file.lastModified;
    }
});