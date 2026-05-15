// dashboard.js

const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("certificateForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const payload = {

        name: document.getElementById("name").value,
        domain: document.getElementById("domain").value,
        mark: document.getElementById("mark").value,
        domain_code: document.getElementById("domain_code").value,
        batch: document.getElementById("batch").value,
        group: document.getElementById("group").value
    };

    try{

        const response = await fetch(`${API_URL}/generate-certificate`,{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(payload)
        });

        const data = await response.json();

        document.getElementById("result").innerHTML = `
        
            <h3 style="color:green;">
                Certificate Generated Successfully
            </h3>

            <p>
                <strong>Certificate ID:</strong>
                ${data.certificate_id}
            </p>

            <a href="${API_URL}${data.download_url}" target="_blank">
                Download Certificate
            </a>
        `;

    }catch(error){

        document.getElementById("result").innerHTML = `
            <h3 style="color:red;">
                Server Error
            </h3>
        `;
    }

});