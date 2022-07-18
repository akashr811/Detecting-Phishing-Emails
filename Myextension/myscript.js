
fetch('http://127.0.0.1:5000/ext', {
    mode: 'cors',
    credentials: 'include',
    method: 'GET'
})
    .then(res => res.json())
    .then(Data => {
        const Allmails = Data.MailsChecked;
        const Phishy=Data.PhishingEmails;
        const all = document.getElementById('all');
        const ep = document.getElementById('ep');
        all.innerHTML = Allmails;
        ep.innerHTML = Phishy;    
    })
