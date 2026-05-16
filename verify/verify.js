// verify.js

const API_URL = "https://mcq-certificate-oo0j.onrender.com";

async function verifyCertificate(){

    const certificate_id = document.getElementById("certificate_id").value;

    const result = document.getElementById("result");

    if(!certificate_id){

        result.innerHTML = `
            <p class="invalid">
                Please Enter Certificate ID
            </p>
        `;

        return;
    }

    try{

        const response = await fetch(
            `${API_URL}/verify/${certificate_id}`
        );

        const data = await response.json();

        if(data.success){

            result.innerHTML = `

                <div class="result-card">

                    <h3>
                        Certificate Verified
                    </h3>

                    <p>
                        <strong>Name:</strong>
                        ${data.name}
                    </p>

                    <p>
                        <strong>Domain:</strong>
                        ${data.domain}
                    </p>

                    <p>
                        <strong>Mark:</strong>
                        ${data.mark}
                    </p>

                    <p>
                        <strong>Batch:</strong>
                        ${data.batch}
                    </p>

                    <p>
                        <strong>Group:</strong>
                        ${data.group}
                    </p>

                    <p>
                        <strong>Date of Issue:</strong>
                        ${data.issue_date}
                    </p>

                    <a
    href="${API_URL}${data.download_url}"
    download
    class="download-btn"
    >
        Download Certificate PDF
    </a>

                </div>
            `;

        }else{

            result.innerHTML = `
                <p class="invalid">
                    Invalid Certificate ID
                </p>
            `;
        }

    }catch(error){

        result.innerHTML = `
            <p class="invalid">
                Server Error
            </p>
        `;
    }
}