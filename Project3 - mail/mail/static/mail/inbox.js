document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function hide_all_views() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}

function compose_email(replyData) {

  // Show compose view and hide other views
  hide_all_views();
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Fill out the composition fields if this is a reply
  if(replyData.to){
    document.querySelector('#compose-recipients').value = replyData.to;
    document.querySelector('#compose-subject').value = replyData.subject;
    document.querySelector('#compose-body').value = replyData.body;
  }

  document.querySelector('#compose-form .btn').addEventListener('click', send_email);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  hide_all_views();
  const emailsView = document.querySelector('#emails-view');
  emailsView.style.display = 'block';

  // Show the mailbox name, this should also destroy any container built after it.
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(mail => {
    // Check that something was returned
    if(mail.length){
      // build a ul to contain the list of fetched mail
      const mailContainer = document.createElement("ul");
      mailContainer.setAttribute("class", "mail-container list-group");
      emailsView.append(mailContainer);

      // display the emails in a list
      const itemTemplate = {};
      mail.forEach(item => {
        // Build templates based on mailbox (this seems inefficient, but is it more inefficient than comparisons?)
        itemTemplate['inbox'] = `<span>From: ${item.sender}</span><span>Subject: ${item.subject}</span><span>${item.timestamp}</span>`
        itemTemplate['sent'] = `<span>To: ${item.recipients[0]}</span><span>Subject: ${item.subject}</span><span>${item.timestamp}</span>`
        itemTemplate['archive'] = `<span>Subject: ${item.subject}</span><span>From: ${item.sender}</span><span>${item.recipients[0]}</span>`

        // build the list element
        const listItem = document.createElement("li");
        listItem.setAttribute("class", "list-group-item");
        listItem.style.display = "flex";
        listItem.style.justifyContent = "space-between";
        listItem.innerHTML = itemTemplate[mailbox];

        // check if message is read and add style as needed.
        if(item.read){
          listItem.style.backgroundColor = "#eee";
        } else {
          listItem.style.backgroundColor = "#fff";
        }

        // add a click event to open the email
        listItem.addEventListener("click", () => read_mail(item.id));
        
        // add the element to the container
        mailContainer.append(listItem);
      });
    } else {
      emailsView.append("No mail found for this view.")
    }
  });
}

function send_email(event){
  //cancel the post behavior for the button
  event.preventDefault();
  
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // api returns an error
      if (result.error){
        // check for and build err div
        const err = document.querySelector("#compose-form .err");
        if(!err){
          const errDiv = document.createElement("div");
          errDiv.setAttribute("class", "err");
          errDiv.innerHTML = result.error;
          document.querySelector("#compose-form").prepend(errDiv);
        } else {
          err.innerHTML = result.error;
        }
      } else {
        // no error so load the sent box
        load_mailbox('sent'); 
      }
  });
}

function read_mail(mailId){
  // Show the mailbox and hide other views
  hide_all_views();
  const emailView = document.querySelector('#emails-view');
  emailView.style.display = 'block';

  // Get the email to display
  fetch(`/emails/${mailId}`)
  .then(response => response.json())
  .then(item => {
    if(!item.error){
      // Do some stuff only if you're the recipient. Security is of no concern for this assignment
      const me = document.querySelector(".container > h2").innerHTML;
      if(item.recipients.includes(me)){
        // Mark the message as read
        fetch(`/emails/${mailId}`, {
          method: 'put',
          body: JSON.stringify({
            read: true
          })
        })

        // Build the view with actions as the recipient
        emailView.innerHTML = `
          <h3>${item.subject}</h3>
          <div><small>From ${item.sender} To ${item.recipients} on ${item.timestamp}</small></div>
          <p class="m-3">${item.body}</p>
          <button id="markUnread" class="btn btn-sm btn-outline-primary">Mark as ${item.read ? "unread" : "read"}</button>
          <button id="archiveItem" class="btn btn-sm btn-outline-primary">${item.archived ? "Unarchive" : "Archive"}</button>
          <button id="replyToItem" class="btn btn-sm btn-outline-primary">Reply</button>
        `;

        // Add some listeners for action buttons
        document.querySelector("#markUnread").addEventListener("click", () => {
          // toggle read status
          item.read = !item.read
          
          // update the server
          fetch(`/emails/${mailId}`, {
            method: 'put',
            body: JSON.stringify({
              read: item.read
            })
          })

          // update the button
          if(item.read){
            document.querySelector("#markUnread").innerHTML = "Mark as unread"
          } else {
            document.querySelector("#markUnread").innerHTML = "Mark as read"
          }
        })

        document.querySelector("#archiveItem").addEventListener("click", () => {
          // toggle read status
          item.archived = !item.archived

          // update the server
          fetch(`/emails/${mailId}`, {
            method: 'put',
            body: JSON.stringify({
              archived: item.archived
            })
          })
          .then(() => load_mailbox("inbox"));
        })

        document.querySelector("#replyToItem").addEventListener("click", () => {
          replyData = {
            "to": item.sender,
            "subject": `Re: ${item.subject}`,
            "body": `\n\n---\nOn ${item.timestamp} ${item.sender} wrote: \n${item.body}`
          }
          compose_email(replyData);
        })

      } else {
        // Build the view without the action buttons
          emailView.innerHTML = `
          <h3>${item.subject}</h3>
          <div><small>From ${item.sender} To ${item.recipients} on ${item.timestamp}</small></div>
          <p class="m-3">${item.body}</p>
        `;
      }
    } else {
      emailView.innerHTML = `<h3>Mail not found</h3>`;
    }
  });  
}