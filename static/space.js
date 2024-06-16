$(document).ready(function() {
    $('#upload-form').submit(function(event) {
        event.preventDefault();
        
        var formData = new FormData();
        formData.append('file', $('#file')[0].files[0]);

        fetch('/analyze-tif', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'analyzed_data.zip');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        })
        .catch(error => {
            alert('Ошибка при экспорте данных в SHP: ' + error);
        });
    });
});
